import time
import os
from queue import Queue, Empty
from threading import Thread
from typing import Optional, Tuple, List, Any, Dict

import cv2
import numpy as np
from ultralytics import YOLO

from .console import console
from .gps import GPSExtractor
from .location import LocationService
from .gmail_service import GmailService


class PotholeDetector:
    """Main pothole detection system with real-time processing capabilities."""

    def __init__(
        self,
        model_path: str,
        confidence_threshold: float = 0.5,
        gmail_service: Optional[GmailService] = None,
        location_service: Optional[LocationService] = None,
    ):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.gmail_service = gmail_service
        self.location_service = location_service
        self.model: Optional[YOLO] = None

        # Threading components for real-time processing
        self.frame_queue: Queue[Optional[np.ndarray]] = Queue(maxsize=2)
        self.result_queue: Queue[Tuple[np.ndarray, Any]] = Queue(maxsize=2)
        self.inference_thread: Optional[Thread] = None
        self.running = False

    def load_model(self) -> bool:
        """Load YOLO model."""
        try:
            with console.status("[bold blue]Loading YOLO model...", spinner="dots"):
                self.model = YOLO(self.model_path)
            console.print(f"[green]✓ Model loaded: {self.model_path}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Failed to load model: {e}[/red]")
            return False

    def _inference_worker(self):
        """Background thread for model inference."""
        while self.running:
            try:
                if not self.frame_queue.empty():
                    frame = self.frame_queue.get(timeout=0.1)
                    if frame is None:
                        break

                    # Run inference
                    if self.model is None:
                        continue
                    results = self.model(frame, verbose=False)

                    # Put result in queue if space available
                    if not self.result_queue.full():
                        self.result_queue.put((frame, results))
                else:
                    time.sleep(0.01)  # Prevent busy waiting

            except Empty:
                continue
            except Exception as e:
                console.print(f"[red]Inference error: {e}[/red]")
                time.sleep(0.01)

    def _draw_detections(self, frame: np.ndarray, results) -> Tuple[np.ndarray, bool]:
        """Draw bounding boxes and return if pothole detected."""
        pothole_detected = False

        if self.model is None:
            return frame, False

        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    # Get box coordinates and info
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]

                    # Check if pothole detected with sufficient confidence
                    if (
                        class_name.lower() in ["ph", "pothole"]
                        and confidence >= self.confidence_threshold
                    ):
                        pothole_detected = True
                        color = (0, 0, 255)  # Red for potholes
                    else:
                        color = (0, 255, 0)  # Green for other objects

                    # Draw bounding box and label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                    label = f"{class_name} {confidence:.2f}"
                    label_size = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
                    )[0]
                    cv2.rectangle(
                        frame,
                        (x1, y1 - label_size[1] - 10),
                        (x1 + label_size[0], y1),
                        color,
                        -1,
                    )
                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        2,
                    )

        return frame, pothole_detected

    def _send_pothole_alert(
        self,
        input_path: str,
        output_path: str,
        sender_email: str,
        recipient_emails: List[str],
        inference_time: float,
        is_video: bool = False,
        video_duration: Optional[float] = None,
    ):
        """Send email alert when pothole is detected."""
        if not self.gmail_service or not self.location_service:
            return

        # Extract GPS data
        gps_coords = None
        if is_video:
            gps_coords = GPSExtractor.from_video(input_path)
        else:
            gps_coords = GPSExtractor.from_image(input_path)

        # Prepare email content
        file_type = "video" if is_video else "image"
        subject = f"🚨 Pothole Detected in {file_type.title()}!"

        body_lines = [
            f"A pothole has been detected in the {file_type}: {os.path.basename(input_path)}",
            "",
            f"📁 Output {file_type}: {os.path.basename(output_path)}",
            f"⏱️ Inference time: {inference_time:.2f} seconds",
        ]

        if is_video and video_duration:
            body_lines.append(f"🎬 Video duration: {video_duration:.2f} seconds")

        if gps_coords:
            lat, lon = gps_coords
            address = self.location_service.get_address(lat, lon)
            maps_link = self.location_service.get_maps_link(lat, lon)

            body_lines.extend(
                [
                    "",
                    "📍 Location Details:",
                    f"   Latitude: {lat:.6f}",
                    f"   Longitude: {lon:.6f}",
                    f"   Address: {address}",
                    f"   🗺️ Google Maps: {maps_link}",
                ]
            )
        else:
            body_lines.extend(
                [
                    "",
                    f"⚠️ No GPS data available in the {file_type} file.",
                ]
            )

        body_text = "\n".join(body_lines)

        # Send email with attachments
        attachments = [input_path]
        if os.path.exists(output_path):
            attachments.append(output_path)

        self.gmail_service.send_alert(
            sender_email, recipient_emails, subject, body_text, attachments
        )

    def process_image(
        self,
        input_path: str,
        output_path: str,
        sender_email: Optional[str] = None,
        recipient_emails: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Process a single image."""
        start_time = time.time()

        # Load and process image
        image = cv2.imread(input_path)
        if image is None:
            raise ValueError(f"Could not load image: {input_path}")

        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")

        results = self.model(image, verbose=False)
        processed_image, pothole_detected = self._draw_detections(image, results)

        # Save output
        cv2.imwrite(output_path, processed_image)

        inference_time = time.time() - start_time

        # Send alert if pothole detected
        if pothole_detected and sender_email and recipient_emails:
            self._send_pothole_alert(
                input_path,
                output_path,
                sender_email,
                recipient_emails,
                inference_time,
                is_video=False,
            )

        return {
            "inference_time": inference_time,
            "pothole_detected": pothole_detected,
            "output_path": output_path,
        }

    def process_video(
        self,
        input_path: str,
        output_path: str,
        frame_skip: int = 2,
        sender_email: Optional[str] = None,
        recipient_emails: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Process video file with optimized threading."""
        start_time = time.time()

        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {input_path}")

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        video_duration = total_frames / fps if fps > 0 else 0

        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            output_path, fourcc, max(1, fps // (frame_skip + 1)), (width, height)
        )

        # Start inference thread
        self.running = True
        self.inference_thread = Thread(target=self._inference_worker, daemon=True)
        self.inference_thread.start()

        frame_count = 0
        pothole_detected = False
        processed_frames = []

        from rich.progress import Progress, SpinnerColumn, TextColumn

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Processing video..."),
            console=console,
        ) as progress:
            task = progress.add_task("Processing", total=total_frames)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1
                progress.update(task, advance=1)

                # Skip frames as specified
                if frame_count % (frame_skip + 1) != 0:
                    continue

                # Add frame to inference queue
                if self.frame_queue.empty():
                    self.frame_queue.put(frame.copy())

                # Get processed results
                if not self.result_queue.empty():
                    processed_frame, results = self.result_queue.get()
                    processed_frame, frame_pothole = self._draw_detections(
                        processed_frame, results
                    )

                    if frame_pothole:
                        pothole_detected = True

                    processed_frames.append(processed_frame)
                    out.write(processed_frame)

        # Process any remaining frames in queue
        while not self.result_queue.empty():
            try:
                processed_frame, results = self.result_queue.get_nowait()
                processed_frame, frame_pothole = self._draw_detections(
                    processed_frame, results
                )
                if frame_pothole:
                    pothole_detected = True
                out.write(processed_frame)
            except Empty:
                break

        # Cleanup
        self.running = False
        try:
            self.frame_queue.put_nowait(None)  # Signal thread to stop
        except Exception:
            pass

        if self.inference_thread and self.inference_thread.is_alive():
            self.inference_thread.join(timeout=1)

        cap.release()
        out.release()

        inference_time = time.time() - start_time

        # Send alert if pothole detected
        if pothole_detected and sender_email and recipient_emails:
            self._send_pothole_alert(
                input_path,
                output_path,
                sender_email,
                recipient_emails,
                inference_time,
                is_video=True,
                video_duration=video_duration,
            )

        return {
            "inference_time": inference_time,
            "video_duration": video_duration,
            "pothole_detected": pothole_detected,
            "output_path": output_path,
        }

    def process_webcam(
        self,
        output_path: Optional[str] = None,
        frame_skip: int = 2,
        camera_index: int = 0,
    ) -> None:
        """Process live webcam feed."""
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise ValueError(f"Could not open camera {camera_index}")

        # Get camera properties
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # Default to 30 if fps is 0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        console.print(f"[green]Camera opened: {width}x{height} @ {fps}fps[/green]")

        # Setup video writer if output path provided
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(
                output_path, fourcc, max(1, fps // (frame_skip + 1)), (width, height)
            )

        # Start inference thread
        self.running = True
        self.inference_thread = Thread(target=self._inference_worker, daemon=True)
        self.inference_thread.start()

        frame_count = 0

        console.print("[yellow]Press 'q' to quit, 's' to save current frame[/yellow]")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    console.print("[red]Failed to read from camera[/red]")
                    break

                frame_count += 1

                # Skip frames as specified
                if frame_count % (frame_skip + 1) != 0:
                    cv2.imshow("Pothole Detection", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    continue

                # Add frame to inference queue
                if self.frame_queue.empty():
                    self.frame_queue.put(frame.copy())

                # Display current frame (may not have detections yet)
                display_frame = frame.copy()

                # Get processed results if available
                if not self.result_queue.empty():
                    try:
                        processed_frame, results = self.result_queue.get_nowait()
                        display_frame, pothole_detected = self._draw_detections(
                            processed_frame, results
                        )

                        if pothole_detected:
                            # Add alert overlay
                            cv2.putText(
                                display_frame,
                                "POTHOLE DETECTED!",
                                (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 0, 255),
                                3,
                            )

                        # Save frame if recording
                        if out:
                            out.write(display_frame)
                    except Empty:
                        pass

                # Show frame
                cv2.imshow("Pothole Detection", display_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                elif key == ord("s"):
                    # Save current frame as image
                    timestamp = int(time.time())
                    save_path = f"frame_{timestamp}.jpg"
                    cv2.imwrite(save_path, display_frame)
                    console.print(f"[green]Frame saved: {save_path}[/green]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
        finally:
            # Cleanup
            self.running = False
            try:
                self.frame_queue.put_nowait(None)
            except Exception:
                pass

            if self.inference_thread and self.inference_thread.is_alive():
                self.inference_thread.join(timeout=1)

            cap.release()
            if out:
                out.release()
            cv2.destroyAllWindows()

            if output_path and out:
                console.print(f"[green]Video saved: {output_path}[/green]")

# enhanced_video_processor.py

"""import cv2
import numpy as np
import requests
import json
import time
import argparse
from collections import deque

def process_frame(frame, server_url, model=None, confidence=0.5):
    start_time = time.time()
    
    # Prepare the image for sending
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
    
    # Prepare query parameters
    params = {'confidence': confidence}
    if model:
        params['model'] = model
    
    # Send the image to the server
    response = requests.post(server_url, files=files, params=params)
    
    if response.status_code == 200:
        result = response.json()
        predictions = result['predictions']
        class_names = result['class_names']
        performance = result['performance']
        
        # Draw bounding boxes
        for detection in predictions:
            class_id = int(detection[5])
            confidence = detection[4]
            bbox = detection[:4]
            
            x1, y1, x2, y2 = bbox
            x1 = int(x1 * frame.shape[1])
            y1 = int(y1 * frame.shape[0])
            x2 = int(x2 * frame.shape[1])
            y2 = int(y2 * frame.shape[0])
            
            label = f'{class_names[class_id]} {confidence:.2f}'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Add performance metrics to the frame
        cv2.putText(frame, f"Inference: {performance['inference_time']:.3f}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Total: {processing_time:.3f}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"CPU: {performance['cpu_usage']:.1f}%", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"RAM: {performance['ram_usage']:.1f}%", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame, predictions
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return frame, None

def run_inference_on_video(video_path, output_path, server_url, model=None, confidence=0.5, skip_frames=2):
    print(f"Running inference on video: {video_path}")
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    print(f"Video properties: {frame_width}x{frame_height} @ {fps}fps")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps // (skip_frames + 1), (frame_width, frame_height))

    frame_count = 0
    fps_queue = deque(maxlen=30)  # Store last 30 frame processing times
    heatmap = np.zeros((frame_height, frame_width), dtype=np.float32)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("End of video reached")
            break

        frame_count += 1
        if frame_count % (skip_frames + 1) != 0:
            continue

        start_time = time.time()
        frame, predictions = process_frame(frame, server_url, model, confidence)
        
        # Update heatmap
        if predictions:
            for detection in predictions:
                x1, y1, x2, y2 = detection[:4]
                x1 = int(x1 * frame_width)
                y1 = int(y1 * frame_height)
                x2 = int(x2 * frame_width)
                y2 = int(y2 * frame_height)
                heatmap[y1:y2, x1:x2] += 1

        end_time = time.time()
        fps_queue.append(1 / (end_time - start_time))
        avg_fps = sum(fps_queue) / len(fps_queue)

        cv2.putText(frame, f"FPS: {avg_fps:.2f}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        out.write(frame)

        cv2.imshow('Object Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("User interrupted")
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Output video saved to {output_path}")

    # Normalize and save heatmap
    heatmap_normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap_color = cv2.applyColorMap(heatmap_normalized.astype(np.uint8), cv2.COLORMAP_JET)
    cv2.imwrite("heatmap.png", heatmap_color)
    print("Heatmap saved as heatmap.png")

def get_available_models(server_url):
    response = requests.get(f"{server_url}/models")
    if response.status_code == 200:
        return response.json()['models']
    else:
        print(f"Error fetching models: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run enhanced object detection on video')
    parser.add_argument('--input-path', required=True, help='Path to the input video file')
    parser.add_argument('--output-path', required=True, help='Path to save the output video')
    parser.add_argument('--skip-frames', type=int, default=2, help='Number of frames to skip between detections')
    parser.add_argument('--server-url', default='http://localhost:8000/predict', help='Base URL of the model server')
    parser.add_argument('--model', help='Name of the model to use (if multiple models are loaded)')
    parser.add_argument('--confidence', type=float, default=0.5, help='Confidence threshold for detections')
    args = parser.parse_args()

    print(f"Input path: {args.input_path}")
    print(f"Output path: {args.output_path}")
    print(f"Skip frames: {args.skip_frames}")
    print(f"Server URL: {args.server_url}")
    print(f"Confidence threshold: {args.confidence}")

    available_models = get_available_models(args.server_url)
    print(f"Available models: {available_models}")

    if args.model and args.model not in available_models:
        print(f"Warning: Specified model '{args.model}' is not available. Using default model.")
        args.model = None

    run_inference_on_video(args.input_path, args.output_path, f"{args.server_url}/predict", 
                           model=args.model, confidence=args.confidence, skip_frames=args.skip_frames)
"""

# enhanced_video_processor.py

import cv2
import numpy as np
import requests
import time
import argparse
from collections import deque
from location_based_alerts import LocationBasedAlerts, process_frame_with_alerts

def process_frame(frame, server_url, model=None, confidence=0.5):
    start_time = time.time()
    
    # Prepare the image for sending
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
    
    # Prepare query parameters
    params = {'confidence': confidence}
    if model:
        params['model'] = model
    
    # Send the image to the server
    response = requests.post(server_url, files=files, params=params)
    
    if response.status_code == 200:
        result = response.json()
        predictions = result['predictions']
        class_names = result['class_names']
        performance = result['performance']
        
        # Draw bounding boxes
        for detection in predictions:
            class_id = int(detection[5])
            confidence = detection[4]
            bbox = detection[:4]
            
            x1, y1, x2, y2 = bbox
            x1 = int(x1 * frame.shape[1])
            y1 = int(y1 * frame.shape[0])
            x2 = int(x2 * frame.shape[1])
            y2 = int(y2 * frame.shape[0])
            
            label = f'{class_names[class_id]} {confidence:.2f}'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Add performance metrics to the frame
        cv2.putText(frame, f"Inference: {performance['inference_time']:.3f}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Total: {processing_time:.3f}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"CPU: {performance['cpu_usage']:.1f}%", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"RAM: {performance['ram_usage']:.1f}%", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame, predictions
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return frame, None

def run_inference_on_video(video_path, output_path, server_url, model=None, confidence=0.5, skip_frames=2, alerts=None, recipient=None):
    print(f"Running inference on video: {video_path}")
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    print(f"Video properties: {frame_width}x{frame_height} @ {fps}fps")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps // (skip_frames + 1), (frame_width, frame_height))

    frame_count = 0
    fps_queue = deque(maxlen=30)  # Store last 30 frame processing times
    heatmap = np.zeros((frame_height, frame_width), dtype=np.float32)

    # Extract location from the first frame (assuming it's constant for the whole video)
    ret, first_frame = video_capture.read()
    if ret:
        cv2.imwrite("temp_first_frame.jpg", first_frame)
        location_coords = alerts.extract_location("temp_first_frame.jpg")
        if location_coords:
            lat, lon = location_coords
            address = alerts.get_address_from_coordinates(lat, lon)
            location_data = {
                "coordinates": f"{lat}, {lon}",
                "address": address
            }
        else:
            location_data = {
                "coordinates": "Unknown",
                "address": "Location data not available"
            }
    else:
        location_data = {
            "coordinates": "Unknown",
            "address": "Location data not available"
        }

    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the beginning of the video

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("End of video reached")
            break

        frame_count += 1
        if frame_count % (skip_frames + 1) != 0:
            continue

        start_time = time.time()
        frame, predictions = process_frame(frame, server_url, model, confidence)
        
        if alerts and recipient:
            frame = process_frame_with_alerts(frame, predictions, alerts, recipient, location_data)
        
        # Update heatmap
        if predictions:
            for detection in predictions:
                x1, y1, x2, y2 = detection[:4]
                x1 = int(x1 * frame_width)
                y1 = int(y1 * frame_height)
                x2 = int(x2 * frame_width)
                y2 = int(y2 * frame_height)
                heatmap[y1:y2, x1:x2] += 1

        end_time = time.time()
        fps_queue.append(1 / (end_time - start_time))
        avg_fps = sum(fps_queue) / len(fps_queue)

        cv2.putText(frame, f"FPS: {avg_fps:.2f}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        out.write(frame)

        cv2.imshow('Object Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("User interrupted")
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Output video saved to {output_path}")

    # Normalize and save heatmap
    heatmap_normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap_color = cv2.applyColorMap(heatmap_normalized.astype(np.uint8), cv2.COLORMAP_JET)
    cv2.imwrite("heatmap.png", heatmap_color)
    print("Heatmap saved as heatmap.png")

def get_available_models(server_url):
    response = requests.get(f"{server_url}/models")
    if response.status_code == 200:
        return response.json()['models']
    else:
        print(f"Error fetching models: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run enhanced object detection on video')
    parser.add_argument('--input-path', required=True, help='Path to the input video file')
    parser.add_argument('--output-path', required=True, help='Path to save the output video')
    parser.add_argument('--skip-frames', type=int, default=2, help='Number of frames to skip between detections')
    parser.add_argument('--server-url', default='http://localhost:8000/predict', help='Base URL of the model server')
    parser.add_argument('--model', help='Name of the model to use (if multiple models are loaded)')
    parser.add_argument('--confidence', type=float, default=0.5, help='Confidence threshold for detections')
    parser.add_argument('--enable-alerts', action='store_true', help='Enable email alerts')
    parser.add_argument('--recipient-email', help='Email address to send alerts to')
    args = parser.parse_args()

    print(f"Input path: {args.input_path}")
    print(f"Output path: {args.output_path}")
    print(f"Skip frames: {args.skip_frames}")
    print(f"Server URL: {args.server_url}")
    print(f"Confidence threshold: {args.confidence}")

    available_models = get_available_models(args.server_url)
    print(f"Available models: {available_models}")

    if args.model and args.model not in available_models:
        print(f"Warning: Specified model '{args.model}' is not available. Using default model.")
        args.model = None

    alerts = None
    if args.enable_alerts and args.recipient_email:
        alerts = LocationBasedAlerts(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            sender_email="your_email@gmail.com",
            sender_password="your_app_password"
        )

    run_inference_on_video(args.input_path, args.output_path, f"{args.server_url}/predict", 
                           model=args.model, confidence=args.confidence, skip_frames=args.skip_frames,
                           alerts=alerts, recipient=args.recipient_email)
import cv2
import numpy as np
import requests
import time
import argparse

def process_frame(frame, server_url):
    start_time = time.time()
    
    # Prepare the image for sending
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
    
    # Send the image to the server
    response = requests.post(server_url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        predictions = np.array(result['predictions'])
        class_names = result['class_names']
        
        # Draw bounding boxes
        for detection in predictions[0]:
            if detection[4] > 0.5:  # Confidence threshold
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
        print(f"Frame processed in {processing_time:.4f} seconds")
        
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    return frame

def run_inference_on_video(video_path, output_path, server_url, skip_frames=2):
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
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("End of video reached")
            break

        frame_count += 1
        if frame_count % (skip_frames + 1) != 0:
            continue

        frame = process_frame(frame, server_url)
        out.write(frame)

        cv2.imshow('Object Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("User interrupted")
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Output video saved to {output_path}")

def run_inference_on_webcam(output_path, server_url, skip_frames=2):
    print("Starting webcam inference")
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open webcam")
        return

    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    print(f"Webcam properties: {frame_width}x{frame_height} @ {fps}fps")

    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps // (skip_frames + 1), (frame_width, frame_height))

    frame_count = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error reading from webcam")
            break

        frame_count += 1
        if frame_count % (skip_frames + 1) != 0:
            continue

        frame = process_frame(frame, server_url)

        if output_path:
            out.write(frame)

        cv2.imshow('Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("User interrupted")
            break

    video_capture.release()
    
    if output_path:
        out.release()
        
    cv2.destroyAllWindows()
    
    if output_path:
        print(f"Output video saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run object detection on video or webcam')
    parser.add_argument('--input-type', choices=['video', 'webcam'], required=True, help='Input type (video or webcam)')
    parser.add_argument('--input-path', help='Path to the input video file')
    parser.add_argument('--output-path', required=True, help='Path to save the output video')
    parser.add_argument('--skip-frames', type=int, default=2, help='Number of frames to skip between detections')
    parser.add_argument('--server-url', default='http://localhost:8000/predict', help='URL of the model server')
    args = parser.parse_args()

    print(f"Input type: {args.input_type}")
    print(f"Input path: {args.input_path}")
    print(f"Output path: {args.output_path}")
    print(f"Skip frames: {args.skip_frames}")
    print(f"Server URL: {args.server_url}")

    if args.input_type == 'video':
        run_inference_on_video(args.input_path, args.output_path, args.server_url, skip_frames=args.skip_frames)
    elif args.input_type == 'webcam':
        run_inference_on_webcam(args.output_path, args.server_url, skip_frames=args.skip_frames)

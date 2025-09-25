from flask import Flask, render_template, Response, request
import cv2
from enhanced_video_processor import process_frame

app = Flask(__name__)

video_capture = None
server_url = "http://localhost:8000/predict"
current_model = None
confidence_threshold = 0.5

def gen_frames():
    global video_capture, server_url, current_model, confidence_threshold
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            frame, _ = process_frame(frame, server_url, model=current_model, confidence=confidence_threshold)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_model', methods=['POST'])
def set_model():
    global current_model
    current_model = request.form['model']
    return f"Model set to {current_model}"

@app.route('/set_confidence', methods=['POST'])
def set_confidence():
    global confidence_threshold
    confidence_threshold = float(request.form['confidence'])
    return f"Confidence threshold set to {confidence_threshold}"

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run web interface for object detection')
    parser.add_argument('--input', required=True, help='Path to input video file or camera index')
    parser.add_argument('--server-url', default='http://localhost:8000', help='URL of the model server')
    args = parser.parse_args()

    if args.input.isdigit():
        video_capture = cv2.VideoCapture(int(args.input))
    else:
        video_capture = cv2.VideoCapture(args.input)

    server_url = f"{args.server_url}/predict"

    app.run(debug=True)

### Installation steps

```bash
pip3 install fastapi uvicorn onnxruntime opencv-python numpy requests
```

### Start the Server

```bash
python3 model_server.py --weights yolov10m.onnx --class-names class.json --port 8000
```

### Run Inference on a Video

```bash
python3 video_processor.py --input-type video --input-path path/to/video.mp4 --output-path output.mp4 --server-url http://localhost:8000/predict
```

### Run Inference on Webcam

```bash
python3 video_processor.py --input-type webcam --output-path output.mp4 --server-url http://localhost:8000/predict
```

---

### Using the Enhanced Model Server

Start the enhanced model server:

```bash
python3 enhanced_model_server.py --weights path/to/weights.onnx --class-names path/to/class_names.json --model-name my_model --port 8000
```

Run the enhanced video processor:

```bash
python3 enhanced_video_processor.py --input-path path/to/video.mp4 --output-path output.mp4 --server-url http://localhost:8000/predict --model my_model --confidence 0.6
```

---

### Using the Web Interface

Install Flask:

```bash
pip3 install flask
```

Run the web interface:

```bash
python3 web_interface.py --input path/to/video.mp4 --server-url http://localhost:8000
```

Open a web browser and go to:

```
http://localhost:5000
```

---

### Using the Alert System

Install required libraries:

```bash
pip3 install geopy Pillow
```

Set up an email account for sending alerts. If using Gmail, you'll need to create an **"App Password"** for security. Modify the main section of the script with your SMTP server details and recipient email address.

To integrate this system with your existing object detection pipeline, call the `process_frame_with_alerts` function instead of (or in addition to) your current frame processing function.

#### Integrate with Your Existing Code

Import the necessary components in your main script:

```python
from location_alerts import LocationBasedAlerts, process_frame_with_alerts
```

Initialize the `AlertSystem` in your main function:

```python
alerts = LocationBasedAlerts(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    sender_email="your_email@gmail.com",
    sender_password="your_app_password"
)
```

Modify your frame processing loop to use `process_frame_with_alerts`:

```python
# Inside your video processing loop
location_data = "Current location info"  # Implement this based on your setup
frame = process_frame_with_alerts(
    frame, predictions, class_names, alerts,
    recipient="recipient@example.com", location_data=location_data
)
```

---

### Using the Updated Code

When running the script, you can now enable alerts and specify a recipient email like this:

```bash
python3 enhanced_video_processor.py --input-path your_video.mp4 --output-path output.mp4 --enable-alerts --recipient-email user@example.com
```

Make sure to replace the SMTP server details and sender email/password in the `LocationBasedAlerts` initialization with your actual email server details.

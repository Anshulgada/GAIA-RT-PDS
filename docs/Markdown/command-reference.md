# 📖 Command Reference

## **`image` - Process Single Image**

```powershell
uv run pothole-detector.py image [OPTIONS]

Options:
  -m, --model TEXT           Path to YOLO model weights (.pt file) [required]
  -i, --input TEXT           Path to input image [required]
  -o, --output TEXT          Path to output image [required]
  -c, --confidence FLOAT     Detection confidence threshold [default: 0.5]
  -s, --sender-email TEXT    Sender email address for alerts
  -r, --recipients TEXT      Recipient email addresses (space-separated string). Default: "anshulgada02@gmail.com"
  -ea, --enable-alerts       Enable email alerts for detections
```

## **`video` - Process Video File**

```powershell
uv run pothole-detector.py video [OPTIONS]

Options:
  -m, --model TEXT           Path to YOLO model weights (.pt file) [required]
  -i, --input TEXT           Path to input video [required]
  -o, --output TEXT          Path to output video [required]
  -c, --confidence FLOAT     Detection confidence threshold [default: 0.5]
  -f, --frame-skip INTEGER   Number of frames to skip between processing [default: 2]
  -s, --sender-email TEXT    Sender email address for alerts
  -r, --recipients TEXT      Recipient email addresses (space-separated). Default: "anshulgada02@gmail.com"
  -ea, --enable-alerts       Enable email alerts for detections
```

## **`webcam` - Live Camera Detection**

```powershell
uv run pothole-detector.py webcam [OPTIONS]

Options:
  -m, --model TEXT           Path to YOLO model weights (.pt file) [required]
  -o, --output TEXT          Path to save recorded video (optional)
  -c, --confidence FLOAT     Detection confidence threshold [default: 0.5]
  -f, --frame-skip INTEGER   Number of frames to skip between processing [default: 2]
  --camera INTEGER           Camera index [default: 0]
```

## **`test` - System Validation**

```powershell
uv run pothole-detector.py test [OPTIONS]

Options:
  -m, --model TEXT           Path to YOLO model weights (.pt file) [required]
  --test-image TEXT          Path to test image (optional)
```

## **`setup` - Gmail API Configuration**

```powershell
uv run pothole-detector.py setup
```

## **`download` - Download YOLOv10 base models**

```powershell
uv run pothole-detector.py download -md n s m -o models/

Options:
  -md, --model-download    Model variants to download (choices: n s m b l x). Provide one or more space-separated.
  -o, --output-dir         Directory to save downloaded model weights (default: models/)
```

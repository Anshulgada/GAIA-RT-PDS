# 🔧 Basic Usage

```powershell
# Test your model
uv run pothole-detector.py test --model best.pt --test-image sample.jpg

# Process single image with no alerts
uv run pothole-detector.py image \
  --model best.pt \
  --input photo.jpg \
  --output result.jpg

# Process video with alerts (requires sender email when using --enable-alerts)
uv run pothole-detector.py video \
  --model best.pt \
  --input video.mp4 \
  --output result.mp4 \
  --enable-alerts \
  --sender-email your-email@gmail.com

# Process with custom recipients (space-separated list)
uv run pothole-detector.py image \
  --model best.pt \
  --input photo.jpg \
  --output result.jpg \
  --enable-alerts \
  --sender-email your-email@gmail.com \
  --recipients "maintenance@city.gov supervisor@city.gov"

# Live webcam detection (optionally save to file with --output)
uv run pothole-detector.py webcam --model best.pt --camera 0 --output monitoring.mp4

# Download base YOLOv10 models (variants: n s m b l x)
uv run pothole-detector.py download -md n s m -o models/
```

# **Advanced Usage Examples**

## **High-Performance Video Processing**

```powershell
# Process 4K video with optimized settings
uv run pothole-detector.py video \
  --model best.pt \
  --input 4k_dashcam.mp4 \
  --output processed_4k.mp4 \
  --frame-skip 5 \
  --confidence 0.7
```

## **Multi-Recipient Alert System**

```powershell
# Send alerts to multiple stakeholders
uv run pothole-detector.py image \
  --model best.pt \
  --input street_photo.jpg \
  --output detection_result.jpg \
  --enable-alerts \
  --sender-email monitoring@city.gov \
  --recipients maintenance@city.gov supervisor@city.gov contractor@repairs.com

# Or use the default recipient (anshulgada02@gmail.com)
python pothole-detector.py image \
  --model best.pt \
  --input street_photo.jpg \
  --output detection_result.jpg \
  --enable-alerts \
  --sender-email monitoring@city.gov
```

## **Continuous Monitoring Setup**

```powershell
# Live monitoring with recording (PowerShell-friendly)
uv run pothole-detector.py webcam \
  --model best.pt \
  --output monitoring.mp4 \
  --confidence 0.6 \
  --frame-skip 3 \
  --camera 0
```

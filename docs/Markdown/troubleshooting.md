# 🐛 Troubleshooting

## Common Issues and Solutions

### Model Loading Errors

```bash
# Error: "Model file not found"
Solution: Check file path and permissions
python pothole-detector.py test --model /full/path/to/best.pt

# Error: "CUDA out of memory"
Solution: Reduce batch size or use CPU
export CUDA_VISIBLE_DEVICES=""
```

### Camera Issues

```bash
# Error: "Could not open camera"
Solutions:
1. Check camera permissions
2. Try different camera index (0, 1, 2...)
3. Verify camera is not in use by other applications

# List available cameras (Linux)
ls /dev/video*

# Test camera (Windows)
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```

### Gmail API Issues

```bash
# Error: "credentials.json not found"
Solution: Download OAuth2 credentials from Google Cloud Console

# Error: "Authentication failed"
Solutions:
1. Delete token.pickle and re-authenticate
2. Check Gmail API is enabled in Google Cloud Console
3. Verify OAuth2 consent screen is configured

# Using default recipient (anshulgada02@gmail.com)
Info: The system automatically uses anshulgada02@gmail.com as recipient when:
- --enable-alerts is used without --recipients
- Only --sender-email is provided for alerts
- To use different recipients, specify --recipients custom@example.com
```

### GPS Extraction Issues

```bash
# No GPS data found
Solutions:
1. Check if image has EXIF data: exiftool image.jpg
2. Ensure location services were enabled when photo was taken
3. Try with different image format (JPEG recommended)

# Video metadata issues
Solutions:
1. Install ffmpeg: sudo apt install ffmpeg
2. Check video has GPS metadata: ffprobe -show_format video.mp4
3. Re-record with GPS-enabled device
```

## Performance Tuning

### For Low-End Hardware

```bash
python pothole-detector.py video \
  --model best.pt \
  --input video.mp4 \
  --output result.mp4 \
  --frame-skip 10 \
  --confidence 0.7
```

### For High-End Hardware

```bash
python pothole-detector.py video \
  --model best.pt \
  --input 4k_video.mp4 \
  --output 4k_result.mp4 \
  --frame-skip 1 \
  --confidence 0.3
```

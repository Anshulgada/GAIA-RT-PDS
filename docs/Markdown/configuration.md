# 🔧 Configuration

## **Model Requirements**

- **Supported Formats**: PyTorch (.pt), ONNX (.onnx)
- **Recommended**: YOLOv8 or YOLOv10 models trained on pothole datasets
- **Classes**: Model should detect 'pothole' or 'ph' class

The repository includes several YOLOv10 variant weights in `models/` (for example `yolov10n.pt`, `yolov10s.pt`, `yolov10m.pt`, `yolov10b.pt`, `yolov10l.pt`, and `yolov10x.pt`). Choose the variant that matches your deployment constraints (speed vs accuracy).
You can also train your own custom model using Ultralytics YOLOv8/YOLOv10 training pipelines.

## **Gmail API Setup**

1. **Google Cloud Console Setup**:

   ```
   1. Go to https://console.cloud.google.com/
   2. Create new project: "Pothole Detection System"
   3. Enable Gmail API in API Library
   4. Create credentials → OAuth 2.0 Client ID
   5. Application type: Desktop application
   6. Download credentials.json
   ```

2. **Authentication Flow**:

```powershell
 uv run pothole-detector.py setup
```

- Browser will open for Google authentication
- Grant permissions to send emails
- Credentials saved securely in token.pickle

## **GPS Data Requirements**

### **For Images**:

- EXIF data with GPS coordinates
- Supported formats: JPEG with GPS tags
- Camera apps that embed location data

### **For Videos**:

- Metadata with location tags
- Supported formats: MP4, MOV with GPS metadata
- Dash cameras or mobile apps with GPS logging

## **Camera Configuration**

```python
# Default camera indices
0  # Primary camera (laptop webcam)
1  # Secondary camera (external USB)
2+ # Additional cameras
```

# 🎯 Use Cases (how the CLI maps)

- **Municipal infrastructure monitoring**

  - Use the `video` command to process patrol footage and optionally enable email alerts to notify maintenance teams. Reverse geocoding adds addresses to alerts when GPS is present.

- **Insurance claim processing**

  - Use the `image` command to analyze claim photos at a higher confidence threshold to reduce false positives; save annotated output for reports.

- **Research and data collection**

  - Use the `video` command with low frame-skip for dense sampling; extract GPS if available and correlate with detections for mapping/analysis.

- **Fleet management / live monitoring**
  - Use the `webcam` command to run continuous inference from a dashcam feed and optionally record the annotated stream to disk.

**Quick `uv` one-liners:**

```powershell
# Municipal (video with alerts to defaults)
uv run pothole-detector.py video -m best.pt -i patrol.mp4 -o out.mp4 -ea -s city-bot@example.com

# Insurance (image, higher confidence)
uv run pothole-detector.py image -m best.pt -i claim.jpg -o claim_annotated.jpg -c 0.7

# Research (dense sampling)
uv run pothole-detector.py video -m best.pt -i street.mp4 -o street_dense.mp4 -f 1 -c 0.4

# Fleet/live (webcam, record)
uv run pothole-detector.py webcam -m best.pt -o fleet.mp4 -f 3 -c 0.6 --camera 0
```

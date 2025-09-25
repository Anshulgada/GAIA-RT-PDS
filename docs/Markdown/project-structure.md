# Project structure

Below is a detailed top-level view of the repository with primary folders and files.

```
GAIA - Real Time Pothole Detection System/
├── .github/
├── assets/
│   ├── GAIA Logo.png
│   └── GAIA-Logo-Banner-4096-1876.png
├── docs/
│   ├── Markdown/
│   │   ├── acknowledgments.md
│   │   ├── architecture.md
│   │   ├── command-reference.md
│   │   ├── configuration.md
│   │   ├── contributing.md
│   │   ├── default-email-config.md
│   │   ├── dependencies.md
│   │   ├── downloading-models.md
│   │   ├── features.md
│   │   ├── gmail-setup.md
│   │   ├── installation.md
│   │   ├── license.md
│   │   ├── performance.md
│   │   ├── project-background.md
│   │   ├── project-structure.md
│   │   ├── support.md
│   │   ├── technical-details.md
│   │   ├── troubleshooting.md
│   │   ├── usage.md
│   │   ├── use-cases.md
│   │   └── windows-quickstart.md
│   ├── Other/
│   │   ├── GAIA Post Project PPT.pptx
│   │   ├── GAIA Startup Device (Pitch).pptx
│   │   ├── Internal Presentation (6th Sem).pptx
│   │   └── SRS.docx
│   ├── PDFs/
│   │   ├── GAIA Post Project PPT.pdf
│   │   ├── GAIA Project Report.pdf
│   │   ├── GAIA Startup Device (Pitch).pdf
│   │   ├── Internal Presentation (6th Sem).pdf
│   │   ├── NV Jetson Nano Developer Kit User Guide.pdf
│   │   ├── Research Paper.pdf
│   │   ├── SRS Template.pdf
│   │   └── SRS.pdf
│   └── Research Papers/
│       ├── Applications of Artificial Intelligence Enhanced Drones in Pothole Detection.pdf
│       ├── Detecting Potholes using Simple Image Processing Techniques and Real World Footage.pdf
│       ├── Detection and Segmentation of Cement Concrete Pavement.pdf
│       ├── Detection of Pothole by Image Processing Using UAV.pdf
│       ├── Detection of Potholes on Roads using a Drone.pdf
│       ├── Pothole Detection using UltraSonic Sensors.pdf
│       └── Pothole Detection with Image Processing and Spectral Clustering.pdf
├── models/
│   ├── yolov10b.pt
│   ├── yolov10l.pt
│   ├── yolov10m.pt
│   ├── yolov10n.pt
│   ├── yolov10s.pt
│   └── yolov10x.pt
├── Previous Code Iterations/
│   ├── additional-code.py
│   ├── app.py
│   ├── cmds.txt
│   ├── enhanced_model_server.py
│   ├── enhanced_video_processor.py
│   ├── export.py
│   ├── Final-inference-code (modified).py
│   ├── Final-inference-code-mod-2.py
│   ├── Final-inference-code-mod-3.py
│   ├── Final-inference-code-mod.py
│   ├── Final-inference-code.py
│   ├── live-old.py
│   ├── live.py
│   ├── location_based_alerts.py
│   ├── model_server.py
│   ├── steps.md
│   ├── test-vid-geo.py
│   ├── video_processor.py
│   ├── web_interface.py
│   ├── yolo_class.json
│   └── Yolov10 - Other.ipynb
├── src/
│   └── pothole_detector/
│       ├── __init__.py
│       ├── cli.py
│       ├── console.py
│       ├── detector.py
│       ├── ffmpeg_utils.py
│       ├── gmail_service.py
│       ├── gps.py
│       └── location.py
├── Test-Data/
│   ├── Images/
│   │   ├── PH-Test-GT-Res.jpg
│   │   ├── PH-Test-GT.jpg
│   │   ├── PH-Test-GT2-Res.jpeg
│   │   └── PH-Test-GT2.jpeg
│   └── Videos/
│       ├── test-vid-GT-res.mov
│       ├── test-vid-GT.mov
│       ├── test-vid-with-gps-res.mp4
│       └── whatsapp-res.mp4
├── utils/
│   ├── models/
│   ├── add-geo-loc-to-img.py
│   ├── add-geo-loc-to-vid.py
│   ├── download_models.py
│   ├── hf-uploader.py
│   ├── pt-to-tflite.py
│   └── read-pickle.py
├── data.yaml
├── LICENSE
├── pothole-detector.pt
├── pothole-detector.py
├── pyproject.toml
├── README.md
├── uv.lock
└── Yolov10.ipynb
```

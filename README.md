![GAIA Logo Banner](assets/GAIA-Logo-Banner-4096-1876.png)

# 🛰️ Real Time Pothole Detection System

**GAIA (Ground Assessment and Identification Assistant)** is a real-time pothole detection system powered by YOLOv10 with GPS extraction, reverse geocoding, and optional email alerts. Use it on images, videos, or live webcam feeds.

This README is a concise overview — full details live in docs.

## 🚀 Quick Start

- Repository: https://github.com/Anshulgada/GAIA-RT-PDS
- Install with uv: [Installation](docs/Markdown/installation.md)
- Optional Gmail setup for alerts: [Gmail API Setup](docs/Markdown/gmail-setup.md)
- Run a quick test:

```powershell
uv run pothole-detector.py test --model models/yolov10n.pt
```

## 📚 Documentation

| Topic                              | Link                                                             |
| ---------------------------------- | ---------------------------------------------------------------- |
| Features                           | [features.md](docs/Markdown/features.md)                         |
| System Architecture                | [architecture.md](docs/Markdown/architecture.md)                 |
| Installation (uv)                  | [installation.md](docs/Markdown/installation.md)                 |
| Windows Quickstart                 | [windows-quickstart.md](docs/Markdown/windows-quickstart.md)     |
| Usage                              | [usage.md](docs/Markdown/usage.md)                               |
| Configuration                      | [configuration.md](docs/Markdown/configuration.md)               |
| Command Reference                  | [command-reference.md](docs/Markdown/command-reference.md)       |
| Default Email Config               | [default-email-config.md](docs/Markdown/default-email-config.md) |
| Dependencies & System Requirements | [dependencies.md](docs/Markdown/dependencies.md)                 |
| Performance                        | [performance.md](docs/Markdown/performance.md)                   |
| Use Cases                          | [use-cases.md](docs/Markdown/use-cases.md)                       |
| Technical Details                  | [technical-details.md](docs/Markdown/technical-details.md)       |
| Troubleshooting                    | [troubleshooting.md](docs/Markdown/troubleshooting.md)           |
| Downloading base YOLOv10 models    | [downloading-models.md](docs/Markdown/downloading-models.md)     |
| Contributing                       | [contributing.md](docs/Markdown/contributing.md)                 |
| License                            | [license.md](docs/Markdown/license.md)                           |
| Project Background                 | [project-background.md](docs/Markdown/project-background.md)     |
| Project Structure                  | [project-structure.md](docs/Markdown/project-structure.md)       |
| Acknowledgments                    | [acknowledgments.md](docs/Markdown/acknowledgments.md)           |
| Support                            | [support.md](docs/Markdown/support.md)                           |
| Examples                           | [examples.md](docs/Markdown/examples.md)                         |

## 🏗️ System Architecture

### Core Components

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   PotholeDetector   │    │    GPSExtractor     │    │   LocationService   │
│                     │    │                     │    │                     │
│ • Model Loading     │    │ • Image EXIF        │    │ • Reverse Geocoding │
│ • Inference Engine  │    │ • Video Metadata    │    │ • Address Lookup    │
│ • Threading System  │    │ • Coordinate Parse  │    │ • Maps Integration  │
│ • Real-time Process │    │                     │    │                     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                           │                           │
           └───────────────────────────┼───────────────────────────┘
                                       │
                            ┌─────────────────────┐
                            │    GmailService     │
                            │                     │
                            │ • OAuth2 Auth       │
                            │ • Email Composition │
                            │ • File Attachments  │
                            │ • Secure Sending    │
                            └─────────────────────┘
```

### Threading Architecture

```
Main Thread                    Inference Thread
     │                              │
     ├─ Frame Capture               │
     ├─ Display Management          │
     ├─ User Input                  │
     │                              │
Frame Queue ────────────────────────┤
     │                              ├─ Model Inference
     │                              ├─ Detection Processing
     │                              │
Result Queue ───────────────────────┘
     │
     ├─ Result Processing
     ├─ Alert Triggering
     └─ Output Generation
```

## 🖼️ Demo

### Image Test

![Test Image](Test-Data/Images/PH-Test-GT2.jpeg)

### Image Test Result

![Test Image Result](Test-Data/Images/PH-Test-GT2-Res.jpeg)

These examples demonstrate the system's ability to detect and annotate potholes in real-world scenarios.

## 📓 Jupyter Notebook

The notebook `Yolov10.ipynb` was used for training the YOLOv10 model included in this project. It contains the full training workflow, including data preparation, model configuration, training loops, and evaluation steps. You can review or adapt it to retrain the model, experiment with new data, or understand the training process in detail.

Open it in Google Colab or VS Code to explore or modify the training pipeline.

## 📥 Models

Base YOLOv10 variants and trained `pothole-detector.pt` are mirrored here:
https://huggingface.co/datasets/Anshulgada/RT-PDS

The full dataset (50k images and labels each) is available as `Yolo.zip` in the same Hugging Face repo.

### Dataset Structure

The dataset follows standard YOLO format:

```
Yolo/
├── Inference Images/        # Example images for quick testing
└── Datasets/
     ├── train/
     │   ├── images/         # ~38k training images
     │   └── labels/
     ├── test/
     │    ├── images/        # 10k test images
     │    └── labels/
     └── valid/
         ├── images/         # 6k validation images
         └── labels/
```

## Project structure

Below is a brief top-level view of the repository with primary folders and files.
For a detailed view check [Project Structure](docs/Markdown/project-structure.md)

```
GAIA - Real Time Pothole Detection System/
├── .github/
├── docs/
│   ├── Markdown/
│   ├── Other/
│   ├── PDFs/
│   └── Research Papers/
├── Previous Code Iterations/
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
│   └── Videos/
├── utils/
├── data.yaml
├── GAIA Logo.png
├── LICENSE
├── pothole-detector.pt
├── pothole-detector.py
├── pyproject.toml
├── README copy.md
├── README.md
├── uv.lock
└── Yolov10.ipynb
```

## 📄 License

This project is licensed under the [MIT LICENSE](LICENSE).

### Happy Pothole Hunting! 🕳️🔍

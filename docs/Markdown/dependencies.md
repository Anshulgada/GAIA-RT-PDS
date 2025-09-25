# 📦 Dependencies and system requirements

Managed via uv (declared in `pyproject.toml` / `uv.lock`):

## Core Dependencies

```txt
ultralytics>=8.0.0          # YOLO model support
opencv-python>=4.5.0        # Computer vision processing
pillow>=8.0.0              # Image processing
numpy>=1.21.0              # Numerical operations
click>=8.0.0               # Modern CLI framework
rich>=12.0.0               # Beautiful terminal output
```

## GPS & Location Services

```txt
piexif>=1.1.3              # EXIF data extraction
geopy>=2.2.0               # Reverse geocoding
```

## Email & Authentication

```txt
google-api-python-client>=2.0.0    # Gmail API
google-auth-oauthlib>=0.5.0        # OAuth2 authentication
google-auth-httplib2>=0.1.0        # HTTP transport
```

## Optional Dependencies Handling

The system gracefully handles missing optional dependencies:

- **Gmail APIs**: If `google-auth-oauthlib` or `google-api-python-client` are missing, email alerts are disabled with a warning
- **Location Services**: If `geopy` is missing, reverse geocoding is disabled but GPS coordinates are still shown
- **GPS Extraction**: If `piexif` or `ffmpeg` are missing, GPS extraction fails gracefully
- **Core Functionality**: Pothole detection works without any optional dependencies

**Minimal Installation** (detection only):

```powershell
uv add ultralytics opencv-python pillow click rich numpy
```

## System Requirements

**FFmpeg**

```txt
- Required for video metadata extraction and some processing

- Install via OS package manager (winget/choco/apt/brew); not via pip/uv
```

### Windows

Download commands at `https://www.gyan.dev/ffmpeg/builds/`

```powershell
winget install FFmpeg
# or
choco install ffmpeg-full -y
```

### Ubuntu/Debian

`sudo apt update ; sudo apt install ffmpeg`

### macOS

`brew install ffmpeg`

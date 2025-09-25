# 🌟 Features

The project was originally targeted drone-based capture where drones transmit imagery and telemetry to a cloud server that runs the AI model (or alternatively runs on Jetson-class devices at the edge). The project also explored vehicle-mounted deployments, depth estimation via stereo vision or LiDAR, and Jetson-class GPU acceleration for embedded, real-time inference.

## 🔍 Multi-Modal Detection

- **Image Processing**: Single image analysis with bounding box visualization
- **Video Processing**: Batch video processing with optimized frame skipping
- **Live Webcam**: Real-time detection with live camera feeds
- **High Performance**: Multithreaded inference for smooth real-time processing

## 📍 Advanced Location Services

- **GPS Extraction**: Automatic GPS coordinate extraction from image EXIF and video metadata
- **Reverse Geocoding**: Convert coordinates to human-readable street addresses
- **Google Maps Integration**: Direct links to detected pothole locations
- **Location-Based Alerts**: Context-aware notifications with precise location data

## 📧 Intelligent Alert System

- **Gmail API Integration**: Secure OAuth2 authentication (no password storage)
- **Rich Email Notifications**: Detailed alerts with GPS coordinates, addresses, and map links
- **File Attachments**: Automatic attachment of input and processed output files
- **Customizable Recipients**: Support for multiple email recipients

## 🎨 Modern User Experience

- **Beautiful CLI**: Rich terminal interface with colors, progress bars, and tables
- **Intuitive Commands**: Simple, verb-based command structure
- **Comprehensive Testing**: Built-in system validation and diagnostics
- **Error Handling**: Graceful error handling with helpful messages
- **Default Configuration**: Pre-configured with anshulgada02@gmail.com as default recipient
- **Optional Dependencies**: Graceful fallback when optional libraries are missing

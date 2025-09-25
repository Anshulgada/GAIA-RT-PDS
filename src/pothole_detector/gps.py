from typing import Optional, Tuple
from PIL import Image
import piexif
import json
import subprocess
from .ffmpeg_utils import check_and_install_ffmpeg
from .console import console


class GPSExtractor:
    """Handle GPS data extraction from images and videos."""

    @staticmethod
    def from_image(image_path: str) -> Optional[Tuple[float, float]]:
        """Extract GPS coordinates from image EXIF data."""
        try:
            with Image.open(image_path) as img:
                if not hasattr(img, "_getexif"):
                    return None

                exif_data = img._getexif()
                if not exif_data:
                    return None

                if hasattr(img, "info") and "exif" in img.info:
                    try:
                        exif_dict = piexif.load(img.info["exif"])
                        gps_data = exif_dict.get("GPS", {})

                        if (
                            piexif.GPSIFD.GPSLatitude in gps_data
                            and piexif.GPSIFD.GPSLongitude in gps_data
                        ):
                            lat_data = gps_data[piexif.GPSIFD.GPSLatitude]
                            lon_data = gps_data[piexif.GPSIFD.GPSLongitude]
                            lat_ref = gps_data.get(piexif.GPSIFD.GPSLatitudeRef, b"N")
                            lon_ref = gps_data.get(piexif.GPSIFD.GPSLongitudeRef, b"E")

                            if isinstance(lat_ref, bytes):
                                lat_ref = lat_ref.decode()
                            if isinstance(lon_ref, bytes):
                                lon_ref = lon_ref.decode()

                            lat = sum(
                                float(num) / float(denom) for num, denom in lat_data
                            )
                            lon = sum(
                                float(num) / float(denom) for num, denom in lon_data
                            )

                            if lat_ref == "S":
                                lat = -lat
                            if lon_ref == "W":
                                lon = -lon

                            return lat, lon
                    except Exception:
                        pass

        except Exception as e:
            console.print(
                f"[yellow]Warning: Could not extract GPS from image: {e}[/yellow]"
            )

        return None

    @staticmethod
    def from_video(video_path: str) -> Optional[Tuple[float, float]]:
        """Extract GPS coordinates from video metadata."""
        if not check_and_install_ffmpeg():
            console.print(
                "[red]Error: FFmpeg is required but could not be installed automatically.[/red]"
            )
            console.print(
                "[yellow]Please install FFmpeg manually and try again.[/yellow]"
            )
            return None

        try:
            cmd = [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format_tags=location",
                "-of",
                "json",
                video_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                metadata = json.loads(result.stdout)
                tags = metadata.get("format", {}).get("tags", {})

                if "location" in tags:
                    coords = tags["location"].split(",")
                    if len(coords) == 2:
                        return float(coords[0].strip()), float(coords[1].strip())

        except Exception as e:
            console.print(
                f"[yellow]Warning: Could not extract GPS from video: {e}[/yellow]"
            )

        return None

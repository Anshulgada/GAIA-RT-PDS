import os
import sys
import time

from .console import console
from .detector import PotholeDetector
from .gmail_service import GmailService
from .location import LocationService
from .gps import GPSExtractor
from utils.download_models import download_models

import rich_click as click
from rich.table import Table
from rich.panel import Panel

# Enable rich-click globally
click.rich_click.MAX_WIDTH = 120
click.rich_click.STYLE_HELPTEXT = "dim"
click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_SWITCH = "bold green"
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.SHOW_METAVARS_COLUMN = True
click.rich_click.SHOW_VERSION = True

# --- Enable -h as alias for --help globally ---
if "-h" in sys.argv:
    sys.argv[sys.argv.index("-h")] = "--help"


@click.group(invoke_without_command=True)
@click.version_option(version="1.0.0")
@click.pass_context
def cli(ctx):
    """🚨 Unified Pothole Detection System"""
    # Always show the panel
    console.print(
        Panel.fit(
            "[bold blue]Pothole Detection System[/bold blue]\n"
            "[dim]Real-time ML inference with GPS tracking and smart email alerts[/dim]",
            border_style="blue",
        )
    )

    # If no subcommand or --help, also show help text
    if ctx.invoked_subcommand is None and not ctx.args:
        click.echo(ctx.get_help())


@cli.command()
@click.option(
    "--model-download",
    "-md",
    type=click.Choice([" n ", " s ", " m ", " b ", " l ", " x "]),
    multiple=True,
    required=False,
    help="Download one or more YOLOv10 model(s) variant (e.g. -md n s m) [Base Model to be trained on custom dataset]",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    default="models/",
    show_default=True,
    help="Directory to save downloaded model weights",
)
def download(model_download, output_dir):
    """Download YOLOv10 model weights (Base Models to be trained on custom dataset)"""
    click.echo(" Starting model download...\n")
    download_models(variants=model_download, output_dir=output_dir)



@cli.command()
@click.option(
    "--model", "-m", required=True, help="Path to YOLO model weights (.pt file)"
)
@click.option("--input", "-i", required=True, help="Path to input image")
@click.option("--output", "-o", required=True, help="Path to output image")
@click.option(
    "--confidence",
    "-c",
    default=0.5,
    help="Detection confidence threshold (default: 0.5)",
)
@click.option("--sender-email", "-s", help="Sender email address for alerts")
@click.option(
    "--recipients",
    "-r",
    default="anshulgada02@gmail.com",
    help="Recipient email addresses (space-separated: 'email1@gmail.com email2@gmail.com') [default: anshulgada02@gmail.com]",
)
@click.option(
    "--enable-alerts", "-ea", is_flag=True, help="Enable email alerts for detections"
)
def image(model, input, output, confidence, sender_email, recipients, enable_alerts):
    """Process a single image for pothole detection."""

    # Initialize services
    gmail_service = None
    location_service = None

    if enable_alerts:
        if not sender_email:
            console.print("[red]Error: --sender-email required for alerts[/red]")
            return

        # Parse recipients (space-separated string to list)
        # Click provides a default string; convert it into a list once.
        recipients = (
            recipients.split()
            if recipients and isinstance(recipients, str)
            else (recipients or ["anshulgada02@gmail.com"])
        )

        gmail_service = GmailService()
        if not gmail_service.authenticate():
            return

        location_service = LocationService()

    # Initialize detector
    detector = PotholeDetector(
        model_path=model,
        confidence_threshold=confidence,
        gmail_service=gmail_service,
        location_service=location_service,
    )

    if not detector.load_model():
        return

    try:
        # Process image
        result = detector.process_image(
            input_path=input,
            output_path=output,
            sender_email=sender_email,
            recipient_emails=list(recipients),
        )

        # Display results
        table = Table(title="Processing Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Input", input)
        table.add_row("Output", output)
        table.add_row("Inference Time", f"{result['inference_time']:.2f}s")
        table.add_row(
            "Pothole Detected",
            "[red]Yes[/red]" if result["pothole_detected"] else "[green]No[/green]",
        )

        console.print(table)

        if result["pothole_detected"]:
            console.print("[red]⚠️  POTHOLE DETECTED![/red]")

    except Exception as e:
        console.print(f"[red]Error processing image: {e}[/red]")


@cli.command()
@click.option(
    "--model", "-m", required=True, help="Path to YOLO model weights (.pt file)"
)
@click.option("--input", "-i", required=True, help="Path to input video")
@click.option("--output", "-o", required=True, help="Path to output video")
@click.option(
    "--confidence",
    "-c",
    default=0.5,
    help="Detection confidence threshold (default: 0.5)",
)
@click.option(
    "--frame-skip",
    "-f",
    default=2,
    help="Number of frames to skip between processing (default: 2)",
)
@click.option("--sender-email", "-s", help="Sender email address for alerts")
@click.option(
    "--recipients",
    "-r",
    default="anshulgada02@gmail.com",
    help="Recipient email addresses (space-separated: 'email1@gmail.com email2@gmail.com') [default: anshulgada02@gmail.com]",
)
@click.option(
    "--enable-alerts", "-ea", is_flag=True, help="Enable email alerts for detections"
)
def video(
    model,
    input,
    output,
    confidence,
    frame_skip,
    sender_email,
    recipients,
    enable_alerts,
):
    """Process a video file for pothole detection."""

    # Initialize services
    gmail_service = None
    location_service = None

    if enable_alerts:
        if not sender_email:
            console.print("[red]Error: --sender-email required for alerts[/red]")
            return

        # Parse recipients (space-separated string to list)
        recipients = (
            recipients.split()
            if recipients and isinstance(recipients, str)
            else (recipients or ["anshulgada02@gmail.com"])
        )

        gmail_service = GmailService()
        if not gmail_service.authenticate():
            return

        location_service = LocationService()

    # Initialize detector
    detector = PotholeDetector(
        model_path=model,
        confidence_threshold=confidence,
        gmail_service=gmail_service,
        location_service=location_service,
    )

    if not detector.load_model():
        return

    try:
        # Process video
        result = detector.process_video(
            input_path=input,
            output_path=output,
            frame_skip=frame_skip,
            sender_email=sender_email,
            recipient_emails=list(recipients),
        )

        # Display results
        table = Table(title="Processing Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Input", input)
        table.add_row("Output", output)
        table.add_row("Video Duration", f"{result['video_duration']:.2f}s")
        table.add_row("Inference Time", f"{result['inference_time']:.2f}s")
        table.add_row(
            "Processing Speed",
            f"{result['video_duration'] / result['inference_time']:.1f}x real-time",
        )
        table.add_row(
            "Pothole Detected",
            "[red]Yes[/red]" if result["pothole_detected"] else "[green]No[/green]",
        )

        console.print(table)

        if result["pothole_detected"]:
            console.print("[red]⚠️  POTHOLE DETECTED![/red]")

    except Exception as e:
        console.print(f"[red]Error processing video: {e}[/red]")


@cli.command()
@click.option(
    "--model", "-m", required=True, help="Path to YOLO model weights (.pt file)"
)
@click.option("--output", "-o", help="Path to save recorded video (optional)")
@click.option(
    "--confidence",
    "-c",
    default=0.5,
    help="Detection confidence threshold (default: 0.5)",
)
@click.option(
    "--frame-skip",
    "-f",
    default=2,
    help="Number of frames to skip between processing (default: 2)",
)
@click.option("--camera", default=0, help="Camera index (default: 0)")
def webcam(model, output, confidence, frame_skip, camera):
    """Process live webcam feed for real-time pothole detection."""

    # Initialize detector (no alerts for webcam mode)
    detector = PotholeDetector(model_path=model, confidence_threshold=confidence)

    if not detector.load_model():
        return

    try:
        console.print(f"[green]Starting webcam detection (camera {camera})[/green]")
        detector.process_webcam(
            output_path=output, frame_skip=frame_skip, camera_index=camera
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Detection stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error with webcam: {e}[/red]")


@cli.command()
def setup():
    """Setup Gmail API credentials for email alerts."""

    console.print(
        Panel(
            "[bold blue]Gmail API Setup[/bold blue]\n\n"
            "1. Go to the Google Cloud Console (https://console.cloud.google.com/)\n"
            "2. Create a new project or select an existing one\n"
            "3. Enable the Gmail API\n"
            "4. Create credentials (OAuth 2.0 Client ID) for a desktop application\n"
            "5. Download the credentials file and save it as 'credentials.json'\n"
            "6. Run this command to authenticate\n\n"
            "[dim]The system will open a browser window for authentication[/dim]",
            border_style="blue",
        )
    )

    if not os.path.exists("credentials.json"):
        console.print("[red]Error: credentials.json not found![/red]")
        console.print(
            "Please download your OAuth 2.0 credentials file and save it as 'credentials.json'"
        )
        return

    gmail_service = GmailService()
    if gmail_service.authenticate():
        console.print("[green]✅ Gmail API setup complete![/green]")
        console.print("You can now use email alerts with the --enable-alerts flag")
    else:
        console.print("[red]❌ Gmail API setup failed[/red]")


@cli.command()
@click.option(
    "--model", "-m", required=True, help="Path to YOLO model weights (.pt file)"
)
@click.option("--test-image", help="Path to test image (optional)")
def test(model, test_image):
    """Test the detection system and display model information."""

    console.print("[blue]🔍 Testing Pothole Detection System[/blue]")

    # Test model loading
    detector = PotholeDetector(model_path=model, confidence_threshold=0.5)

    if not detector.load_model():
        return

    # Display model info
    table = Table(title="Model Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Model Path", model)
    table.add_row("Model Type", str(type(detector.model).__name__))
    table.add_row("Classes", str(list(detector.model.names.values())))
    table.add_row("Device", str(detector.model.device))

    console.print(table)

    # Test with image if provided
    if test_image:
        if not os.path.exists(test_image):
            console.print(f"[red]Test image not found: {test_image}[/red]")
            return

        console.print(f"\n[blue]Testing with image: {test_image}[/blue]")

        try:
            # Create temporary output path
            output_path = f"test_output_{int(time.time())}.jpg"

            result = detector.process_image(
                input_path=test_image, output_path=output_path
            )

            console.print("[green]✅ Test successful![/green]")
            console.print(f"Inference time: {result['inference_time']:.2f}s")
            console.print(
                f"Pothole detected: {'Yes' if result['pothole_detected'] else 'No'}"
            )
            console.print(f"Output saved: {output_path}")

            # Test GPS extraction
            gps_coords = GPSExtractor.from_image(test_image)
            if gps_coords:
                lat, lon = gps_coords
                console.print(f"[green]GPS found: {lat:.6f}, {lon:.6f}[/green]")

                location_service = LocationService()
                address = location_service.get_address(lat, lon)
                console.print(f"Address: {address}")
            else:
                console.print("[yellow]No GPS data found in test image[/yellow]")

        except Exception as e:
            console.print(f"[red]Test failed: {e}[/red]")

    console.print("\n[green]✅ System test complete![/green]")

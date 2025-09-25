import subprocess
import platform
from .console import console


try:
    import ffmpeg as ffmpeg_py  # type: ignore

    FFMPEG_PYTHON_AVAILABLE = True
except Exception:
    ffmpeg_py = None
    FFMPEG_PYTHON_AVAILABLE = False


def check_and_install_ffmpeg() -> bool:
    """Check if FFmpeg is available and attempt to install if missing."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, check=True, timeout=10
        )
        return True
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        pass

    if FFMPEG_PYTHON_AVAILABLE:
        try:
            ffmpeg_py.probe(
                "test", v="quiet", f="lavfi", i="testsrc2=duration=1:size=32x32:rate=1"
            )
            return True
        except Exception:
            pass

    system = platform.system().lower()
    console.print(
        "[yellow]FFmpeg not found. Attempting automatic installation...[/yellow]"
    )

    try:
        if system == "windows":
            try:
                subprocess.run(["winget", "install", "ffmpeg"], check=True, timeout=60)
                console.print("[green]✓ FFmpeg installed via winget[/green]")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    subprocess.run(
                        ["choco", "install", "ffmpeg-full", "-y"],
                        check=True,
                        timeout=120,
                    )
                    console.print("[green]✓ FFmpeg installed via chocolatey[/green]")
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass

        elif system == "darwin":
            try:
                subprocess.run(["brew", "install", "ffmpeg"], check=True, timeout=120)
                console.print("[green]✓ FFmpeg installed via homebrew[/green]")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

        elif system == "linux":
            package_managers = [
                (["apt", "update"], ["apt", "install", "-y", "ffmpeg"]),
                (["yum", "install", "-y", "ffmpeg"],),
                (["dnf", "install", "-y", "ffmpeg"],),
                (["pacman", "-S", "--noconfirm", "ffmpeg"],),
            ]

            for commands in package_managers:
                try:
                    for cmd in commands:
                        subprocess.run(cmd, check=True, timeout=120)
                    console.print(
                        "[green]✓ FFmpeg installed via system package manager[/green]"
                    )
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue

    except Exception as e:
        console.print(f"[yellow]Could not install FFmpeg automatically: {e}[/yellow]")

    console.print("[red]✗ FFmpeg installation failed[/red]")
    console.print("[yellow]Please install FFmpeg manually:[/yellow]")
    console.print("  Windows: winget install FFmpeg  or  choco install ffmpeg")
    console.print("  macOS:   brew install ffmpeg")
    console.print("  Linux:   sudo apt install ffmpeg  or  sudo yum install ffmpeg")

    return False

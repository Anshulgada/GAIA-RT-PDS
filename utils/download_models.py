import os
import requests
from rich.console import Console
from rich.progress import Progress
from huggingface_hub import hf_hub_download

console = Console()

# Default local directory to store models
LOCAL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(LOCAL_DIR, exist_ok=True)

# Model variants to download
MODEL_VARIANTS = ["n", "s", "m", "b", "l", "x"]  # yolov10n, yolov10s, etc.

# GitHub URL template for Ultralytics assets
GITHUB_URL_TEMPLATE = (
    "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov10{}.pt"
)

# Hugging Face repo (fallback)
HF_REPO = "Anshulgada/RT-PDS-Models"
HF_REPO_TYPE = "dataset"  # Important, because it's a dataset, not a model repo


def download_from_github(model_name, output_dir):
    variant = model_name.replace("yolov10", "").replace(".pt", "")
    url = GITHUB_URL_TEMPLATE.format(variant)
    local_path = os.path.join(output_dir, model_name)

    if os.path.exists(local_path):
        console.print(
            f"\n[green] ✅ {model_name} already exists in {output_dir}, skipping GitHub download.[/green]"
        )
        return True

    try:
        console.print(f"\n[cyan] ⬇️ Downloading {model_name} from GitHub...[/cyan]")
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        console.print(
            f"\n[green] ✅ Saved {model_name} from GitHub to {local_path[:-12]}[/green]\n"
        )
        return True
    except Exception as e:
        console.print(
            f"\n[yellow] ⚠️ GitHub download failed for {model_name}: {e}[/yellow]"
        )
        return False


def download_from_hf(model_name, output_dir):
    local_path = os.path.join(output_dir, model_name)

    if os.path.exists(local_path):
        console.print(
            f"\n[green] ✅ {model_name} already exists in {output_dir}, skipping HF download.[/green]"
        )
        return

    try:
        console.print(
            f"\n[cyan] ⬇️ Downloading {model_name} from Hugging Face fallback...[/cyan]"
        )
        hf_hub_download(
            repo_id=HF_REPO,
            repo_type=HF_REPO_TYPE,
            filename=model_name,
            local_dir=output_dir,
        )
        console.print(f"\n[green] ✅ Saved {model_name} from HF to {output_dir[:-12]}[/green]\n")
    except Exception as e:
        console.print(
            f"\n[red] ❌ Hugging Face download failed for {model_name}: {e}[/red]"
        )


def download_models(variants=None, output_dir: str = LOCAL_DIR):
    # Ensure output dir exists
    os.makedirs(output_dir, exist_ok=True)

    # If user passed multiple variants (-md "n s m")
    variants_to_download = list(variants) if variants else MODEL_VARIANTS

    with Progress() as progress:
        task = progress.add_task(
            "[blue] Downloading models...", total=len(variants_to_download)
        )
        for v in variants_to_download:
            model_name = f"yolov10{v}.pt"

            # Download from GitHub first
            success = download_from_github(model_name, output_dir)

            # If GitHub fails, fallback to HF
            if not success:
                download_from_hf(model_name, output_dir)

            # Advance the progress bar first
            progress.update(task, advance=1)

    # Force a newline after progress bar completes
    console.print(
        "\n ✅ Download completed! Saved to [bold]{0}[/bold]\n".format(output_dir)
    )


if __name__ == "__main__":
    download_models()

# 📥 Downloading base YOLOv10 models

If you want to download base YOLOv10 variants automatically, there are two ways to do it:

1. Use the built-in CLI command (recommended):

```powershell
uv run pothole-detector.py download -md n s m -o models/
```

2. Use the helper script directly: `utils/download_models.py` — this script:

- Downloads YOLOv10 base model weights (variants: `n`, `s`, `m`, `b`, `l`, `x`) into `utils/models/` by default.

- Attempts to download from a GitHub release first using a Ultralytics assets URL template.

- Falls back to the Hugging Face dataset `Anshulgada/RT-PDS` when the GitHub download fails.

- Shows progress using `rich` and uses `requests` (and `huggingface_hub.hf_hub_download` for HF fallback).

## Usage (direct):

```powershell
# From repository root
uv run utils/download_models.py

# Or import and call from Python
python -c "from utils.download_models import download_models; download_models(variants=('n','s','m'), output_dir='models/')"
```

## Notes:

- Default output directory when called directly is `utils/models/` (the script creates it if missing).

- The CLI `download` command delegates to `utils.download_models.download_models`, so both approaches are equivalent.

- The script checks if a model file already exists and skips re-downloading it.

- Dependencies for the downloader: `requests`, `rich`, and `huggingface_hub` (HF fallback).

## Hosting:

Both base YOLOv10 variants and the trained `pothole-detector.pt` are mirrored at https://huggingface.co/datasets/Anshulgada/RT-PDS

The full dataset (50k images and labels each) is available as `Yolo.zip` in the same Hugging Face repo.

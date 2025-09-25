# 🚀 Installation (uv)

Repository: https://github.com/Anshulgada/GAIA-RT-PDS

Models: Base YOLOv10 variants and the trained `pothole-detector.pt` are hosted at https://huggingface.co/datasets/Anshulgada/RT-PDS

The full dataset (50k images and labels each) is available as `Yolo.zip` in the same Hugging Face repo.

### Dataset Structure

The dataset follows standard YOLO format:

```
Yolo/
├── Inference Images/       # Example images for quick testing
└── Datasets/
	├── train/
	│   ├── images/         # ~38k training images
	│   └── labels/
	├── valid/
	│   ├── images/         # 6k validation images
	│   └── labels/
	└── test/
		├── images/         # 10k test images
		└── labels/
```

### Downloading with Python

```python
from huggingface_hub import hf_hub_download

# Download the model
model_path = hf_hub_download(
	repo_id="Anshulgada/RT-PDS",
	filename="pothole-detector.pt"
)

# Download the zipped YOLO dataset
dataset_path = hf_hub_download(
	repo_id="Anshulgada/RT-PDS",
	filename="Yolo.zip",
	repo_type="dataset"
)
```

```powershell
# Clone repository
git clone https://github.com/Anshulgada/GAIA-RT-PDS
cd GAIA-RT-PDS

# Create and activate a virtual environment (uv)
uv venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Linux/Mac

# Install project dependencies from pyproject.toml / uv.lock
uv sync

# Optional: add extras if not already declared
# uv add piexif geopy google-api-python-client google-auth-oauthlib google-auth-httplib2 rich-click huggingface_hub
```

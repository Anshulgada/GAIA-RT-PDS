from huggingface_hub import HfApi
import os

api = HfApi(token=os.getenv("HF_TOKEN"))
api.upload_large_folder(
    folder_path="Yolo/",
    repo_id="Anshulgada/RT-PDS-Dataset",
    repo_type="dataset",
)



# from huggingface_hub import HfApi

# api = HfApi(token=os.getenv("HF_TOKEN"))
# repo_id = "Anshulgada/RT-PDS-Dataset"

# folders_to_upload = [
#     "Yolo/Datasets/valid/labels",
#     "Yolo/Inference Images"
# ]

# for folder in folders_to_upload:
#     print(f"Uploading folder: {folder}")
#     api.upload_folder(
#         folder_path=folder,
#         repo_id=repo_id,
#         repo_type="dataset",
#         ignore_patterns=[".venv/*"]
#     )

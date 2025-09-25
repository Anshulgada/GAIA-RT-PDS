# 🪟 Windows Quickstart (PowerShell + uv)

```powershell
# 1) Install uv (if missing) [Suggested methods]

>  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# or by
>  pipx install uv

# or by
>  winget install --id=astral-sh.uv  -e



# 2) Clone and prepare env
>  git clone https://github.com/Anshulgada/GAIA-RT-PDS
>  cd GAIA-RT-PDS
>  uv venv
>  .venv\Scripts\activate
>  uv sync



# 3) Optional: download base models
>  uv run pothole-detector.py download -md n s -o models/



# 4) Smoke test
>  uv run pothole-detector.py test --model models/yolov10n.pt
```

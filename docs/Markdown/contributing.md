# 🤝 Contributing

## Development setup (uv)

```powershell
# Clone repository
git clone https://github.com/Anshulgada/GAIA-RT-PDS
cd GAIA-RT-PDS

# Environment
uv venv ; .venv\Scripts\activate
uv sync

# Lint (ruff)
uvx tool ruff check .
uvx tool ruff format .

# Quick sanity test (requires a model)
uv run pothole-detector.py test --model models/yolov10n.pt
```

## Guidelines

- Use feature branches and open PRs with a brief description and before/after screenshots where relevant.
- Keep changes focused; update README/docs when public behavior changes.
- Prefer adding small smoke tests for new CLI behavior (where practical).

# **📧 Default Email Configuration**

**Important**: The system uses `anshulgada02@gmail.com` as the default alert recipient. This is the project maintainer's email for demonstration purposes.

**For Production Use**:

```powershell
# Always specify your own recipients
uv run pothole-detector.py image \
  --enable-alerts \
  --sender-email your-monitoring@company.com \
  --recipients "maintenance@company.com ops@company.com"
```

- **No Recipients Required**: When using `--enable-alerts`, you only need to provide `--sender-email`.
- **Override When Needed**: Use `--recipients` to specify a space-separated list of email addresses.
- **Multiple Recipients**: Provide them as a single quoted string (PowerShell): `--recipients "a@x.com b@y.com"`.
- **Automatic Fallback**: If no recipients are specified, alerts go to the default email.

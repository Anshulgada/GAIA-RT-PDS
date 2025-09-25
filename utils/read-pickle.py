import pickle
from google.oauth2.credentials import Credentials

file_path = "src/pothole_detector/token.pickle"

try:
    with open(file_path, "rb") as f:
        creds: Credentials = pickle.load(f)

    print(creds.__dict__)

    print("\nAttributes of the Credentials object:\n")
    for attr, value in creds.__dict__.items():
        print(f"  {attr}: {value}")

    # print("Type:", type(creds))
    # print("Valid:", creds.valid)
    # print("Expired:", creds.expired)
    # print("Token:", creds.token[:20] + "..." if creds.token else None)
    # print("Refresh token:", creds.refresh_token)
    # print("Client ID:", creds.client_id)
    # print("Client Secret:", creds.client_secret)
    # print("Expiry:", creds.expiry)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred while reading the pickle file: {e}")

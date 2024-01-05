from google_auth_oauthlib.flow import InstalledAppFlow

# Set the path to the downloaded credentials JSON file
credentials_path = "client_secret_100525849490-5ur6knctcem36hubkb4stre2s9dtv909.apps.googleusercontent.com.json"

# Define the scopes for the Google Drive API
# scopes = ["https://www.googleapis.com/auth/drive.file"]
scopes = ["https://www.googleapis.com/auth/drive.file"]

# Set up the OAuth 2.0 flow
flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes=scopes)

# Run the OAuth 2.0 flow and obtain credentials
credentials = flow.run_local_server(port=8080)

# Print the access token (you'll use this for API requests)
print(f"Access Token: {credentials.token}")

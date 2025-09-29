import requests
import os
from dotenv import load_dotenv

# Replace these with your API credentials
load_dotenv()
UID = os.getenv("UID")
SECRET = os.getenv("SECRET")
TOKEN_URL = "https://api.intra.42.fr/oauth/token"

def get_access_token():
    # Prepare the payload for client credentials flow
    data = {
        'grant_type': 'client_credentials'
    }

    # Make the request to get the token
    response = requests.post(
        TOKEN_URL,
        data=data,
        auth=(UID, SECRET)
    )

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get("access_token")
        print("Access token:", access_token)
        return access_token
    else:
        print("Error obtaining token:", response.status_code, response.text)
        return None

def get_users_madrid(token):
    url = "https://api.intra.42.fr/v2/campus/11/users"
    headers = {"Authorization": f"Bearer {token}"}
    users = []

    page = 1
    while True:
        params = {"page": page, "per_page": 100}  # increase per_page for more results
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if not data or len(data) == 0:
            break
        for user in data:
            users.append((user.get('id'), user.get('login')))
        page += 1

    return users

if __name__ == "__main__":
    token = get_access_token()
    users = get_users_madrid(token)
    for uid, login in users:
        print(uid, login)

import json
import os
from pprint import pprint

import requests
from dotenv import load_dotenv

# относительный путь для примера, лучше использовать глобальный!
load_dotenv("./.env")

client_id = os.getenv("CLIENT_ID", None)
client_secret = os.getenv("CLIENT_SECRET", None)


def make_headers(token):
    return {"X-Xapp-Token": token}


def get_token(client_id, client_secret):
    # url = f"https://api.artsy.net/api/tokens/xapp_token
    # ?client_id={client_id}&client_secret={client_secret}"
    url = "https://api.artsy.net/api/tokens/xapp_token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(url, params=params)
    token_data = response.json()
    # expires??
    # token_data = json.loads(response.text)
    try:
        token = token_data["token"]
    except Exception as e:
        print(e)
        return None
    return token


def get_artist(headers, artist="andy-warhol"):
    url = "https://api.artsy.net/api/artists"
    if not (artist is None or artist == ""):
        url = f"{url}/{artist}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def save_artist_info(artist_info, path):
    with open(path, "w") as f:
        json.dump(artist_info, f)


def pipeline(client_id, client_secret, artist, path="artist.json"):
    token = get_token(client_id, client_secret)
    if token is None:
        print("Token is None!")
        return None

    headers = make_headers(token)
    artist_info = get_artist(headers, artist)
    if artist_info is None:
        print("artist_info is None")
        return None

    save_artist_info(artist_info, path)
    return artist_info


if __name__ == "__main__":
    # artist = "andy-warhol"
    artist_info = pipeline(client_id, client_secret, "")
    pprint(artist_info)
    print()

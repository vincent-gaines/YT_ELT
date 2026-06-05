import dotenv
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")   

API_KEY = os.getenv("API_KEY")

#curl \
#  'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle=%40MrBeast&key=[YOUR_API_KEY]' \
#  --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
#  --header 'Accept: application/json' \
#  --compressed
# API Key = "AIzaSyBWolftaEVUfX4pcFuekSHwBSUS49TX0rE"

CHANNEL_HANDLE = "MrBeast"
maxResults = 50

def get_playlist_id() :

    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}" 

        response = requests.get(url)

        response.raise_for_status()  # Check if the request was successful

        data = response.json()
        #print(json.dumps(data, indent=4))

        channel_items = data['items'][0]

        channel_playlistid = channel_items['contentDetails']['relatedPlaylists']['uploads']

        #print(f"Channel Playlist ID: {channel_playlistid}")
        return channel_playlistid

    except requests.exceptions.RequestException as e:
        raise e




def get_video_ids(playlistid) :

    video_ids = []

    pageToken = None

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistid}&key={API_KEY}"


    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            data = response.json()
            #print(json.dumps(data, indent=4))

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')
            if not pageToken:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlistid = get_playlist_id()
    video_ids = get_video_ids(playlistid)
    print(f"Video IDs: {video_ids}")
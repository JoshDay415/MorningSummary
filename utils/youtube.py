import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

def get_latest_video(channel_id):
    api_key = os.getenv("YOUTUBE_API_KEY")
    now = datetime.now(timezone.utc)
    twelve_hours_ago = now - timedelta(hours=12)

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": api_key,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "publishedAfter": twelve_hours_ago.isoformat(),
        "maxResults": 1,
        "type": "video"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data.get("items"):
        return None  # No new video in last 12 hours

    video = data["items"][0]
    title = video["snippet"]["title"]
    video_id = video["id"].get("videoId")

    if not video_id:
        return None

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    return f"🎥 *New video in last 12h:*\n{title}\n{video_url}"

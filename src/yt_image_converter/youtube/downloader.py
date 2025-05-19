# downloader.py
import requests
from PIL import Image
from io import BytesIO

def download_thumbnail(video_id: str) -> Image.Image:
    url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

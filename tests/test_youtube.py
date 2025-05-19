from src.yt_image_converter.youtube.downloader import extract_video_id

def test_extract_video_id():
    assert extract_video_id("https://youtube.com/watch?v=abc123") == "abc123"

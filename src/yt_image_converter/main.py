# main.py
from src.yt_image_converter.image_processing.round_img import create_rounded_image
from src.yt_image_converter.reel_creator.create_reel import create_reel
from youtube.downloader import download_thumbnail
from youtube.extractor import extract_clean_screenshot
from image_processing.effects import overlay_thumbnail

def run_pipeline(video_id, executable_path):
    print("📸 Taking screenshot...")
    box = extract_clean_screenshot(video_id, executable_path, "base.png")

    print("🖼 Downloading thumbnail...", box)
    thumb = download_thumbnail(video_id)

    print("🧩 Compositing...")
    overlay_thumbnail("base.png", thumb, box, "final_output.png")

    print("✅ Done. Saved to final_output.png")

    print("Creating rounded img...")
    create_rounded_image("final_output.png", "final_output_rounded.png", 10)

    print("Creating reel...")
    create_reel("final_output_rounded.png", "final_reel.mp4")

    print("✅ Done. Reel saved to final_reel.mp4")

run_pipeline("h9Z4oGN89MU",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

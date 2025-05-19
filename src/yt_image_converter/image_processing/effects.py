# effects.py
from PIL import Image
import numpy as np

def overlay_thumbnail(base_path: str, thumb_img: Image.Image, box: dict, output_path="final_output.png"):
    base = Image.open(base_path).convert("RGBA")
    thumb_resized = thumb_img.resize((int(box['width']), int(box['height'])))
    base.paste(thumb_resized, (int(box['x']), int(box['y'])-50))
    base.save(output_path)

# Create a horizontal gradient background (#000000 to #3533cd)
def create_linear_gradient(width, height, start_color, end_color):
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    for x in range(width):
        r = int(start_color[0] * (width - x) / width + end_color[0] * x / width)
        g = int(start_color[1] * (width - x) / width + end_color[1] * x / width)
        b = int(start_color[2] * (width - x) / width + end_color[2] * x / width)
        gradient[:, x] = [r, g, b]
    return gradient
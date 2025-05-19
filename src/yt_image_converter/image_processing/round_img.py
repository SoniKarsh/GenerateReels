# Step 1: Round the corners of the input image
from PIL import Image, ImageDraw

def create_rounded_image(image_path, output_path, radius):
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (w, h)], radius=radius, fill=255)
    img.putalpha(mask)
    img.save(output_path)
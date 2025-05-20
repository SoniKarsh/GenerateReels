from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Constants
WIDTH, HEIGHT = 1080, 1920
START_COLOR = np.array([0, 0, 0])
END_COLOR = np.array([53, 51, 205])
OUTPUT_DIR = "generated_posters"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Font paths and sizes
font_large_path = "/Users/technobugsai/PycharmProjects/GenerateReels/assets/fonts/LeagueSpartan-ExtraBold.ttf"
font_small_path = "/Users/technobugsai/PycharmProjects/GenerateReels/assets/fonts/Sanchez-Regular.ttf"
font_large_size = 105
font_small_size = int(23.3)

# Load fonts
font_large = ImageFont.truetype(font_large_path, font_large_size)
font_small = ImageFont.truetype(font_small_path, font_small_size)

def create_gradient_background():
    gradient = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for x in range(WIDTH):
        ratio = x / WIDTH
        color = (1 - ratio) * START_COLOR + ratio * END_COLOR
        gradient[:, x, :] = color
    return Image.fromarray(gradient, mode='RGB')

def draw_centered_text(image, day_number):
    draw = ImageDraw.Draw(image)
    main_text = "Discover,\nlearn,\nrepeat."
    day_text = f"DAY {day_number}"

    # Calculate bounding boxes
    main_text_bbox = draw.multiline_textbbox((0, 0), main_text, font=font_large, spacing=20)
    day_text_bbox = draw.textbbox((0, 0), day_text, font=font_small)

    total_height = (main_text_bbox[3] - main_text_bbox[1]) + (day_text_bbox[3] - day_text_bbox[1]) + 30
    center_x = WIDTH // 2
    main_text_x = center_x - (main_text_bbox[2] - main_text_bbox[0]) // 2
    main_text_y = (HEIGHT - total_height) // 2
    day_text_x = center_x - (day_text_bbox[2] - day_text_bbox[0]) // 2
    day_text_y = main_text_y + (main_text_bbox[3] - main_text_bbox[1]) + 30

    # Draw texts
    draw.multiline_text((main_text_x, main_text_y), main_text, font=font_large, fill="white", spacing=20, align="center")
    draw.text((day_text_x, day_text_y), day_text, font=font_small, fill="white")
    return image

def generate_posters(start_day=1, end_day=30):
    for day in range(start_day, end_day + 1):
        img = create_gradient_background()
        img = draw_centered_text(img, day)
        filename = f"day_{day:02}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"Saved {filename}")

if __name__ == "__main__":
    generate_posters(1, 30)

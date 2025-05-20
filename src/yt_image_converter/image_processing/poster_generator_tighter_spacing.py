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
font_large_size = 150
font_small_size = int(30)

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

def draw_text_with_custom_spacing(draw, text, position, font, fill, line_spacing, char_spacing):
    """Draw multiline text with custom character spacing."""
    x, y = position
    for line in text.split("\n"):
        line_x = x
        for char in line:
            draw.text((line_x, y), char, font=font, fill=fill)
            char_width = font.getlength(char)
            line_x += char_width + char_spacing
        y += font.getbbox("A")[3] + line_spacing

def draw_centered_left_aligned_text(image, day_number):
    draw = ImageDraw.Draw(image)
    main_text = "Discover,\nlearn,\nrepeat."
    day_text = f"DAY {day_number}"

    lines = main_text.split("\n")
    char_spacing = -2
    line_spacing = 10

    # Calculate true width of each line with custom character spacing
    line_widths = []
    for line in lines:
        total_width = sum(font_large.getlength(char) + char_spacing for char in line) - char_spacing
        line_widths.append(total_width)

    text_block_width = max(line_widths)
    text_block_height = len(lines) * (font_large.getbbox("A")[3] + line_spacing) + 30 + font_small.getbbox("A")[3]

    # Center the block horizontally and vertically
    block_x = (WIDTH - text_block_width) // 2
    main_text_y = (HEIGHT - text_block_height) // 2
    day_text_y = main_text_y + len(lines) * (font_large.getbbox("A")[3] + line_spacing) + 30

    # Draw large multiline text with left alignment but centered block
    y = main_text_y
    for idx, line in enumerate(lines):
        x = block_x
        for char in line:
            draw.text((x, y), char, font=font_large, fill="white")
            x += font_large.getlength(char) + char_spacing
        y += font_large.getbbox("A")[3] + line_spacing

    # Draw day text
    draw.text((block_x, day_text_y), day_text, font=font_small, fill="white")

    return image

def generate_posters(start_day=1, end_day=30):
    for day in range(start_day, end_day + 1):
        img = create_gradient_background()
        img = draw_centered_left_aligned_text(img, day)
        filename = f"day_{day:02}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"Saved {filename}")

if __name__ == "__main__":
    generate_posters(1, 3)

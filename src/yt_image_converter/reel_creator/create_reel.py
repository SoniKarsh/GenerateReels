from moviepy import ImageClip, CompositeVideoClip

from src.yt_image_converter.image_processing.effects import create_linear_gradient


def create_reel(rounded_image_path, output_path):
    video_duration = 10  # seconds
    image_width = 600
    video_size = (1080, 1920)

    # Load image clip and apply zoom-in animation
    image_clip = ImageClip(rounded_image_path).with_duration(video_duration)
    image_clip = image_clip.resized(width=image_width)
    zoomed_clip = image_clip.resized(lambda t: 2.0 - 0.05 * t)

    start_color = (0, 0, 0)  # Black
    end_color = (53, 51, 205)  # #3533cd

    gradient_np = create_linear_gradient(video_size[0], video_size[1], start_color, end_color)
    bg_clip = ImageClip(gradient_np).with_duration(video_duration)

    # Step 4: Composite background and animated image
    final_video = CompositeVideoClip([bg_clip, zoomed_clip.with_position("center")], size=video_size)

    # Step 5: Export the final video
    final_video.write_videofile(output_path, fps=30)

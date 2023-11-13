import random
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
import os


def generate_image_from_text(text_input):
    # Extract resolution and proportion of white pixels from the text input
    resolution, white_pixel_proportion = [int(val) for val in text_input.split()]

    # Calculate the width and height of the image
    width = int(math.sqrt(resolution))
    height = width

    # Create a new image
    image = Image.new('RGB', (width, height))

    # Generate pixels based on the proportion of white pixels
    total_pixels = width * height
    white_pixels_count = int(total_pixels * white_pixel_proportion / 100)
    black_pixels_count = total_pixels - white_pixels_count

    # Create a list of pixel colors
    pixels = [(255, 255, 255)] * white_pixels_count + [(0, 0, 0)] * black_pixels_count
    random.shuffle(pixels)

    # Set the pixels in the image
    image.putdata(pixels)

    return image



def create_image_with_text(text_input, size):
    width, height = size

    # Create a new image with a white background
    image = Image.new('RGB', (width, height), color='white')

    # Create a Draw object to draw on the image
    draw = ImageDraw.Draw(image)

    # Load a system font
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    font = ImageFont.truetype(font_path, min(width, height) // len(text_input))

    # Calculate the size of the text and position it in the center of the image
    text_width, text_height = draw.textsize(text_input, font=font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # Draw the text on the image
    draw.text((x, y), text_input, fill='black', font=font)

    return image


from PIL import Image, ImageDraw
import math


def get_white_pixels_count(input_image, angle):
    width, height = input_image.size
    white_pixels_count = 0

    for x in range(width):
        for y in range(height):
            pixel = input_image.getpixel((x, y))
            if pixel == (255, 255, 255):  # White pixel
                new_x = int(x - y * math.tan(math.radians(angle)))
                if 0 <= new_x < width:
                    white_pixels_count += 1

    return white_pixels_count


def create_image_with_lines(input_image):
    width, height = input_image.size

    # Copy input_image to output_image
    output_image = input_image.copy()
    draw = ImageDraw.Draw(output_image)

    max_white_pixels = 0
    white_pixels_counts = []
    angles = [i for i in range(91)]  # Angles from 0 to 90 degrees

    for angle in angles:
        white_pixels_count = get_white_pixels_count(input_image, angle)
        max_white_pixels = max(max_white_pixels, white_pixels_count)
        white_pixels_counts.append(white_pixels_count)

    for i, angle in enumerate(angles):
        brightness = int(255 * white_pixels_counts[i] / max_white_pixels)
        end_x = int(width * math.cos(math.radians(angle)))
        end_y = int(height * math.sin(math.radians(angle)))
        line_color = (brightness, brightness, brightness)
        draw.line([(0, height), (end_x, height - end_y)], fill=line_color, width=1)

    return output_image


if __name__ == "__main__":

    create_image_with_text("I'm gonna be an uncle", (400, 400)).save("generated_txt_image.png")
    ImageOps.invert(create_image_with_text("I'm gonna be an uncle", (400, 400))).save("wOb_txt_image_inverted.png")
    input_image = Image.open("wOb_txt_image_inverted.png").convert('RGB')
    output_image = create_image_with_lines(input_image)
    output_image.save("output_image.png")

    # text_input = "160000 30"  # 400x400 pixel image with 30% white pixels
    # image = generate_image_from_text(text_input)
    # image.save("generated_image.png")

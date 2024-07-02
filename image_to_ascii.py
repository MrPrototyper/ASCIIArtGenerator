#!/usr/bin/env python3

import sys
from PIL import Image, ImageDraw, ImageFont

def save_ascii_art(text, output_path, position=(10, 10), font_path='fonts/RubikMonoOne-Regular.ttf', font_size=20, font_color=(255,255,255)):
    """
    Save ASCII art as an image file.

    Args:
        text (str): The ASCII art text to be saved.
        output_path (str): The path to save the image file.
        position (tuple, optional): The position of the text in the image. Defaults to (10, 10).
        font_path (str, optional): The path to the font file. Defaults to 'fonts/RubikMonoOne-Regular.ttf'.
        font_size (int, optional): The font size. Defaults to 20.
        font_color (tuple, optional): The font color in RGB format. Defaults to (255, 255, 255).
    """
    # Split the text into lines
    lines = text.split('\n')

    # Get the width and height of the image based on the font size and number of lines
    first_line = text.split('\n')[0]
    width = len(first_line) * font_size
    height = font_size * len(lines)

    # Create a new image with the specified width and height
    img = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Load the font
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # Draw the text on the image
    draw.text(position, text, font_color, font=font)

    # Save the image to the specified output path
    img.save(output_path)

def create_ascii_art(image_path, ascii_chars=' .-~:+=*#%@', width=160):
    """
    Convert an image to ASCII art.

    Args:
        image_path (str): The path to the input image file.
        output_path (str, optional): The path to save the ASCII art. Defaults to an empty string.
        ascii_chars (str, optional): The characters used to represent different shades of gray. Defaults to ' .-~:+=*#%@'.
        width (int, optional): The desired width of the ASCII art. Defaults to 160.

    Returns:
        str: The ASCII art representation of the image.
    """
    # Open the image
    image = Image.open(image_path)

    # Calculate the height based on the desired width
    height = int(width * image.height // image.width)

    # Resize the image to the desired width and height
    image = image.resize((width, height), Image.NEAREST)

    # Initialize an empty string to store the ASCII art
    ascii_image = ''

    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            # Get the RGB values of the pixel
            r, g, b = image.getpixel((x, y))

            # Convert the RGB values to grayscale
            gray = 0.299 * r + 0.587 * g + 0.114 * b

            # Calculate the index of the ASCII character based on the grayscale value
            index = int(gray / 256 * len(ascii_chars))

            # Append the corresponding ASCII character to the ASCII art string
            ascii_image += ascii_chars[index]

        # Add a new line character at the end of each row
        ascii_image += '\n'

    # Return the ASCII art
    return ascii_image

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} <image_path> <output_path>')
        sys.exit(1)

    input_image = f'images/source/{sys.argv[1]}'
    output_file = f'images/output/{sys.argv[2]}'

    ascii_image = create_ascii_art(input_image)
    extension = output_file.split('.')[-1]

    if extension == 'txt':
        with open(output_file, 'w') as f:
            f.write(ascii_image)        
    elif output_file == '-' or output_file == 'stdout':
        print(ascii_image)
    else:
        save_ascii_art(ascii_image, output_file, font_path='fonts/RubikMonoOne-Regular.ttf', font_size=10)

    
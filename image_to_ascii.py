#!/usr/bin/env python3

import sys
from PIL import Image, ImageDraw, ImageFont

def save_ascii_art(text, output_path, position=(10, 10), font_path='fonts/RubikMonoOne-Regular.ttf', font_size=20, font_color=(255,255,255)):                
    lines = text.split('\n')
    first_line = text.split('\n')[0]
    width = len(first_line)*font_size
    height = font_size*(len(lines))

    img = Image.new('RGB', (width, height), color = (0, 0, 0))
    draw = ImageDraw.Draw(img)

    if font_path:
        font = ImageFont.truetype(font_path, font_size) 
    else:
        font = ImageFont.load_default()
    
    draw.text(position, text, font_color, font=font)
    img.save(output_path)
    
def create_ascii_art(image_path, output_path='', ascii_chars=' .-~:+=*#%@', width=160):
        image = Image.open(image_path)
        height = int(width * image.height // image.width)
        image = image.resize((width, height), Image.NEAREST)

        ascii_image = ''

        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                gray = 0.299 * r + 0.587 * g + 0.114 * b
                index = int(gray / 256 * len(ascii_chars))
                ascii_image += ascii_chars[index]        
            ascii_image += '\n'
        return ascii_image

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} <image_path> <output_path>')
        sys.exit(1)

    input_image = f'images/source/{sys.argv[1]}'
    output_file = f'images/output/{sys.argv[2]}'

    ascii_image = create_ascii_art(input_image, output_file)
    extension = output_file.split('.')[-1]

    if extension == 'txt':
        with open(output_file, 'w') as f:
            f.write(ascii_image)        
    elif output_file == '-' or output_file == 'stdout':
        print(ascii_image)
    else:
        save_ascii_art(ascii_image, output_file, font_path='fonts/RubikMonoOne-Regular.ttf', font_size=10)

    
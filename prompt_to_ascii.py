import os
import sys
import base64
from dotenv import load_dotenv
from openai import OpenAI

from image_to_ascii import save_ascii_art, create_ascii_art

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def create_image(prompt, output_image) :
    response = client.images.generate(prompt=prompt, model='dall-e-3', size="1024x1024", response_format='b64_json')
    image_data = base64.b64decode(response.data[0].b64_json)

    with open(output_image, 'wb') as f:
        f.write(image_data)      

if __name__ == '__main__':    
    output_file = f'images/output/{sys.argv[1]}.jpg'
    dalle_file = f'images/output/{sys.argv[1]}.dalle.jpg'

    create_image('The sentence "Bye Teo" in bold big letter using a littel baby boy theme', dalle_file)
    print(f'Dall-e image saved to {dalle_file}')
    ascii_art = create_ascii_art(dalle_file, output_file)
    save_ascii_art(ascii_art, output_file)
    print(f'Ascii art saved to {output_file}')
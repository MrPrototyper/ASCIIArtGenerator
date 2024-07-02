import os
import shutil
import sys
import cv2
import time
from image_to_ascii import create_ascii_art, save_ascii_art

def video_to_ascii(video_path, output_path):
    """
    Converts a video file to ASCII art frames and creates an ASCII art video.

    Parameters:
    video_path (str): The path to the video file.
    output_path (str): The path to the output directory where the ASCII art frames and video will be saved.

    Returns:
    None
    """
    vidObj = cv2.VideoCapture(video_path)
    count = 0
    flag = 1
    # Create output images
    while flag:
        flag, image = vidObj.read()
        if flag:
            cv2.imwrite(f'{output_path}/images/{count}.jpg', image)
            count += 1    

    for i in range(count):        
        input_image = f'{output_path}/images/{i}.jpg'
        ascii_art = create_ascii_art(input_image)        
        save_ascii_art(ascii_art, f'{output_path}/ascii/{i}.jpg')

    # Create video from ascii images    
    frame = cv2.imread(f'{output_path}/ascii/0.jpg')
    ih, iw = frame.shape
    fourcc= cv2.VideoWriter_fourcc(*'mp4v')
    for i in range(count):
        frame = cv2.imread(f'{output_path}/ascii/{i}.jpg')
        frame = cv2.resize(frame, (iw, ih))
        if i == 0:
            out = cv2.VideoWriter(f'{output_path}/ascii_video.mp4', fourcc, 25, (iw, ih))
        out.write(frame)

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} <video_path> <output_path>')
        sys.exit(1)    
    video_path = f'videos/input/{sys.argv[1]}'
    output_path = f'videos/output/{sys.argv[2]}'
    start_time = time.time()
    video_to_ascii(video_path, output_path)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Total processing time: {elapsed_time:.2f} seconds')
    print(f'Ascii video saved to {output_path}')
    clear_folder('videos/output/monster/ascii')
    clear_folder('videos/output/monster/html')
    clear_folder('videos/output/monster/images')
    print(f'All folders cleared')
    



import os
import time
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

from PIL import Image
import pillow_avif
from numpy import array

def encode_avif(in_file, out_file):
    with Image.open(in_file) as im:
        quality = 45
        w, h = im.size
        if w * h > 256 * 256:
            quality = 40
        im.save(out_file, save_all=False, optimize=True,quality=quality, compress_level=1)

def encode_avif_folder(in_folder, out_folder):
    start_time = time.time()
    if not os.path.exists(in_folder):
        raise Exception(f'{in_folder} not exists! Exit')
    if not os.path.exists(out_folder):
        os.makedirs(out_folder, exist_ok=True)
    with ThreadPoolExecutor(max_workers=10) as exec:
        for file_name in os.listdir(in_folder):
            out_file = os.path.join(out_folder, f'{os.path.splitext(file_name)[0]}.avif')
            # encode_avif(os.path.join(in_folder, file_name), out_file)
            exec.submit(encode_avif,os.path.join(in_folder, file_name), out_file)
    print(f'Time is: {round(time.time() - start_time,3)}s')

def test_speed(in_folder, out_folder):
    if not os.path.exists(in_folder):
        raise Exception(f'{in_folder} not exists! Exit')
    if not os.path.exists(out_folder):
        os.makedirs(out_folder, exist_ok=True)
    NUM_OF_IMG_TEST = 1000
    start_time = time.time()
    i = 0
    file_names = os.listdir(in_folder)
    file_paths = [os.path.join(in_folder, filename) for filename in file_names]
    while i < NUM_OF_IMG_TEST:
        for file_name, file_path in zip(file_names, file_paths):
            if i % 100 == 0:
                [os.remove(os.path.join(out_folder, filename)) for filename in os.listdir(out_folder)]
            encode_avif(file_path, os.path.join(out_folder, f'{i}_{os.path.splitext(file_name)[0]}.avif'))
            i += 1
            if i > NUM_OF_IMG_TEST:
                break
    print(f'Time is: {round(time.time() - start_time, 3)}s')

def main():
    filename = '/home/nghiacv/Downloads/c58755e537a7def987b6.jpg'
    # filename = '/home/nghiacv/Downloads/94ceedf9bf6648381177.jpg'
    filename = '/home/nghiacv/Downloads/IMG_39.jpg'
    # filename = '/home/nghiacv/Downloads/IMG_20190717_165818.png'
    # encode_avif(filename)
    in_folder = 'avif-test-images'
    # in_folder = 'large_images'
    out_folder = 'out_avif'
    # encode_avif_folder(in_folder, out_folder)
    test_speed(in_folder, out_folder)

if __name__ == "__main__":
    main()

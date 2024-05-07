import numpy as np

from pathlib import Path 
from PIL import Image
from typing import List 
from skimage.filters import threshold_otsu

def get_black_to_white_ratio(image_path:Path):
    """ Load the image and convert to gray scale """
    img = Image.open(image_path)
    img_gray = img.convert('L')
    
    """ Convert the image to black and white"""
    threshold = 128  
    img_bw = img_gray.point(lambda x: 255 if x > threshold else 0, '1')
    
    """ Calculate the ratio of black pixels """
    black_pixels = sum(pixel == 0 for pixel in img_bw.getdata())
    total_pixels = img_bw.size[0] * img_bw.size[1]
    black_ratio = black_pixels / total_pixels
    
    return black_ratio

def is_image_quality_acceptable(image_path:Path, image_orientation:str)->bool:
    """  ⚫ -> Good image, 🔘 -> Bad image"""
    threshold = 0.04 if image_orientation == "Portrait" else 0.03
    black_ratio = get_black_to_white_ratio(image_path)
    if black_ratio > threshold:
        return True
    return False

def get_threshold_value(data: List):
    """ input: list of values, output: optimal threshold value for the given data"""

    """ Convert the data to numpy array"""
    data = np.array(data)
    """ Applying Otsu's method to find an optimal threshold value"""
    optimal_threshold = threshold_otsu(data)
    return optimal_threshold

if __name__ == "__main__":

    from ocr_handwriting_aligner.image_utils import plot_displot
    from tqdm import tqdm 

    black_ratios = []
    image_paths = list(Path("cropped_line_images").rglob("*.jpg"))
    bad_images_dir = Path("bad_images")
    bad_images_dir.mkdir(parents=True, exist_ok=True)

    good_images_dir = Path("good_images")
    good_images_dir.mkdir(parents=True, exist_ok=True)


    line_image_label_dir = Path("cropped_line_images_label")
    for image_path in tqdm(image_paths, desc="Checking image quality"):
        label_image_path = line_image_label_dir / image_path.parent.stem / image_path.name
        black_ratio = get_black_to_white_ratio(label_image_path)
        if black_ratio > 0.03:
            image_file_path = good_images_dir / image_path.name
        else:
            image_file_path = bad_images_dir / image_path.name
        """ save image"""
        image_label_path = line_image_label_dir / image_path.parent.stem / image_path.name
        Image.open(image_label_path).save(image_file_path)
        black_ratios.append(black_ratio)


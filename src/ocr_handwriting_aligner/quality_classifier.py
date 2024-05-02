from pathlib import Path 

from PIL import Image

def get_black_to_white_ration(image_path:Path):
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

def is_image_quality_acceptable(image_path:Path, threshold:int = 0.04)->bool:
    """  ⚫ -> Good image, 🔘 -> Bad image"""
    black_ratio = get_black_to_white_ration(image_path)
    if black_ratio > threshold:
        return True
    return False

if __name__ == "__main__":

    from ocr_handwriting_aligner.image_utils import plot_displot
    

    black_ratios = []
    image_paths = list(Path("cropped_line_images_label").rglob("*.jpg"))
    bad_images_dir = Path("bad_images")
    bad_images_dir.mkdir(parents=True, exist_ok=True)

    good_images_dir = Path("good_images")
    good_images_dir.mkdir(parents=True, exist_ok=True)

    for image_path in image_paths:
        black_ratio = get_black_to_white_ration(image_path)
        if black_ratio > 0.04:
            image_file_path = good_images_dir / image_path.name
        else:
            image_file_path = bad_images_dir / image_path.name
        """ save image"""
        Image.open(image_path).save(image_file_path)
        black_ratios.append(black_ratio)

    plot_displot(black_ratios, "Black to White Ratio", "Black to White Ratio", "black_to_white_ratio.jpg")
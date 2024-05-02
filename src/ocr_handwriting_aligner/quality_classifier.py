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

def classify_line_image(image_path:Path, threshold:int = 0.125)->int:
    """ input:   image path for line image label 
                 (either a filled black circle ⚫or not filled black circle🔘) 
        output: 1 if the image is filled black circle ⚫ and 0 if not filled black circle🔘"""
    """  ⚫ -> Good image, 🔘 -> Bad image"""
    black_ratio = get_black_to_white_ration(image_path)
    if black_ratio > threshold:
        return 1
    else:
        return 0

if __name__ == "__main__":
    from ocr_handwriting_aligner.image_utils import plot_displot

    black_ratios = []
    image_paths = list(Path("cropped_line_images_label").rglob("*.jpg"))
    bad_images_dir = Path("bad_images")
    bad_images_dir.mkdir(parents=True, exist_ok=True)
    for image_path in image_paths:
        black_ratio = get_black_to_white_ration(image_path)
        black_ratios.append(black_ratio)

    plot_displot(black_ratios, "Black to White Ratio", "Black to White Ratio", "black_to_white_ratio.jpg")
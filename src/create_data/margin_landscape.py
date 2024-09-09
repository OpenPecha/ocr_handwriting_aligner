import cv2
from pathlib import Path
from tqdm import tqdm
from margin import get_image_margin  

def get_image_margin(image_path: str):
    """ Load the image and convert to grayscale """
    img = cv2.imread(image_path, 0)

    """ Apply GaussianBlur """
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    """ Threshold the image """
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    """ Define a large horizontal kernel """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    """ Get the largest contour which might be the text block """
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)

    """ Format the margins in the desired output """
    margins = {
        'Top-Left': (x, y),
        'Bottom-Right': (x + w, y + h)
    }
    return margins

if __name__ == "__main__":
    # Define the directory for portrait images
    image_dir = Path('/Users/tenzinchoedon/Downloads/scanned_images/ocr_images/landscape')

    # Get a list of all image files in the directory
    image_files = list(image_dir.glob("*.png"))  # Assuming the images are in .png format

    # Process each image file with a progress bar
    for image_file in tqdm(image_files, desc="Processing images"):
        margins = get_image_margin(str(image_file))
        print(f"Margins for {image_file.name}: {margins}")

def test_get_image_margin():
    # Define directories for portrait and landscape images
    DATA_DIR = Path("/Users/tenzinchoedon/Downloads/scanned_images/ocr_images")
    
    # Specify the filenames for testing
    portrait_image_file = "P000011_v001_00001 - 00500-001.png"  
    landscape_image_file = "P000012_v001_00001 - 00500-001.png"  
    
    # Construct full paths
    portrait_image_path = DATA_DIR / "portrait" / portrait_image_file
    landscape_image_path = DATA_DIR / "landscape" / landscape_image_file

    # Check if files exist
    if not portrait_image_path.exists():
        raise FileNotFoundError(f"Portrait image not found: {portrait_image_path}")
    if not landscape_image_path.exists():
        raise FileNotFoundError(f"Landscape image not found: {landscape_image_path}")

    # Test with a portrait image
    portrait_margin_coordinate = get_image_margin(str(portrait_image_path))
    assert portrait_margin_coordinate == {'Top-Left': (64, 55), 'Bottom-Right': (1192, 1702)}, \
        f"Expected portrait margins: {{'Top-Left': (64, 55), 'Bottom-Right': (1192, 1730)}} but got {portrait_margin_coordinate}"

    # Test with a landscape image
    landscape_margin_coordinate = get_image_margin(str(landscape_image_path))
    assert landscape_margin_coordinate == {'Top-Left': (72, 61), 'Bottom-Right': (1721, 1193)}, \
        f"Expected landscape margins: {{'Top-Left': (72, 61), 'Bottom-Right': (1721, 1193)}} but got {landscape_margin_coordinate}"

if __name__ == "__main__":
    test_get_image_margin()


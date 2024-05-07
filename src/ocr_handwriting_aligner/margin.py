import cv2



def get_image_margin(image_path:str):
    """ Load the image and convert to grayscale"""
    img = cv2.imread(image_path, 0)

    """Apply GaussianBlur"""
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    """ Threshold the image """
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    """ Define a large horizontal kernel"""
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
    
    image_path = "P000013_v001_00001 - 00353_to_image_000001.jpg"
    margin_coordinate = get_image_margin(image_path)
    print(margin_coordinate)
    
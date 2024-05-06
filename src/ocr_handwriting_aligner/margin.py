import cv2

def get_image_margin(image_path:str):
    """ Read the image """
    image = cv2.imread(image_path)
    if image is None:
        return "Image not found. Please check the path."

    """ Convert the image to grayscale """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    """ Apply GaussianBlur to reduce noise and improve edge detection """
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    """ Detect edges using Canny edge detector """
    edges = cv2.Canny(blur, 75, 150)

    """ Find contours based on edges detected"""
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    """ Find the largest contour assuming it's the document """
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        """ Assuming the document margin is uniform around the text block """
        """  We can estimate the margin coordinates (top-left and bottom-right) """
        margin_coordinates = {'Top-Left': (x, y), 'Bottom-Right': (x + w, y + h)}
        return margin_coordinates
    else:
        return "No contours found. Check the quality or content of the image."

if __name__ == "__main__":
    
    image_path = "images_output/P000010_v001_00001 - 00500/P000010_v001_00001 - 00500_to_image_000001.jpg"
    margin_coordinate = get_image_margin(image_path)
    print(margin_coordinate)
    
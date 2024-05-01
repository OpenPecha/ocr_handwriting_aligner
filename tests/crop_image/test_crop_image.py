from pathlib import Path 

from ocr_handwriting_aligner.image_utils import crop_image

def test_crop_image():
    DATA_DIR = Path(__file__).parent / "data"
    image_path = DATA_DIR / "potrait_cursive_handwritings.jpg"
    coordinates_from_xml = [(79, 171), (1425, 173), (1427, 331), (78, 327)]
    x_coords, y_coords = zip(*coordinates_from_xml)

    """ Calculate minimum and maximum x and y values """
    min_x = min(x_coords)
    min_y = min(y_coords)
    max_x = max(x_coords)
    max_y = max(y_coords)
    coordinates = (min_x, min_y, max_x, max_y)

    cropped_image = crop_image(image_path, coordinates)
    cropped_image_path = DATA_DIR / "cropped_image.jpg"
    cropped_image.save(cropped_image_path)
    assert cropped_image_path.exists()
    expected_cropped_image_path = DATA_DIR / "expected_cropped_image.jpg"
    assert cropped_image_path.read_bytes() == expected_cropped_image_path.read_bytes()
    cropped_image_path.unlink()

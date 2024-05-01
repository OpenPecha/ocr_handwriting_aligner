from pathlib import Path 

from ocr_handwriting_aligner.image_utils import crop_image
from ocr_handwriting_aligner.utils import standardize_coordinates_from_xml

def test_crop_image():
    DATA_DIR = Path(__file__).parent / "data"
    image_path = DATA_DIR / "potrait_cursive_handwritings.jpg"
    coordinates_from_xml = [(79, 171), (1425, 173), (1427, 331), (78, 327)]
    coordinates = standardize_coordinates_from_xml(coordinates_from_xml)

    cropped_image = crop_image(image_path, coordinates)
    cropped_image_path = DATA_DIR / "cropped_image.jpg"
    cropped_image.save(cropped_image_path)
    assert cropped_image_path.exists()
    expected_cropped_image_path = DATA_DIR / "expected_cropped_image.jpg"
    assert cropped_image_path.read_bytes() == expected_cropped_image_path.read_bytes()
    cropped_image_path.unlink()

from pathlib import Path 

from ocr_handwriting_aligner.margin import get_image_margin


def test_get_image_margin():
    DATA_DIR = Path(__file__).parent / "data"
    image_path = str(DATA_DIR / "potrait_image.jpg")
    margin_coordinate = get_image_margin(image_path)
    assert margin_coordinate == {'Top-Left': (74, 57), 'Bottom-Right': (1578, 2257)}

    DATA_DIR = Path(__file__).parent / "data"
    image_path = str(DATA_DIR / "landscape_image.jpg")
    margin_coordinate = get_image_margin(image_path)
    assert margin_coordinate == {'Top-Left': (72, 70), 'Bottom-Right': (1580, 2273)}



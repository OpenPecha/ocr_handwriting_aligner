from pathlib import Path 

from ocr_handwriting_aligner.quality_classifier import is_image_quality_acceptable


def test_quality_classfier():
    DATA_DIR = Path(__file__).parent / "data"
    good_image_label_path = DATA_DIR / "good_image_label.jpg"
    image_orientation = "Portrait"
    result = is_image_quality_acceptable(good_image_label_path, image_orientation)
    assert result == True

    bad_image_label_path = DATA_DIR / "bad_image_label.jpg"
    result = is_image_quality_acceptable(bad_image_label_path, image_orientation)
    assert result == False


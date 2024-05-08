import shutil
from pathlib import Path 

from ocr_handwriting_aligner.image_utils import pdf_to_images


def test_pdf_to_images():
    DATA_DIR = Path(__file__).parent / "data"
    pdf_file_path = DATA_DIR / "P000010_v001_00001 - 00003.pdf"

    result = pdf_to_images(pdf_file_path, DATA_DIR)
    assert len(result) == 3
    for image_path in result:
        assert image_path.exists()
    
    """ Clean up"""
    shutil.rmtree(DATA_DIR / pdf_file_path.stem, ignore_errors=True)

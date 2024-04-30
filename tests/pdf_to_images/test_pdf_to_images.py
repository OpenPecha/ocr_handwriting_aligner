import shutil
from pathlib import Path 

from ocr_handwriting_aligner.image_utils import pdf_to_images


def test_pdf_to_images():
    DATA_DIR = Path(__file__).parent / "data"
    pdf_file_path = DATA_DIR / "potrait_cursive_handwriting.pdf"

    result = pdf_to_images(pdf_file_path, DATA_DIR)
    assert "images_path" in result
    assert len(result["images_path"]) == 3
    for image_path in result["images_path"]:
        assert image_path.exists()
    
    """ Clean up"""
    shutil.rmtree(DATA_DIR / pdf_file_path.stem, ignore_errors=True)

    pdf_file_path = DATA_DIR / "does_not_exist.pdf"
    result = pdf_to_images(pdf_file_path, DATA_DIR)

    assert "error" in result
    assert result["error"] == f"PDF file {str(pdf_file_path)} does not exist"



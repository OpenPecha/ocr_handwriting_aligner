import math

from tqdm import tqdm
from pathlib import Path
from pdf2image import convert_from_path, pdfinfo_from_path
from typing import Dict 

def get_total_pages(pdf_path):
    pdf_info = pdfinfo_from_path(pdf_path)
    return int(pdf_info["Pages"])

def pdf_to_images(pdf_path: Path, output_dir: Path, batch_size:int=10)->Dict:
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_to_images_dir = Path(output_dir/pdf_path.stem)
    if not pdf_to_images_dir.exists():
        pdf_to_images_dir.mkdir(parents=True, exist_ok=True)

    if not pdf_path.exists():
        error_msg = {"error": f"PDF file {pdf_path} does not exist"}
        return error_msg

    try:
        total_pages = get_total_pages(pdf_path)
        total_batches = math.ceil(total_pages / batch_size)

        result = {"images_path":[]}
        """ spliting pdf to images in batches, since pdf2image is not able to convert all pages at once"""
        for batch_index in tqdm(range(total_batches), desc=f"Converting pdf to images in {total_batches} batches"):
            start_page = batch_index * batch_size + 1
            end_page = min((batch_index + 1) * batch_size, total_pages)
            pages = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)

            for i, page in enumerate(pages, start=start_page):
                image_path = pdf_to_images_dir / f"{pdf_path.stem}_to_image_{i:06}.jpg"
                page.save(image_path, "JPEG")
                result["images_path"].append(image_path)
        
        return result

    except Exception as e:
        error_msg = {"error": f"Error converting PDF file {pdf_path}: {e}"}
        return error_msg



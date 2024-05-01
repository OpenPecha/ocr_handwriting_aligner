from pathlib import Path 
from typing import List

from tqdm import tqdm 

from ocr_handwriting_aligner.utils import get_coordinates_from_xml, standardize_coordinates_from_xml, sort_paths_and_get_paths
from ocr_handwriting_aligner.image_utils import crop_image
from ocr_handwriting_aligner.config import PORTRAIT_LINE_IMAGES_COORDINATES_XML_PATH, PORTRAIT_LINE_IMAGES_LABEL_COORDINATES_XML_PATH

def crop_image_pipeline(image_path: Path, output_dir:Path, xml_path:Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    coordinates_from_xml =  get_coordinates_from_xml(xml_path)
    for idx,coordinate_from_xml in enumerate(coordinates_from_xml.values()):
            coordinate = standardize_coordinates_from_xml(coordinate_from_xml)
            cropped_image = crop_image(image_path, coordinate)
            cropped_image.save(output_dir / f"{image_path.stem}_{idx}.jpg")


def pipeline(images_path: List[Path]):
    """ This function is the main pipeline function that will be called to crop the line images from the given images"""
    line_image_dir = Path("cropped_line_images")
    line_image_label_dir = Path("cropped_line_images_label") 
    
    line_image_dir.mkdir(parents=True, exist_ok=True)
    line_image_label_dir.mkdir(parents=True, exist_ok=True)

    images_path = sort_paths_and_get_paths(images_path)

    for image_path in tqdm(images_path, desc="Cropping line images"):
        """ coordinates_from_xml is a dictionary with keys as line numbers and values as list of coordinates"""
        """ there will be coordinates for each line in the image(7 lines)"""
        cropped_image_dir = line_image_dir / image_path.stem
        crop_image_pipeline(image_path, cropped_image_dir, PORTRAIT_LINE_IMAGES_COORDINATES_XML_PATH)
        
        cropped_image_dir = line_image_label_dir / image_path.stem
        crop_image_pipeline(image_path, cropped_image_dir, PORTRAIT_LINE_IMAGES_LABEL_COORDINATES_XML_PATH)
        


if __name__ == "__main__":
    images_path = list(Path("images_output").rglob("*.jpg"))
    pipeline(images_path)
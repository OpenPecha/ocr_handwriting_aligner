import csv 
from pathlib import Path 
from typing import List

from tqdm import tqdm 

from ocr_handwriting_aligner.utils import get_coordinates_from_xml, standardize_coordinates_from_xml, sort_paths_and_get_paths
from ocr_handwriting_aligner.image_utils import crop_image
from ocr_handwriting_aligner.config import (
        PORTRAIT_LINE_IMAGES_COORDINATES_XML_PATH, 
        PORTRAIT_LINE_IMAGES_LABEL_COORDINATES_XML_PATH, 
        PORTRAIT_IMAGE_MARGIN,
        LANDSCAPE_LINE_IMAGES_COORDINATES_XML_PATH,
        LANDSCAPE_LINE_IMAGES_LABEL_COORDINATES_XML_PATH,
        LANDSCAPE_IMAGE_MARGIN
)
from ocr_handwriting_aligner.quality_classifier import is_image_quality_acceptable
from ocr_handwriting_aligner.parse_transcript import get_line_image_transcript
from ocr_handwriting_aligner.margin import get_image_margin

def crop_line_image_pipeline(image_path: Path, output_dir:Path, xml_path:Path, image_orientation:str ):
    """ This function crops the line images from the given image based on the coordinates from the xml file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    coordinates_from_xml =  get_coordinates_from_xml(xml_path)
    margin = get_image_margin(str(image_path))
    """ Adjust the coordinates based on the margin of the the standard image"""
    STANDARD_IMAGE_MARGIN = PORTRAIT_IMAGE_MARGIN if image_orientation == "Portrait" else LANDSCAPE_IMAGE_MARGIN
    vertical_diff = STANDARD_IMAGE_MARGIN["Top-Left"][1]-margin["Top-Left"][1]
    horizontal_diff = STANDARD_IMAGE_MARGIN["Top-Left"][0]-margin["Top-Left"][0]
    
    for idx,coordinate_from_xml in enumerate(coordinates_from_xml.values()):
            coordinate = standardize_coordinates_from_xml(coordinate_from_xml)
            """ Adjust the coordinates based on the margin of the image"""
            coordinate = (coordinate[0]-horizontal_diff, coordinate[1]-vertical_diff, coordinate[2]-horizontal_diff, coordinate[3]-vertical_diff)
            cropped_image = crop_image(image_path, coordinate)
            cropped_image.save(output_dir / f"{image_path.stem}_{idx+1}.jpg")


def crop_line_image_label_pipeline(image_path: Path, output_dir:Path, xml_path:Path):
    """ This function crops the line images from the given image based on the coordinates from the xml file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    coordinates_from_xml =  get_coordinates_from_xml(xml_path)

    for idx,coordinate_from_xml in enumerate(coordinates_from_xml.values()):
            coordinate = standardize_coordinates_from_xml(coordinate_from_xml)
            """ Adjust the coordinates based on the margin of the image"""
            coordinate = (coordinate[0], coordinate[1], coordinate[2], coordinate[3])
            cropped_image = crop_image(image_path, coordinate)
            cropped_image.save(output_dir / f"{image_path.stem}_{idx+1}.jpg")



def pipeline(images_path: List[Path], transcript_file_path:Path, image_orientation:str, output_csv_path:Path=Path("line_image_mapping.csv")):
    """ This function is the main pipeline function that will be called to crop the line images from the given images"""
    line_image_dir = Path("cropped_line_images")
    line_image_label_dir = Path("cropped_line_images_label") 
    
    line_image_dir.mkdir(parents=True, exist_ok=True)
    line_image_label_dir.mkdir(parents=True, exist_ok=True)

    images_path = sort_paths_and_get_paths(images_path)

    for image_path in tqdm(images_path, desc="Cropping line images"):
        """ coordinates_from_xml is a dictionary with keys as line numbers and values as list of coordinates"""
        """ there will be coordinates for each line in the image(7 lines)"""
        
        """ line image """
        cropped_image_dir = line_image_dir / image_path.stem
        xml_path = PORTRAIT_LINE_IMAGES_COORDINATES_XML_PATH if image_orientation== "Portrait" else LANDSCAPE_LINE_IMAGES_COORDINATES_XML_PATH
        crop_line_image_pipeline(image_path, cropped_image_dir, xml_path, image_orientation)
        
        """ line image label """
        cropped_image_dir = line_image_label_dir / image_path.stem
        xml_path = PORTRAIT_LINE_IMAGES_LABEL_COORDINATES_XML_PATH if image_orientation == "Portrait" else LANDSCAPE_LINE_IMAGES_LABEL_COORDINATES_XML_PATH
        crop_line_image_label_pipeline(image_path, cropped_image_dir, xml_path)
        
    """ get acceptable good line images """
    images_path = list(line_image_dir.rglob("*.jpg"))
    images_path = sort_paths_and_get_paths(images_path)

    acceptable_images = []
    for image_path in tqdm(images_path, desc="Getting acceptable line images"):
        """ get line image label path """
        label_image_path = line_image_label_dir / image_path.parent.stem / image_path.name
        
        if not label_image_path.exists():
            print(f"Label image not found for {str(image_path)}")
            continue

        """ check if the image quality is acceptable"""
        """ if the image quality is acceptable, then get the transcript for the line image"""
        if is_image_quality_acceptable(label_image_path, image_orientation):
            image_name = image_path.parent.name
            image_number = int(image_name.split("_")[-1])
            line_number = int(image_path.stem.split("_")[-1])
            image_transcript = get_line_image_transcript(transcript_file_path, image_number, line_number)
            if image_transcript is None:
                continue
            if image_transcript["text"] :
                acceptable_images.append({"images_path": str(image_path), "transcripts": image_transcript["text"]})

    """ write the mapping to csv"""
    with open(output_csv_path, 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = ["images_path", "transcripts"]) 
        writer.writeheader() 
        writer.writerows(acceptable_images) 
    return acceptable_images

if __name__ == "__main__":
    images_path = list(Path("pdf_to_images_output").rglob("*.jpg"))
    transcript_file_path = Path("P000013_v001.csv")
    image_orientation="Landscape"
    acceptable_images = pipeline(images_path, transcript_file_path, image_orientation)
    print(f"Number of line images: {len(images_path)*5}")
    print(f"Number of acceptable line images: {len(acceptable_images)}")
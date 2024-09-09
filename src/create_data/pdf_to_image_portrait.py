from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

def pdf_to_images(pdf_file, output_dir):
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Processing {pdf_file} -> Output directory: {output_dir}")

    # Construct the command for pdftoppm
    output_prefix = output_dir / pdf_file.stem
    command = ["pdftoppm", str(pdf_file), str(output_prefix), "-png"]
    print(f"Running command: {' '.join(command)}")

    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Check for errors
    if result.returncode != 0:
        return f"Error processing {pdf_file}: {result.stderr}"
    return f"Successfully processed {pdf_file}"

def get_coordinates_from_xml(xml_path: Path) -> Dict[int, List[Tuple[int, int]]]:
    namespaces = {
        'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'
    }
    tree = ET.parse(xml_path)
    root = tree.getroot()

    coordinates_dict = {}
    counter = 1

    for text_region in root.findall('.//ns:TextRegion', namespaces):
        coords_element = text_region.find('ns:Coords', namespaces)
        if coords_element is not None:
            coordinates = coords_element.attrib['points']
            coordinate_list = [tuple(map(int, point.split(','))) for point in coordinates.split()]
            coordinates_dict[counter] = coordinate_list
            counter += 1

    return coordinates_dict

def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
        return width, height
    except IOError:
        return "Error: The file could not be opened. Please check the file path and format."

def plot_displot(data, title, x_label, filename):
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    ax = sns.displot(data, kind="hist", bins=30, kde=True, color='blue')
    ax.fig.suptitle(title)
    ax.set_axis_labels(x_label, 'Frequency')
    plt.subplots_adjust(top=0.9)
    ax.savefig(filename)
    plt.close()

def crop_image(image_path: Path, crop_coords: Tuple[int, int, int, int]):
    try:
        with Image.open(image_path) as img:
            cropped_img = img.crop(crop_coords)
            return cropped_img
    except Exception as e:
        print(f"Error cropping image {image_path}: {e}")
        return None

if __name__ == "__main__":
    # Directory for portrait PDFs
    pdf_dir = Path('/Users/tenzinchoedon/Downloads/scanned_images/འཁྱུག་ཡིག་གཤེར་དཔར།(portrait)')
    
    # Output directory for images
    output_dir = Path('/Users/tenzinchoedon/Downloads/scanned_images/ocr_images/portrait')
    
    print(f"Processing directory: {pdf_dir}")

    # Process each PDF file in the directory with a progress bar
    for pdf_file in tqdm(list(pdf_dir.glob("*.pdf")), desc="Converting PDFs to Images"):
        print(f"Found PDF file: {pdf_file}")
        result = pdf_to_images(pdf_file, output_dir)
        print(result)

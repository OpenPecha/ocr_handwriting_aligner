from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET



def sort_paths_and_get_paths(paths:List[Path]) -> List[Path]:
    """ sort paths by string and return as string"""
    return [path for path in sorted(paths, key=lambda path: str(path))]

def get_coordinates_from_xml(xml_path: Path) -> Dict[int, List[Tuple[int, int]]]:
    """Namespace dictionary to handle namespaces in the XML file."""
    namespaces = {
        'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'
    }

    """Parse the XML file."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    """Dictionary to store coordinates."""
    coordinates_dict = {}
    counter = 1

    """Find all TextRegion elements and extract their coordinates as list of tuples."""
    for text_region in root.findall('.//ns:TextRegion', namespaces):
        coords_element = text_region.find('ns:Coords', namespaces)
        if coords_element is not None:
            coordinates = coords_element.attrib['points']
            """ Convert the coordinates string to a list of tuples """
            coordinate_list = [tuple(map(int, point.split(','))) for point in coordinates.split()]
            coordinates_dict[counter] = coordinate_list
            counter += 1

    return coordinates_dict

def standardize_coordinates_from_xml(coordinates_from_xml:  List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Standardize the coordinates to be in the range"""
    """ from xml, we get 4 ordered coordinates,"""
    """ (x1, y1), (x2, y2), (x3, y3), (x4, y4)"""
    """ we need to find min_x, min_y, max_x, max_y"""
    x_coordinates, y_coordinates = zip(*coordinates_from_xml)
    min_x, max_x = min(x_coordinates), max(x_coordinates)
    min_y, max_y = min(y_coordinates), max(y_coordinates)

    return (min_x, min_y, max_x, max_y)

if __name__ == "__main__":
    xml_path = Path("resources/potrait/handwriting_line_images_coordinates.xml")
    coordinates_dict = get_coordinates_from_xml(xml_path)
    print(coordinates_dict)

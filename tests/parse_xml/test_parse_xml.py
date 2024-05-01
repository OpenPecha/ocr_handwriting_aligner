from pathlib import Path 
from ocr_handwriting_aligner.utils import get_coordinates_from_xml

def test_get_coordinates_from_xml():
    DATA_DIR = Path(__file__).parent / "data"
    xml_file_path = DATA_DIR / "handwriting_line_images_coordinates.xml"

    coordinates = get_coordinates_from_xml(xml_file_path)
    print(coordinates)

    assert isinstance(coordinates, dict)
    assert len(coordinates) == 7
    expected_coordinates = {
                            1: [(79, 171), (1425, 173), (1427, 331), (78, 327)], 
                            2: [(78, 440), (1423, 440), (1425, 595), (77, 596)], 
                            3: [(80, 708), (1423, 706), (1428, 866), (81, 868)], 
                            4: [(81, 978), (1427, 978), (1427, 1139), (81, 1139)], 
                            5: [(77, 1249), (1425, 1249), (1425, 1408), (77, 1408)], 
                            6: [(82, 1521), (1427, 1522), (1429, 1681), (83, 1678)], 
                            7: [(83, 1790), (1426, 1790), (1426, 1953), (83, 1953)]
                            }
    assert coordinates == expected_coordinates


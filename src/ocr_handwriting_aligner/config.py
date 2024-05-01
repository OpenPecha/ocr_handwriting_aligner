from pathlib import Path 


CUR_DIR = Path(__file__).parent
ROOT_DIR = CUR_DIR.parent.parent
RESOURCE_DIR = ROOT_DIR / "resources"

POTRAIT_DIR = RESOURCE_DIR / "potrait"

PORTRAIT_LINE_IMAGES_COORDINATES_XML_PATH = POTRAIT_DIR / "handwriting_line_images_coordinates.xml"
PORTRAIT_LINE_IMAGES_LABEL_COORDINATES_XML_PATH = POTRAIT_DIR / "handwriting_line_images_label_coordinates.xml"



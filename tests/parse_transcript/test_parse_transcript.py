from pathlib import Path 

from ocr_handwriting_aligner.parse_transcript import get_line_image_transcript

def test_get_line_image_transcript():
    DATA_DIR = Path(__file__).parent / "data"
    transcript_path = DATA_DIR / "P000010_v001.csv"
    image_number = 1
    output = get_line_image_transcript(transcript_path, image_number,1)
    expected_output = {'name': 'P000010_v001_00001', 
                       'text': '༄༅༅། །ཞལ་གདམས་དང་གསུང་མགུར་སྣ་ཚོགས་ཀྱི་སྐོར་ཀུན་ཕན་བདུད་རྩིའི་སྤྲིན་', 
                       }
    assert output == expected_output


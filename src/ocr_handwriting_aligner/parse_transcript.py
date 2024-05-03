from pathlib import Path 

def get_line_image_transcript(transcript_file_path:Path, image_number:int, line_number:int):
    text = transcript_file_path.read_text(encoding="utf-8")

    """ image_name, line 1 transcript, line 2 transcript, line 3 transcript, line 4 transcript, line 5 transcript, line 6 transcript, line 7 transcript"""
    image_transcript_str = text.split("\n")[image_number-1]
    parsed_image_transcript = image_transcript_str.split(",")
    image_transcript = {}
    if len(parsed_image_transcript) == 8:
        image_transcript["name"] = parsed_image_transcript[0]
        image_transcript["text"] = parsed_image_transcript[line_number]
        return image_transcript
    return None 




if __name__ == "__main__":
    transcript_path = Path("P000010_v001.csv")
    image_number = 1
    image_transcript = get_line_image_transcript(transcript_path, image_number)
    print(image_transcript)

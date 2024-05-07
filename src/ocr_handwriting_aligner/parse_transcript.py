from pathlib import Path 

def get_line_image_transcript(transcript_file_path:Path, image_number:int, line_number:int):
    text = transcript_file_path.read_text(encoding="utf-8")

    """ image_name, line 1 transcript, line 2 transcript, line 3 transcript, line 4 transcript, line 5 transcript, line 6 transcript, line 7 transcript"""
    image_transcript_str = text.split("\n")[image_number-1]
    parsed_image_transcript = image_transcript_str.split(",")
    image_transcript = {}
    try:
            image_transcript["name"] = parsed_image_transcript[0]
            image_transcript["text"] = parsed_image_transcript[line_number]
            return image_transcript
    except Exception as e: 
        print(f"Transcript not found for image number {image_number} and line number {line_number}")
        return None 




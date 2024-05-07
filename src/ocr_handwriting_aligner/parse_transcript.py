import csv 
import pandas as pd

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


def get_image_url(image_name, batch_id):
    """ returns amazon s3 buckets link of the uploaded image"""
    image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/Handwritten-cursive/{batch_id}/{image_name}"
    return image_url

def add_row_to_csv(row, csv_path):
    if Path(csv_path).exists():
        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    else:
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

def standardize_line_texts_to_images_csv_mapping(csv_file_path:Path, batch_id:str, volume_id:str):
    """ parse the line texts to images mapping """
    df = pd.read_csv(csv_file_path)
    images_path = list(df["image_path"])
    transcripts = list(df["transcript"])

    """ standardize """
    output_file_path = f"{batch_id}_{volume_id}.csv"
    if Path(output_file_path).exists():
        Path(output_file_path).unlink()

    headers = ["image_name","transcript","image_url"]
    add_row_to_csv(headers, output_file_path)
    for image_path, transcript in zip(images_path, transcripts):
        image_name = Path(image_path).name
        image_url = get_image_url(image_name, f"{batch_id}")
        row = [image_name, transcript, image_url]
        add_row_to_csv(row, output_file_path)
        row = []

    return output_file_path


if __name__ == "__main__":
    standardize_line_texts_to_images_csv_mapping("line_image_mapping.csv", "P000013", "v001")
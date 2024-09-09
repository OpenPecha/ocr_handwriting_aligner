import numpy as np
from pathlib import Path 
from PIL import Image
from typing import List 
from skimage.filters import threshold_otsu
import pandas as pd
from ocr_handwriting_aligner.quality_classifier import is_image_quality_acceptable

def get_black_to_white_ratio(image_path:Path):
    """ Load the image and convert to gray scale """
    img = Image.open(image_path)
    img_gray = img.convert('L')
    
    """ Convert the image to black and white"""
    threshold = 128  
    img_bw = img_gray.point(lambda x: 255 if x > threshold else 0, '1')
    
    """ Calculate the ratio of black pixels """
    black_pixels = sum(pixel == 0 for pixel in img_bw.getdata())
    total_pixels = img_bw.size[0] * img_bw.size[1]
    black_ratio = black_pixels / total_pixels
    
    return black_ratio

def is_image_quality_acceptable(image_path:Path, image_orientation:str)->bool:
    """  ⚫ -> Good image, 🔘 -> Bad image"""
    threshold = 0.04 if image_orientation == "Portrait" else 0.03
    black_ratio = get_black_to_white_ratio(image_path)
    if black_ratio > threshold:
        return True
    return False

def get_threshold_value(data: List):
    """ input: list of values, output: optimal threshold value for the given data"""

    """ Convert the data to numpy array"""
    data = np.array(data)
    """ Applying Otsu's method to find an optimal threshold value"""
    optimal_threshold = threshold_otsu(data)
    return optimal_threshold

#Testing


def test_quality_classifier():
    
    good_image_label_path = Path("/Users/tenzinchoedon/ocr_handwriting_aligner/src/good_image_label.jpg")
    bad_image_label_path = Path("/Users/tenzinchoedon/ocr_handwriting_aligner/src/bad_image_label.jpg")
    
    image_orientation = "Portrait"
    
    result = is_image_quality_acceptable(good_image_label_path, image_orientation)
    assert result == True, f"Expected True but got {result}"

    result = is_image_quality_acceptable(bad_image_label_path, image_orientation)
    assert result == False, f"Expected False but got {result}"

    print("All tests passed!")  # Print this if all tests are successful

if __name__=="__main___":
    # File paths
    transcript_csv_path = Path("/Users/tenzinchoedon/Desktop/Work/ocr_handwriting_aligner/src/ocr_handwriting_aligner/intern/line_image_mapping_csv/line_image_mapping-portait-000011_v001_00001-00500.csv")
    quality_csv_path = Path("/Users/tenzinchoedon/Desktop/Work/ocr_handwriting_aligner/src/ocr_handwriting_aligner/intern/output_csv/quality_results-portriat-P000011_v001_00001-00500.csv")

    # Load the transcript data without headers
    transcript_df = pd.read_csv(transcript_csv_path, header=0)  # Use header=0 to read the first row as headers

    # Debug: Check the transcript DataFrame
    print("Transcript DataFrame:")
    print(transcript_df.head())
    print("Transcript DataFrame Columns:", transcript_df.columns.tolist())  # Print column names

    # Strip any extra spaces from the image paths
    transcript_df['image_path'] = transcript_df['image_path'].apply(lambda x: x.strip())

    # Load the quality data with headers
    quality_df = pd.read_csv(quality_csv_path)

    # Debug: Check the quality DataFrame
    print("Quality DataFrame:")
    print(quality_df.head())
    print("Quality DataFrame Columns:", quality_df.columns.tolist())  # Print column names

    # Strip any extra spaces from the image paths in the quality DataFrame
    quality_df['image_path'] = quality_df['image_path'].apply(lambda x: x.strip())

    # Filter to keep only accepted data
    accepted_df = quality_df[quality_df['quality'] == 'acceptable'].copy()  # Debug: Check the accepted DataFrame
    print("Accepted DataFrame:")
    print(accepted_df.head())
    print("Accepted DataFrame Columns:", accepted_df.columns.tolist())  # Print column names

    # Construct the S3 URL for the images
    base_s3_url = "s3://monlam.ai.ocr/Handwritten-cursive/Images/cropped_line_images-portrait-P000011_v001_00001-00500/"

    # Create the image_url column
    accepted_df['image_url'] = accepted_df['image_path'].apply(lambda x: f"{base_s3_url}{Path(x).name}")

    # Example of standardizing image_path for merging
    # Extract the base name from the quality_df image_path for merging
    accepted_df['base_image_name'] = accepted_df['image_path'].apply(lambda x: Path(x).name)

    # Extract the base name from transcript_df to match
    transcript_df['base_image_name'] = transcript_df['image_path'].apply(lambda x: Path(x).name)

    # Merge the accepted_df with transcript_df on the standardized base image names
    merged_df = pd.merge(accepted_df, transcript_df[['base_image_name', 'transcript']], on='base_image_name', how='left')

    # Debugging: Print the merged DataFrame to verify the merge
    print("Merged DataFrame:")
    print(merged_df.head())
    print("Merged DataFrame Columns:", merged_df.columns.tolist())  # Print column names

    # Prepare the final DataFrame with the specified headers
    # Use the correct column names based on the merge
    final_df = merged_df[['image_path', 'transcript', 'image_url']]  # Adjust this line if necessary

    # Rename the columns for the final output
    final_df.columns = ['image_name', 'transcript', 'image_url']  # Rename to the specified headings

    # Save the merged data to a new CSV file with headers
    output_csv_path = Path("/Users/tenzinchoedon/Desktop/Work/ocr_handwriting_aligner/src/portrait-P000011_v001_00001-00500.csv")
    final_df.to_csv(output_csv_path, index=False, header=True)  # Save with header

    print(f"Final accepted data saved to {output_csv_path}")



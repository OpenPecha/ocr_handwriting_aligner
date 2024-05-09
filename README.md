
<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<!-- Replace with 1-sentence description about what this tool is or does.-->

<h3 align="center">ocr_handwriting_aligner</h3>

## Description

tool to prepare ocr data of handwritings data


## Project owner(s)

<!-- Link to the repo owners' github profiles -->

- [@tenzin3](https://github.com/tenzin3)

## Installation

```py
pip install git+https://github.com/OpenPecha/ocr_handwriting_aligner.git
```

## Usage

```py
from ocr_handwriting_aligner.pipeline import pipeline

pdf_file_path = Path("P000015_v001_00001 - 00250.pdf")
transcript_file_path = Path("P000015_v001_transcript.csv")
image_orientation="Portrait"
acceptable_images = pipeline(pdf_file_path, transcript_file_path, image_orientation)
print(f"Number of acceptable line images: {len(acceptable_images)}")
```

Important Notes:


-  image_orientation can either be "Potrait" or "Landscape".
- transcript.csv should not have heading and directly start with values. Its value should be "image name", "line 1 transcript", "line 2 transcript", (separated by comma)
- Potrait image has total of 7 lines and Landscape has total of 5 lines handwritings.

Outputs after running the above code:

- "pdf_to_images_output" dir: contains images converted from the pdf (each page -> one image generated)
- "cropped_line_images" dir: each cropped line images in a inner folder dir named after image name
- "cropped_line_images_label" dir: each cropped line images label in a inner folder named after image name
- "line_image_mapping.csv": contains image_path and transcript


## standardize the csv

```py

from ocr_handwriting_aligner.parse_transcript import standardize_line_texts_to_images_csv_mapping

csv_file_path = Path("line_image_mapping.csv")
batch_id = "P000015"
volume_id = "v001"
standardize_line_texts_to_images_csv_mapping(csv_file_path, batch_id, volume_id)
```

Output after running the above code:

- standardize csv: named in format "{batch_id}_{volume_id}.csv" (in this case P000015_v001.csv) with headings "image_name","transcript","image_url" 
- "image url" is refering to a s3 bucket link

- new output dir: a dir name "{batch_id}_{volume_id}" (in this case P000015_v001), all the acceptable images will be copied in this directory, you can upload the images from this directory to the desired s3 bucket
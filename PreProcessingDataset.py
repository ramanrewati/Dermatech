import json
import csv
import os

def create_json_dataset(csv_path, image_root, output_json_path):
    """
    Creating a JSON mllm format required to finetune the QWEN2 VL.
    """

    data = []  
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            image_path = os.path.join(image_root, row['skincap_file_path']) 

            caption = row['caption_zh_polish_en'] + " The condition seems to be " + row['disease'] + "."

            json_item = {
                "messages": [
                    {"content": f"<image>I am facing this skin condition.", "role": "user"},
                    {"content": caption, "role": "assistant"}  
                ],
                "images": [image_path]
            }
            data.append(json_item)  


    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# Example usage:
csv_file_path = 'dataset.csv'
image_root = '/vlm_dataset'  
output_json_file = 'Dermatech_vlm.json'

create_json_dataset(csv_file_path, image_root, output_json_file)
print(f"JSON dataset created at: {output_json_file}")

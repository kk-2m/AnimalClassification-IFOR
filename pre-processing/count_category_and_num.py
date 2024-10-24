import json
import os
import sys

dataset_name = input("Input dataset name(wcs, cct): ")
dataset_type = input("Input dataset type(color, IR): ")

root_directory = "../"

if dataset_name == "wcs":
    dataset_directory = root_directory + "wcs/"
elif dataset_name == "cct":
    dataset_directory = root_directory + "cct/"
else:
    print("Don't exist")
    sys.exit()

if dataset_type == "color":
    target_directory = dataset_directory + "color_bboxes/"
elif dataset_type == "IR":
    target_directory = dataset_directory + "infrared_bboxes/"
else:
    print("Don't exist")
    sys.exit()

mapping_category_and_num = {}
if dataset_type == "color":
    json_name = "NumOfImagesPerCategory_Color.json"
elif dataset_type == "IR":
    json_name = "NumOfImagesPerCategory_IR.json"
else:
    print("Don't exist")
    sys.exit()

subfolders = [f.path for f in os.scandir(target_directory) if f.is_dir()]

for subfolder_name in subfolders:
    num_of_files = len(os.listdir(subfolder_name))
    mapping_category_and_num[subfolder_name] = num_of_files

print(mapping_category_and_num.values())

sorted_items = sorted(mapping_category_and_num.items(), key=lambda x: x[1], reverse=True)
sorted_dict = {key: value for key, value in sorted_items}

with open(dataset_directory+json_name, 'w') as f:
    json.dump(sorted_dict, f, indent=4)
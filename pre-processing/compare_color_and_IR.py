# This code is for counting num of images that is both contained by caltech, wcs.

import json
import csv
import sys
dataset_name = input("Input dataset name(wcs, cct): ")
root_directory = "../"
# Dataset
if dataset_name == "wcs":
    dataset_directory = root_directory + "wcs/"
elif dataset_name == "cct":
    dataset_directory = root_directory + "cct/"
else:
    print("Don't exist")
    sys.exit()

# JSON file path
infrared_json_directory = dataset_directory + "NumOfImagesPerCategory_IR.json"
color_json_directory = dataset_directory + "NumOfImagesPerCategory_Color.json"

# Base class
className = "color_bboxes"
anotherClassName = ""
if className == "color_bboxes":
    anotherClassName = "infrared_bboxes"
else:
    anotherClassName = "color_bboxes"
center_class = dataset_directory + className

mapping_IR_category_and_num = {}
mapping_color_category_and_num = {}

save_file_name = "compared_color_IR_" + dataset_name +".csv"

with open(infrared_json_directory) as f:
    mapping_IR_category_and_num = json.load(f)
with open(color_json_directory) as f:
    mapping_color_category_and_num = json.load(f)


compared_list = []
for color_category in mapping_color_category_and_num:
    infrared_category_path = color_category.replace(className,anotherClassName)
    if infrared_category_path in mapping_IR_category_and_num.keys():
        category_name = color_category.replace(center_class+"/","")
        compared_list.append([category_name, mapping_color_category_and_num[color_category], mapping_IR_category_and_num[infrared_category_path]])


nums_of_category = []
nums_row = []
for h in range(1,16):
    num = h*100
    nums_row.append("~"+str(num))
    num_of_category = 0
    for i in range(len(compared_list)):
        if int(compared_list[i][1])>=num and int(compared_list[i][2])>=num:
            num_of_category += 1
    nums_of_category.append(str(num_of_category))
print(nums_row)
print(nums_of_category)
with open(dataset_directory+save_file_name, 'w',newline='') as f:
    writer = csv.writer(f)

    writer.writerow(nums_row)
    writer.writerow(nums_of_category)
    writer.writerow([])
    writer.writerow(["Category","Color" ,"IR"])
    writer.writerows(compared_list)
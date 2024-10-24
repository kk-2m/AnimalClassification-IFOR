from PIL import Image
import json
import os

dataset_info_json_path = "../wcs/annotation/wcs_20220205_bboxes_with_classes.json"
root_directory = "../wcs/"
# WCS
wcs_directory = images_directory = root_directory + "wcs-unzipped/"
# Step 1
images_directory = root_directory + "images_with_classes/"
# Step 2
infrared_bboxes_directory = root_directory + "infrared_bboxes/"

with open(dataset_info_json_path) as f:
    dataset_info_json = json.load(f)

def isImage_gray(image):
    mode = image.mode
    if(mode == "L"):
        print("grey1")
        return True

    size = image.size

    if mode == "RGBA":
        if(len(set(image.getpixel((0, 0))))==2):
            if(len(set(image.getpixel((size[0]//2, size[1]//2))))==2):
                print("gray2")
                return True

    elif mode == "RGB":
        if(len(set(image.getpixel((0, 0))))==1):
            if(len(set(image.getpixel((size[0]//2, size[1]//2))))==1):
                print("gray3")
                return True
    return False

def mapping_dict_categoryid_to_name():
    category_dict = {}
    for categories_data in dataset_info_json["categories"]:
        category_dict[categories_data["id"]] = categories_data["name"]
    return category_dict

def save_image_to_category_folder(image, category_id, filename):
    new_folder_path = infrared_bboxes_directory + category_dictionary[category_id] +"/"

    if not os.path.isdir(new_folder_path):
        print("mkcategorydir:",new_folder_path)
        os.makedirs(new_folder_path)

    image.save(new_folder_path + filename + ".png")

def crop_image(image, bbox):
    return image.crop((bbox[0],bbox[1],bbox[0]+bbox[2],bbox[1]+bbox[3]))


# Step 1
for images_data in dataset_info_json["images"]:
    try:
        im = Image.open(images_directory + images_data["id"] + ".png")
        print("AlreadyFinished")
        print(images_directory + images_data["id"] + ".png")
        continue
    except Exception as e:
        print("NotYet")
        print(images_directory + images_data["id"] + ".png")
        pass

    try:
        im = Image.open(wcs_directory + images_data["file_name"])
        print("image path", wcs_directory + images_data["file_name"])
        im = im.convert("RGBA")
        im.save(images_directory + images_data["id"] + ".png")
    except Exception as e:
        print("Error:", e)

print("Step1 is completed")

category_dictionary = mapping_dict_categoryid_to_name()
print("mapping categoryID to Name is completed")

for annotation_data in dataset_info_json["annotations"]:
    width = 0
    height = 0

    try:
        im = Image.open(images_directory + annotation_data["image_id"] + ".png")
        print(images_directory + annotation_data["image_id"] + ".png")
        if isImage_gray(im):
            categoryID = annotation_data["category_id"]
            save_image_to_category_folder(crop_image(im,  annotation_data["bbox"]), categoryID, annotation_data["id"])

    except Exception as e:
        print("Error:", e)

print("Step2 is completed")
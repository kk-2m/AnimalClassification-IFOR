from PIL import Image
import json
import os

dataset_info_json_path = "../wcs/annotation/wcs_20220205_bboxes_with_classes.json"
root_directory = "../wcs/"
# Step 1
images_directory = root_directory + "images_with_classes/"
# Step2
saved_bboxes_directory = root_directory + "color_bboxes/"

with open(dataset_info_json_path) as f:
    dataset_info_json = json.load(f)

def isNotImage_gray(image):
    mode = image.mode
    if(mode == "L"):
        print("grey1")
        return False

    size = image.size

    if mode == "RGBA":
        if(len(set(image.getpixel((0, 0))))==2):
            if(len(set(image.getpixel((size[0]//2, size[1]//2))))==2):
                if(len(set(image.getpixel((size[0]//4, size[1]//4))))==2):
                    print("gray2")
                    return False
    elif mode == "RGB":
        if(len(set(image.getpixel((0, 0))))==1):
            if(len(set(image.getpixel((size[0]//2, size[1]//2))))==1):
                if(len(set(image.getpixel((size[0]//4, size[1]//4))))==1):
                    print("gray3")
                    return False
    else:
        print("othermode:", print(mode))
    return True

def mapping_dict_categoryid_to_name():
    category_dict = {}
    for categories_data in dataset_info_json["categories"]:
        category_dict[categories_data["id"]] = categories_data["name"]
    return category_dict

def create_save_folder():
    new_folder_path = saved_bboxes_directory + "/"

    if not os.path.isdir(new_folder_path):
        print("mk_savedir:",new_folder_path)
        os.makedirs(new_folder_path)

def save_image_to_category_folder(image, category_id, filename):
    new_folder_path = saved_bboxes_directory + category_dictionary[category_id] +"/"

    if not os.path.isdir(new_folder_path):
        print("mkcategorydir:",new_folder_path)
        os.makedirs(new_folder_path)

    image.save(new_folder_path + filename + ".png")

def crop_image(image, bbox):
    return image.crop((bbox[0],bbox[1],bbox[0]+bbox[2],bbox[1]+bbox[3]))


# step 2
category_dictionary = mapping_dict_categoryid_to_name()
print("mapping categoryID to Name is completed")

create_save_folder()

for annotation_data in dataset_info_json["annotations"]:
    width = 0
    height = 0

    try:
        im = Image.open(images_directory + annotation_data["image_id"] + ".png")
        if isNotImage_gray(im):
            categoryID = annotation_data["category_id"]
            save_image_to_category_folder(crop_image(im,  annotation_data["bbox"]), categoryID, annotation_data["id"])
    except Exception as e:
        print("Error:", e)

print("Step2 is completed")


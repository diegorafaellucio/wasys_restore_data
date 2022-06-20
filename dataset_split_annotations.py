import os
import shutil

# <annotation>
import os
import xml.etree.cElementTree as ET
from PIL import Image


CLASS_MAPPING = {
    '0': 'real'
    , '1': 'fake'

    # Add your remaining classes here.
}


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def create_root(file_prefix, width, height):
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "IMAGES"

    ET.SubElement(root, "filename").text = "{}.png".format(file_prefix)

    path = ET.SubElement(root, "path")
    path.text = os.path.join('./IMAGES', '{}.png'.format(file_prefix))

    source = ET.SubElement(root, "source")
    database = ET.SubElement(source, "database")
    database.text = 'Unknown'

    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"

    segmented = ET.SubElement(root, "segmented")
    segmented.text = '0'

    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(int(float(str(voc_label[1]))))
        ET.SubElement(bbox, "ymin").text = str(int(float(str(voc_label[2]))))
        ET.SubElement(bbox, "xmax").text = str(int(float(str(voc_label[3]))))
        ET.SubElement(bbox, "ymax").text = str(int(float(str(voc_label[4]))))
    return root


def create_file(file_prefix, width, height, voc_labels, destination_dir):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)

    indent(root)

    tree.write("{}/{}.xml".format(destination_dir, file_prefix))


def read_file(annotation_path, filename, images_path, destination_dir):
    file_prefix = filename.split(".txt")[0]
    image_file_name = "{}.png".format(file_prefix)
    img = Image.open("{}/{}".format(images_path, image_file_name))
    w, h = img.size
    with open(os.path.join(annotation_path, filename), 'r') as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(center_x - (bbox_width / 2))
            voc.append(center_y - (bbox_height / 2))
            voc.append(center_x + (bbox_width / 2))
            voc.append(center_y + (bbox_height / 2))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels, destination_dir)
    print("Processing complete for file: {}".format(filename))

classes_file = '/mnt/179d16f5-8902-4f77-a28f-f0d5e873778c/Wasys/experiments_estacio/data/names.txt'

images_dir = '/mnt/179d16f5-8902-4f77-a28f-f0d5e873778c/Wasys/IMAGES_ESTACIO'

new_images_dir = '/mnt/179d16f5-8902-4f77-a28f-f0d5e873778c/Wasys/NEW_ESTACIO'

def use_image(file_name):
    if 'scaled' in file_name:
        return False
    if 'flip' in file_name:
        return False
    if 'rotated' in file_name:
        return False
    if 'sheared' in file_name:
        return False
    return True


with open(classes_file) as f:
    classes = [line.rstrip() for line in f]

classes_dict = dict()

for i, classe in enumerate(classes):
    classes_dict[i] = classe.upper()

txt_image_files = [txt_file for txt_file in os.listdir(images_dir) if 'txt' in txt_file]

for k, txt_image_file in enumerate(txt_image_files):
    print('{}/{}'.format(k+1, len(txt_image_files)))

    if not use_image(txt_image_file):
        continue

    txt_image_file_path = os.path.join(images_dir, txt_image_file)


    with open(txt_image_file_path) as f:
        txt_data = [line.rstrip() for line in f]

        if len(txt_data) > 0:
            txt_data = txt_data[0].split(' ')
            # print(txt_data)
        else:
            txt_data = None


        if txt_data is not  None:

            classe = classes_dict[int(txt_data[0])]

            class_path = os.path.join(new_images_dir, classe)

            images_path = os.path.join(class_path, 'IMAGES')
            annotations_path = os.path.join(class_path, 'ANNOTATIONS')

            if not os.path.exists(class_path):
                os.mkdir(class_path)
                os.mkdir(images_path)
                os.mkdir(annotations_path)

            read_file(images_dir, txt_image_file, images_path, annotations_path)



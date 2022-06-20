import xml.etree.ElementTree as ET
import os
import shutil
from pathlib import Path as pt
import cv2


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


def file_to_dict(file_path):
    dict = {}
    with open(file_path, "r") as ins:
        for line in ins:
            line = line.replace('\n', '')
            line_data = line.split(' ')
            # print(line)

            first_element = line_data[0].split('/')[-2].split('_')[0]
            second_element = line_data[0].split('/')[-2].split('_')[1]
            third_element = line_data[0].split('/')[-1].split('.')[0]




            id = '{}-{}_{}'.format(first_element, second_element, third_element)

            parent = pt(line_data[0]).parent
            file_name = "{}.{}".format(id, line_data[0].split('/')[-1].split('.')[-1])

            path = os.path.join(parent,'IMAGES',file_name)
            category = int(line_data[1])
            postions = line_data[2:]
            dict[id] = [path, category, postions]

        # print(dict)

    return dict



def generate_xml(image_path, files_path,annotation_path, object_name):

    image_path = os.path.join(files_path, image_path)

    image = cv2.imread(image_path)

    height_size, width_size, _ = image.shape


    xmin_value = int(10)
    ymin_value = int(10)
    xmax_value = height_size - 10
    ymax_value = width_size -10


    # print(path_string)



    root = ET.Element('annotation')

    folder = ET.SubElement(root, "folder")
    folder.text = image_path.split('/')[-2]

    filename = ET.SubElement(root, "filename")
    filename.text = image_path.split('/')[-1]

    path = ET.SubElement(root, "path")
    path.text = image_path

    source = ET.SubElement(root, "source")
    database = ET.SubElement(source, "database")
    database.text = 'Unknown'



    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(width_size)
    height = ET.SubElement(size, "height")
    height.text = str(height_size)
    depth = ET.SubElement(size, "depth")
    depth.text = str(3)

    segmented = ET.SubElement(root, "segmented")
    segmented.text = '0'


    object = ET.SubElement(root, 'object')

    name = ET.SubElement(object, "name")
    name.text = object_name

    pose = ET.SubElement(object, "pose")
    pose.text = "Unspecified"

    truncated = ET.SubElement(object, "truncated")
    truncated.text = "0"

    difficult = ET.SubElement(object, "difficult")
    difficult.text = "0"

    bndbox = ET.SubElement(object, "bndbox")

    xmin = ET.SubElement(bndbox, "xmin")
    xmin.text = str(xmin_value)

    ymin = ET.SubElement(bndbox, "ymin")
    ymin.text = str(ymin_value)

    xmax = ET.SubElement(bndbox, "xmax")
    xmax.text = str(xmax_value)

    ymax = ET.SubElement(bndbox, "ymax")
    ymax.text = str(ymax_value)


    indent(root)

    # ET.dump(root)

    ET.ElementTree(root).write(
        os.path.join(annotation_path, image_path.split('/')[-1].replace('png', 'xml').replace('jpg', 'xml')))




def transform_image_to_xml(dataset_path):


    files_path = os.path.join(dataset_path,'IMAGES')
    annotations_path = os.path.join(dataset_path,'ANNOTATIONS')

    if os.path.exists(annotations_path):
        shutil.rmtree(annotations_path)
        os.mkdir(annotations_path)
    else:
        os.mkdir(annotations_path)

    files = [file for file in os.listdir(files_path) if 'png' in file or 'jpg' in file ]


    for i, file in enumerate(files):
        print('{}/{}'.format(i+1, len(files)))
        # print(dict_label)
        generate_xml(file,files_path,  annotations_path, 'real')



if __name__ == '__main__':
    transform_image_to_xml('/mnt/d/Empresas/Wasys/databases/mesa/COMPROVANTE_RENDIMENTO_PR')
    #
    # for base in bases:
    #     for type in types:
    #
    #         output_annotations_dir = '/home/diego/datasets/VISOB/{}/{}/ANNOTATIONS'.format(base, type)
    #
    #         iris_annotations_txt = '/home/diego/tools/label/video_annotator/visob/iris/{}-{}.txt'.format(base, type)
    #         eye_annotations_txt = '/home/diego/tools/label/video_annotator/visob/eye/{}-{}.txt'.format(base, type)
    #
    #         iris_data = pd.read_csv(iris_annotations_txt, header=None, sep=" ")
    #         eye_data = pd.read_csv(eye_annotations_txt, header=None, sep=" ")
    #
    #         shape = iris_data.shape
    #
    #         for i in range(shape[0]):
    #

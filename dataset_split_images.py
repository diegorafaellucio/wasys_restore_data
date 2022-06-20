import os
import shutil


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
    classes_dict[i] = classe.upper().replace("_"," ")

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




            image_path = os.path.join(images_dir, txt_image_file.replace('txt', 'png'))
            new_image_path = os.path.join(images_path, txt_image_file.replace('txt', 'png'))

            shutil.copy(image_path, new_image_path)

            # print(image_path)
            # print(len(txt_data))
            # if len(txt_data) != 5:
            #     print(txt_image_file_path)
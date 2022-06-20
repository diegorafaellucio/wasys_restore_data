import os
import shutil
import math
import cv2


def fileGenerator(data, file_name):
    file = open(file_name, "a+")
    for i in range(len(data)):
        file.write("{}\n".format(data[i][0]))
    file.close()


def remove_error_png(dataset_path):

    for root, persons, _ in os.walk(dataset_path):

        for person in persons:
            if 'DATA' not in person:

                person_path = os.path.join(root, person)


                person_images_path = os.path.join(person_path,'IMAGES')

                images = [ os.path.join(person_images_path,file) for file in os.listdir(person_images_path) if 'png' in file]

                for image in images:
                    try:
                        img = cv2.imread(image)
                    except:
                        print(image)
                        # os.remove(image)

        break








remove_error_png('/mnt/179d16f5-8902-4f77-a28f-f0d5e873778c/Wasys/NEW_ESTACIO')

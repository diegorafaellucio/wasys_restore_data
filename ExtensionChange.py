import os
import shutil
import math
import cv2

path = "/mnt/d/Empresas/Wasys/databases/mesa/EXTRATO_PAGAMENTO/IMAGES"

files = [image for image in os.listdir(path) if 'png' in image or 'jpg' in image]
for file_index, file_name in enumerate(files):
    print('{}/{}'.format(file_index + 1, len(files)))
    file_path = os.path.join(path, file_name)

    new_file_name = "{}.{}".format(file_path.split('.')[0], "jpg")
    img = cv2.imread(file_path)
    os.remove(file_path)
    cv2.imwrite(new_file_name, img)


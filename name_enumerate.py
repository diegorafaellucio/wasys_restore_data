import os
import shutil
import math
import cv2

path = "/mnt/d/Empresas/Wasys/databases/mesa/EXTRATO_PAGAMENTO/IMAGES/"

files = os.listdir(path)

for file_index, file_name in enumerate(files):
    print('{}/{}'.format(file_index + 1, len(files)))
    extension = str(os.path.splitext(file_name)[-1]).lower()
    new_file_name = '{}{}'.format(file_index, extension)

    original_file_path = os.path.join(path, file_name)
    new_file_path = os.path.join(path, new_file_name)

    shutil.move(original_file_path, new_file_path)


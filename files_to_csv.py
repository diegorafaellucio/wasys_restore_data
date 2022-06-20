import os
import shutil
import math
import cv2

path = "/home/diego/crucial/Empresas/Wasys/comgas/IMAGES"

lines = []

cabecalho = ['arquivo', 'nome_cliente', 'rua', 'numero', 'complemento', 'cep', 'uda']

lines.append(cabecalho)

files = [image for image in os.listdir(path) if 'png' in image or 'jpg' in image]
for file_index, file_name in enumerate(files):
    line = []
    line.append(file_name)
    lines.append(line)

with open('comgas.csv','w') as f:
    for line in lines:
        f.write( '{}\n'.format(','.join(line)) )
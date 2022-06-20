import os
import shutil
import math
import random

classes = ['709_1', '709_2', '5049_001_1', '5049_001_5', '6241_003', '6241_497E_1', '6241_497E_6', '6241_576E',
           '6241_688E_1', '6241_688E_2', 'ADF', 'CARTEIRA_DE_IDENTIDADE_MILITAR_FRENTE',
           'CARTEIRA_DE_IDENTIDADE_MILITAR_VERSO', 'CNH',
           'COMPROVANTE_RENDIMENTO_SIAPE', 'RG_FRENTE', 'RG_VERSO']


def fileGenerator(data, file_name):
    file = open(file_name, "a+")
    for i in range(len(data)):
        file.write("{}\n".format(data[i][0]))
    file.close()


def generateDatabase(dataset_path):
    eval = 0.1
    test = 0.2
    train = 0.7


    dataset_dir = os.path.join(dataset_path, 'DATA')

    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)
    os.makedirs(dataset_dir)

    eval_file = os.path.join(dataset_dir, "eval.txt")
    train_file = os.path.join(dataset_dir, "train.txt")
    test_file = os.path.join(dataset_dir, "test.txt")

    eval_data = []
    train_data = []
    test_data = []

    images = []

    subsets = os.listdir(dataset_path)


    for subset in subsets:
        if subset in classes:

            subset_path = os.path.join(dataset_path, subset)

            subset_images_path = os.path.join(subset_path,'IMAGES')
            subset_annotations_path = os.path.join(subset_path,'ANNOTATIONS')

            images = images + [os.path.join('database',subset, 'IMAGES',file) for file in os.listdir(subset_images_path) if 'jpg' in file or 'png' in file]

    random.shuffle(images)

    files_amount = len(images)

    eval_amount = int(math.floor(files_amount * eval))
    train_amount = int(math.floor(files_amount * train))
    test_amount = int(math.floor(files_amount * test))





    for image in images:

        if len(eval_data) < eval_amount:
            eval_data.append([image])
        elif len(train_data) < train_amount:
            train_data.append([image])
        else:
            test_data.append([image])




    fileGenerator(eval_data, eval_file)
    fileGenerator(train_data, train_file)
    fileGenerator(test_data, test_file)






generateDatabase('/mnt/d/darknet/database')

import os
import shutil
import math


def fileGenerator(data, file_name):
    file = open(file_name, "w")
    for i in range(len(data)):
        file.write("{}\n".format(data[i][0]))
    file.close()


def generateDatabase(dataset):
    eval = 0.2
    test = 0.4
    train = 0.4

    images_path = os.path.join(dataset, 'IMAGES')

    images = os.listdir(images_path)

    images = [image for image in images if 'png' in image]

    files_amount = len(images)

    eval_amount = int(math.floor(files_amount * eval))
    train_amount = int(math.floor(files_amount * train))
    test_amount = int(math.floor(files_amount * test))

    dataset_dir = os.path.join(dataset, 'DATA')
    eval_file = os.path.join(dataset_dir, "eval.txt")
    train_file = os.path.join(dataset_dir, "train.txt")
    test_file = os.path.join(dataset_dir, "test.txt")

    eval_data = []
    train_data = []
    test_data = []

    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)
    os.makedirs(dataset_dir)

    for i in range(len(images)):

        image = os.path.join(images_path, images[i])



        if len(eval_data) < eval_amount:
            eval_data.append([image])
        elif len(train_data) < train_amount:
            train_data.append([image])
        else:
            test_data.append([image])

    fileGenerator(eval_data, eval_file)
    fileGenerator(train_data, train_file)
    fileGenerator(test_data, test_file)


generateDatabase('/media/diego/2A7B42A077B46939/estacio')

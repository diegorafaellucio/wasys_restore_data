import os
import shutil
from pdf2image import convert_from_path, convert_from_bytes

print(os.getcwd())

docs_dir = '/mnt/d/Empresas/Wasys/databases/mesa/EXTRATO_PAGAMENTO/IMAGES'

docs = [doc for doc in os.listdir(docs_dir) if 'pdf' in doc]

for j, doc in enumerate(docs):
    print('{}/{}'.format(j+1, len(docs)), doc)

    doc_name = doc.split('.')[0]
    images = convert_from_path(os.path.join(docs_dir, doc))

    for i, image in enumerate(images):
        image.save(os.path.join(docs_dir,'{}_{}.png'.format(doc_name, i)), 'PNG')

    os.remove(os.path.join(docs_dir, doc))


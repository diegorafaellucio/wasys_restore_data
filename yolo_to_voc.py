# Script to convert yolo annotations to voc format

# Sample format
# <annotation>
#     <folder>_image_fashion</folder>
#     <filename>brooke-cagle-39574.jpg</filename>
#     <size>
#         <width>1200</width>
#         <height>800</height>
#         <depth>3</depth>
#     </size>
#     <segmented>0</segmented>
#     <object>
#         <name>head</name>
#         <pose>Unspecified</pose>
#         <truncated>0</truncated>
#         <difficult>0</difficult>
#         <bndbox>
#             <xmin>549</xmin>
#             <ymin>251</ymin>
#             <xmax>625</xmax>
#             <ymax>335</ymax>
#         </bndbox>
#     </object>
# <annotation>
import os
import xml.etree.cElementTree as ET
from PIL import Image

CLASS_MAPPING = {
    '0': 'boletim_desempenho_enem'
    , '1': 'certidao_de_casamento'
    , '2': 'certidao_de_divorcio'
    , '3': 'certidao_de_nascimento'
    , '4': 'certidao_de_obito'
    , '5': 'certificado_de_proficiencia_equivalente_a_conclusao_do_ensino_medio'
    , '6': 'cnh'
    , '7': 'comprovante_conclusao_ensino_medio'
    , '8': 'comprovante_de_efetivo_exercicio_do_magisterio'
    , '9': 'comprovante_de_equivalencia_expedido_pela_secretaria_de_educacao'
    , '10': 'comprovante_de_percepcao_de_bolsa_de_estudo_integral'
    , '11': 'comprovante_de_residencia'
    , '12': 'comprovantes_de_rendimento'
    , '13': 'contrato_de_prestacao_de_servicos_educacionais_assinado'
    , '14': 'contrato_do_financiamento'
    , '15': 'cpf'
    , '16': 'ctps'
    , '17': 'decisao_judicial_acordo_judicial_escritura_publica_de_pagamento_de_pensao_alimenticia'
    , '18': 'declaracao_de_abandono_de_lar'
    , '19': 'declaracao_de_criterios_socioeconomicos'
    , '20': 'declaracao_de_divorcio'
    , '21': 'declaracao_de_regularidade_junto_ao_enade'
    , '22': 'diploma_de_conclusao_do_ensino_medio'
    , '23': 'diploma_de_graduacao_revalidado_em_universidade_publica_brasileira'
    , '24': 'documento_comprobatorio_de_escolaridade_do_ensino_superior'
    , '25': 'documento_de_adiantamento'
    , '26': 'documento_de_manutencao_da_bolsa'
    , '27': 'documento_de_regularidade_de_inscricao_dri'
    , '28': 'documentos_para_aproveitamento_de_disciplinas'
    , '29': 'exame_nacional_para_certificacao_de_jovens_e_adultos_encceja'
    , '30': 'ficha_de_inscricao'
    , '31': 'historico_escolar'
    , '32': 'historico_escolar_oficial_do_ensino_superior'
    , '33': 'laudo_medico_atestado_deficiencia'
    , '34': 'reservista_frente'
    , '35': 'reservista_verso'
    , '36': 'rg'
    , '37': 'rg_frente'
    , '38': 'rg_verso'
    , '39': 'termo_de_concessao_de_bolsa_tcb'
    , '40': 'titulo_de_eleitor'
    , '41': 'uniao_estavel'
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

    ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)

    path = ET.SubElement(root, "path")
    path.text = os.path.join('./IMAGES', '{}.jpg'.format(file_prefix))

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


def read_file(file_path, annotations_dir, destination_dir):
    images_dir = annotations_dir.replace('ANNOTATIONS_TXT', 'IMAGES')
    file_prefix = file_path.split(".txt")[0]
    image_file_name = "{}.jpg".format(file_prefix)
    img = Image.open("{}/{}".format(images_dir, image_file_name))
    w, h = img.size
    with open(os.path.join(annotations_dir, file_path), 'r') as file:
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
    print("Processing complete for file: {}".format(file_path))


def start(ANNOTATIONS_DIR, DESTINATION_DIR):
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for filename in os.listdir(ANNOTATIONS_DIR):
        if filename.endswith('txt'):
            read_file(filename, ANNOTATIONS_DIR, DESTINATION_DIR)
        else:
            print("Skipping file: {}".format(filename))


if __name__ == "__main__":
    start('/home/diego/diego/ANNOTATIONS_TXT', '/home/diego/diego/ANNOTATIONS')

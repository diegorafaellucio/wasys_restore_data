import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil

# classes = ['boletim_desempenho_enem','certidao_de_casamento','certidao_de_divorcio','certidao_de_nascimento','certidao_de_obito','certificado_de_proficiencia_equivalente_a_conclusao_do_ensino_medio','cnh','comprovante_conclusao_ensino_medio','comprovante_de_efetivo_exercicio_do_magisterio','comprovante_de_equivalencia_expedido_pela_secretaria_de_educacao','comprovante_de_percepcao_de_bolsa_de_estudo_integral','comprovante_de_residencia','comprovantes_de_rendimento','contrato_de_prestacao_de_servicos_educacionais_assinado','contrato_do_financiamento','cpf','ctps','decisao_judicial_acordo_judicial_escritura_publica_de_pagamento_de_pensao_alimenticia','declaracao_de_abandono_de_lar','declaracao_de_criterios_socioeconomicos','declaracao_de_divorcio','declaracao_de_regularidade_junto_ao_enade','diploma_de_conclusao_do_ensino_medio','diploma_de_graduacao_revalidado_em_universidade_publica_brasileira','documento_comprobatorio_de_escolaridade_do_ensino_superior','documento_de_adiantamento','documento_de_manutencao_da_bolsa','documento_de_regularidade_de_inscricao_dri','documentos_para_aproveitamento_de_disciplinas','exame_nacional_para_certificacao_de_jovens_e_adultos_encceja','ficha_de_inscricao','historico_escolar','historico_escolar_oficial_do_ensino_superior','laudo_medico_atestado_deficiencia','reservista_frente','reservista_verso','rg_frente','rg_verso','termo_de_concessao_de_bolsa_tcb','titulo_de_eleitor','uniao_estavel']
# classes = ['fake', 'real']
# classes = ['IRPF', 'IR_RECIBO', 'CNH', 'CNPJ', 'COMP_ENDERECO',  'RG_FRENTE', 'RG_VERSO', ]
classes = ['709_1', '709_2', '5049_001_1', '5049_001_5', '6241_003', '6241_497E_1', '6241_497E_6', '6241_576E',
           '6241_688E_1', '6241_688E_2', 'ADF', 'CARTEIRA_DE_IDENTIDADE_MILITAR_FRENTE',
           'CARTEIRA_DE_IDENTIDADE_MILITAR_VERSO', 'CNH',
           'COMPROVANTE_RENDIMENTO_SIAPE', 'RG_FRENTE', 'RG_VERSO']
refulgo_output_path = 'refulgo'
output_classes = {}

black_list = {'CARTA_DE_CONCESSAO', 'COMPROVANTE_RENDIMENTO_BA', 'COMPROVANTE_RENDIMENTO_EXERCITO',
              'COMPROVANTE_RENDIMENTO_MARINHA', 'COMPROVANTE_RENDIMENTO_MS', 'COMPROVANTE_RENDIMENTO_PE',
              'COMPROVANTE_RENDIMENTO_PR', 'COMPROVANTE_RENDIMENTO_PR_PREV', 'CTPS', 'EXTRATO_PAGAMENTO', 'HISCON', 'HISCRE'}


# classes = ['5049-001', '6241-497E', 'documento_militar_frente', 'documento_militar_verso', 'cnh', 'comprovante_de_rendimento', 'autorizacao_desconto', 'fbp_756', 'fbp_6241_003', 'rg_frente', 'rg_verso', 'simulador']


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]

    if w < 0:
        w = box[0] - box[1]

    h = box[3] - box[2]

    if h < 0:
        h = box[2] - box[3]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(input_file, output_file):
    in_file = open(input_file)
    out_file = open(output_file, 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()

    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text.upper()

        if cls not in output_classes:
            output_classes[cls] = [input_file]
        else:
            paths = output_classes[cls]
            paths.append(input_file)
            output_classes[cls] = paths

        if cls not in classes or int(difficult) == 1:
            continue

        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    out_file.close()


def generate_labels(dataset_path):
    for dataset, subset, _ in os.walk(dataset_path):
        for subset in subset:

            if 'DATA' not in subset:

                class_path = os.path.join(dataset, subset)

                images = os.path.join(class_path, 'IMAGES')
                annotations_path = os.path.join(class_path, 'ANNOTATIONS')

                annotations = os.listdir(annotations_path)

                for annotation in annotations:
                    if 'xml' in annotation:
                        annotation_xml = os.path.join(annotations_path, annotation)
                        print(annotation_xml)
                        annotation_txt = os.path.join(images,
                                                      annotation_xml.replace('xml', 'txt').split('/')[-1])
                        convert_annotation(annotation_xml, annotation_txt)

        break
    print(output_classes)


if __name__ == '__main__':
    dataset_path = '/mnt/d/Empresas/Wasys/databases/mesa'
    generate_labels(dataset_path)

    if os.path.exists(refulgo_output_path):
        shutil.rmtree(refulgo_output_path)
        os.mkdir(refulgo_output_path)
    else:
        os.mkdir(refulgo_output_path)

    for class_key, class_items in output_classes.items():
        if class_key not in classes:
            subset_path = os.path.join(dataset_path, class_key)
            refulgo_class_output_path = os.path.join(refulgo_output_path, class_key)
            os.mkdir(refulgo_class_output_path)

            images_refulgo_class_output_path = os.path.join(refulgo_class_output_path, 'IMAGES')
            annotations_refulgo_class_output_path = os.path.join(refulgo_class_output_path, 'ANNOTATIONS')

            os.mkdir(images_refulgo_class_output_path)
            os.mkdir(annotations_refulgo_class_output_path)

            for xml_path in class_items:
                image_path = xml_path.replace('.xml', '.png').replace('ANNOTATIONS', 'IMAGES')
                file_name = xml_path.split('/')[-1].split('.')[0]
                print(file_name)
                image_new_path = os.path.join(
                    os.path.join(images_refulgo_class_output_path, '{}.png'.format(file_name)))
                annotation_new_path = os.path.join(
                    os.path.join(annotations_refulgo_class_output_path, '{}.xml'.format(file_name)))

                if os.path.exists(image_path):
                    shutil.move(image_path, image_new_path)
                if os.path.exists(xml_path):
                    shutil.move(xml_path, annotation_new_path)

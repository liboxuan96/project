import xml.etree.ElementTree as ET
import os
from os import listdir, getcwd

sets = ['train', 'test', 'val']

classes = ["5_23", "5_24", "5_25", "6_23", "6_24", "6_25", "7_23", "7_24", "7_25"]  # 所有类别的名称


def convert(size, box):#对图片进行归一化处理
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    y = y * dh
    w = w * dw
    h = h * dh
    x1 = box[4] * dw
    y1 = box[5] * dh
    x2 = box[6] * dw
    y2 = box[7] * dh
    x3 = box[8] * dw
    y3 = box[9] * dh
    x4 = box[10] * dw
    y4 = box[11] * dh

    # return (x, y, w, h)
    return (x, y, w, h, x1, y1, x2, y2, x3, y3, x4, y4)


def convert_annotation(image_id):
    in_file = open('data/Annotations/%s.xml' % (image_id))
    out_file = open('data/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text), float(xmlbox.find('x1').text), float(xmlbox.find('y1').text),
             float(xmlbox.find('x2').text), float(xmlbox.find('y2').text), float(xmlbox.find('x3').text),
             float(xmlbox.find('y3').text), float(xmlbox.find('x4').text), float(xmlbox.find('y4').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()
print(wd)
for image_set in sets:
    if not os.path.exists('data/labels/'):
        os.makedirs('data/labels/')
    image_ids = open('data/ImageSets/%s.txt' % (image_set)).read().strip().split()
    list_file = open('data/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write('data/images/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()
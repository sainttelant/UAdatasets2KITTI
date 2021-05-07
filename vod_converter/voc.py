"""
Ingestor and egestor for VOC formats.

http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html
"""

import os
import shutil

"""
访问到根目录
"""
import sys
sys.path.append("../Kitti2voc")

from GetImgName import *
from converter import Ingestor, Egestor
import xml.etree.ElementTree as ET

class VOCIngestor(Ingestor):
    def validate(self, root):
        self.n = 0
        path = f"{root}/VOC"
        for subdir in ["ImageSets", "JPEGImages", "Annotations"]:
            if not os.path.isdir(f"{path}/{subdir}"):
                return False, f"Expected subdirectory {subdir} within {path}"
            if not os.path.isfile(f"{path}/ImageSets/Main/trainval.txt"):
                #先校验一下 trainval.txt
                return False, f"Expected main image set ImageSets/Main/trainval.txt to exist within {path}"
            else:
                if self.n == 0:
                    os.remove(f"{path}/ImageSets/Main/trainval.txt")
                    print("重新根据JPEGImages生成正确的trainval.txt")
                    picpath = f"{path}/JPEGImages"
                    k = aquireDetails(picpath)

                    a = judgeFiles(picpath, k)
                    print("a:",a)
                    with open(f"{path}/ImageSets/Main/trainval.txt", "w+") as f:
                        saveFileNameIntotxt(f, a)
                    f.close()
                    print("finish aquire jpeg files'names")
                    self.n = self.n + 1

        return True, None

    def ingest(self, path):
        image_names = self._get_image_ids(path)
        return [self._get_image_detection(path, image_name) for image_name in image_names]

    def _get_image_ids(self, root):
        path = f"{root}/VOC"
        with open(f"{path}/ImageSets/Main/trainval.txt") as f:
            fnames = []
            for line in f.read().strip().split('\n'):
                cols = line.split()
                if len(cols) > 1:
                    score = cols[1]
                    if score != '1':
                        continue
                fnames.append(cols[0])
            return fnames

    def _get_image_detection(self, root, image_id):
        path = f"{root}/VOC"
        image_path = f"{path}/JPEGImages/{image_id}.jpg"
        if not os.path.isfile(image_path):
            raise Exception(f"Expected {image_path} to exist.")
        annotation_path = f"{path}/Annotations/{image_id}.xml"
        if not os.path.isfile(annotation_path):
            raise Exception(f"Expected annotation file {annotation_path} to exist.")
        tree = ET.parse(annotation_path)
        xml_root = tree.getroot()
        size = xml_root.find('size')
        print("size:",size)
        print("xml_root",xml_root)

        """
        segmented = xml_root.find('segmented').text == '1'
        segmented_path = None
        if segmented:
            segmented_path = f"{path}/SegmentationObject/{image_id}.png"
            if not os.path.isfile(segmented_path):
                raise Exception(f"Expected segmentation file {segmented_path} to exist.")
        """

        image_width = int(size.find('width').text)
        image_height = int(size.find('height').text)
        return {
            'image': {
                'id': image_id,
                'path': image_path,
                #'segmented_path': segmented_path,
                'width': image_width,
                'height': image_height
            },
            'detections': [self._get_detection(node) for node in xml_root.findall('object')]
        }

    def _get_detection(self, node):
        bndbox = node.find('bndbox')
        return {
            'label': node.find('name').text,
            'top': float(bndbox.find('ymin').text) - 1,
            'left': float(bndbox.find('xmin').text) - 1,
            'right': float(bndbox.find('xmax').text) - 1,
            'bottom': float(bndbox.find('ymax').text) - 1,
        }


class VOCEgestor(Egestor):

    def expected_labels(self):
        return {
            'aeroplane': [],
            'cyclist': [],
            'bird': [],
            'boat': [],
            'bottle': [],
            'bus': [],
            'Car': [],
            'cat': [],
            'chair': [],
            'cow': [],
            'diningtable': [],
            'dog': [],
            'horse': [],
            'motorbike': [],
            'pedestrian': ['pedestrian'],
            'pottedplant': [],
            'sheep': [],
            'sofa': [],
            'train': [],
            'tvmonitor': []
        }

    def egest(self, *, image_detections, root):
        image_sets_path = f"{root}/VOC/ImageSets/Main"
        images_path = f"{root}/VOC/JPEGImages"
        annotations_path = f"{root}/VOC/Annotations"
        segmentations_path = f"{root}/VOC/SegmentationObject"
        segmentations_dir_created = False

        for to_create in [image_sets_path, images_path, annotations_path]:
            os.makedirs(to_create, exist_ok=True)

        for image_detection in image_detections:
            image = image_detection['image']
            image_id = image['id']
            src_extension = image['path'].split('.')[-1]
            shutil.copyfile(image['path'], f"{images_path}/{image_id}.{src_extension}")

            with open(f"{image_sets_path}/trainval.txt", 'a') as out_image_index_file:
                out_image_index_file.write(f'{image_id}\n')

            if image['segmented_path'] is not None:
                if not segmentations_dir_created:
                    os.makedirs(segmentations_path)
                    segmentations_dir_created = True
                shutil.copyfile(image['segmented_path'], f"{segmentations_path}/{image_id}.png")

            xml_root = ET.Element('annotation')
            add_text_node(xml_root, 'filename', f"{image_id}.{src_extension}")
            add_text_node(xml_root, 'folder', 'VOC')
            add_text_node(xml_root, 'segmented', int(segmentations_dir_created))

            add_sub_node(xml_root, 'size', {
                'depth': 3,
                'width': image['width'],
                'height': image['height']
            })
            add_sub_node(xml_root, 'source', {
                'annotation': 'Dummy',
                'database': 'Dummy',
                'image': 'Dummy'
            })

            for detection in image_detection['detections']:

                if detection["label"] == "car" and detection['left'] < 100 and detection['left'] > 50 and detection['right'] > 110 and detection["right"] < 190:

                    print("this is left top wrong detection 20 as car!!,remove")
                    continue

                if detection["label"] == "Person" and detection['left'] < 2270 and detection['left']>2255 \
                and detection['right'] \
                > 2280 and detection['right'] < 2300:
                    continue
                else:
                    
                    x_object = add_sub_node(xml_root, 'object', {
                        'name': detection['label'],
                        'difficult': 0,
                        'occluded': 0,
                        'truncated': 0,
                        'pose': 'Unspecified'
                    })
                    add_sub_node(x_object, 'bndbox', {
                        'xmin': detection['left'] + 1,
                        'xmax': detection['right'] + 1,
                        'ymin': detection['top'] + 1,
                        'ymax': detection['bottom'] + 1
                    })

            ET.ElementTree(xml_root).write(f"{annotations_path}/{image_id}.xml")


def add_sub_node(node, name, kvs):
    subnode = ET.SubElement(node, name)
    for k, v in kvs.items():
        add_text_node(subnode, k, v)
    return subnode


def add_text_node(node, name, text):
    subnode = ET.SubElement(node, name)
    subnode.text = f"{text}"
    return subnode








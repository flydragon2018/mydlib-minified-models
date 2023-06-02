import cv2
import dlib
import os
import re

import xml.dom.minidom

# regex:
REG_PART = re.compile("part name='[0-9]+'")
REG_NUM = re.compile("[0-9]+")

# landmarks subsets (relative to 68-landmarks):
EYE_EYEBROWS = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 36, 37, 38, 39,
                40, 41, 42, 43, 44, 45, 46, 47]
NOSE_MOUTH = [27, 28, 29, 30, 31, 32, 33, 34, 35, 48, 49, 50, 51, 52,
              53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]
FACE_CONTOUR = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
#ALL_LANDMARKS = range(0, 68)
 

NECK = [101,102,103,104,105]

FACE_LANDMARKS = list(range(0, 68))

ALL_LANDMARKS=FACE_LANDMARKS+NECK 

# dataset path
ibug_dir = "ibug_300W_large_face_landmark_dataset"

# annotations
train_labels ="labels_ibug_300W_train.xml"
test_labels = "labels_ibug_300W_test.xml"


'''
  <image file='helen/testset/2986046144_1.jpg' width='798' height='1200'>
    <box top='116' left='45' width='643' height='643'>
     
'''

BOX=['top','left','width','height']

def convert_xml(in_path, out_path, parts):
    '''creates a new xml file stored at [out_path] with the desired landmark-points.
    The input xml [in_path] must be structured like the ibug annotation xml.'''
    file = open(in_path, "r")
    out = open(out_path, "w")
    pointSet = set(parts)

    doc=xml.dom.minidom.parse(in_path)
    
    images=doc.getElementsByTagName("image")

    boxes=doc.getElementsByTagName("box")

    print(images)
    print(boxes)

    '''
    for line in file.readlines():
        finds = re.findall(REG_PART, line)

        # find the part section
        if len(finds) <= 0:
            out.write(line)
        else:
            # we are inside the part section 
            # so we can find the part name and the landmark x, y coordinates
            name, x, y = re.findall(REG_NUM, line)

            # if is one of the point i'm looking for, write in the output file
            if int(name) in pointSet:
                out.write(f"      <part name='{name}' x='{x}' y='{y}'/>\n")

    out.close()
    '''


models = [
     # pair: model name, parts
    ("box", BOX),
]



for model_name, parts in models:
  print(f"processing model: {model_name}")
  
  train_xml = f"{model_name}_train.xml"
  test_xml = f"{model_name}_test.xml"
  dat = f"{model_name}.dat"
  convert_xml(train_labels, train_xml, parts)
  convert_xml(test_labels, test_xml, parts)
# -*- coding: utf-8 -*-
import numpy as np

annotation_path = "./config/train.txt"

class_names = [
    "person",
    "bicycle",
    "car",
    "motorbike",
    "aeroplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "sofa",
    "pottedplant",
    "bed",
    "diningtable",
    "toilet",
    "tvmonitor",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush"
]

num_classes = len(class_names)
input_shape = (416, 416)
lr = 1e-4
batch_size = 8
epochs = 100

ignore_thresh = 0.5
iou_threshold = 0.4

label_smooth = 0.05

valid_rate = 0.1
data_augmentation = "all"

anchors = np.array([(5, 9), (9, 16), (15, 26),
                    (23, 38), (34, 53), (49, 80),
                    (80, 119), (130, 179), (200, 243)],
                   np.float32)

anchor_masks = [[6, 7, 8], [3, 4, 5], [0, 1, 2]]
num_bbox = len(anchor_masks[0])

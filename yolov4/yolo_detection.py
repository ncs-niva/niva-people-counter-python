# Usage examples: python yolo_detection.py --video=data/test.mp4 --device 'cpu'
#                 python yolo_detection.py --video=data/test.mp4 --device 'gpu'
#                 python yolo_detection.py --image=data/people1.jpg --device 'cpu'
#                 python yolo_detection.py --image=data/people1.jpg --device 'gpu'

import argparse
import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np


# Define the helper functions
def image_show(path):
    image = cv2.imread(path)
    height, width = image.shape[:2]
    resized_image = cv2.resize(image, (3*width, 3*height), interpolation=cv2.INTER_CUBIC)

    fig = plt.gcf()
    fig.set_size_inches(18, 10)
    plt.axis("off")
    plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
    plt.show()


# Initializing the parameters
conf_threshold = 0.5  # Confidence threshold
nms_threshold = 0.4  # Non-maximum suppression threshold
inp_width = 416  # Width of network's input image
inp_height = 416  # Height of network's input image

parser = argparse.ArgumentParser(description='Object Detection using YOLOv4 in OPENCV')
parser.add_argument('--device', default='cpu', help="Device to perform inference on 'cpu' or 'gpu'.")
parser.add_argument('--image', help='Path to image file.')
parser.add_argument('--video', help='Path to video file.')
args = parser.parse_args()

# Loading the names of classes
classes_file = "./data/coco.names"
classes = None
with open(classes_file, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Giving the configuration and weight files for the model and load the network using them.
modelConfiguration = "./cfg/yolov4.cfg";
modelWeights = "./yolov4.weights";

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)

if args.device == 'cpu':
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    print('Using CPU device.')
elif args.device == 'gpu':
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    print('Using GPU device.')


# Getting the names of the output layers
def get_output_names(dummy_net):
    # Get the names of all the layers in the network
    layer_names = dummy_net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layer_names[i[0] - 1] for i in dummy_net.getUnconnectedOutLayers()]


# Drawing the predicted bounding box
def draw_pred(dummy_frame, class_id, conf, left, top, right, bottom):
    # Drawing a bounding box.
    cv2.rectangle(dummy_frame, (left, top), (right, bottom), (255, 178, 50), 3)
    dummy_label = '%.2f' % conf

    # Getting the label for the class name and its confidence
    if classes:
        assert (class_id < len(classes))
        dummy_label = '%s:%s' % (classes[class_id], dummy_label)

    # Displaying the label at the top of the bounding box
    label_size, base_line = cv2.getTextSize(dummy_label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, label_size[1])
    cv2.rectangle(dummy_frame, (left, top - round(1.5 * label_size[1])),
                  (left + round(1.5 * label_size[0]), top + base_line),
                  (255, 255, 255), cv2.FILLED)
    cv2.putText(dummy_frame, dummy_label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)


# Removing the bounding boxes with low confidence using non-maxima suppression
def postprocess(dummy_frame, dummy_outs):
    frame_height = dummy_frame.shape[0]
    frame_width = dummy_frame.shape[1]

    # Scanning through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    class_ids = []
    confidences = []
    boxes = []
    for out in dummy_outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                width = int(detection[2] * frame_width)
                height = int(detection[3] * frame_height)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Performing non-maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        draw_pred(dummy_frame, class_ids[i], confidences[i], left, top, left + width, top + height)


# Processing inputs
winName = 'Deep learning object detection in OpenCV'
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)


outputFile = "yolo_out_py.avi"


if args.image:
    # Opening the image file
    if not os.path.isfile(args.image):
        print("Input image file ", args.image, " doesn't exist")
        sys.exit(1)
    cap = cv2.VideoCapture(args.image)
    outputFile = args.image[:-4] + '_yolo_out_py.jpg'
elif args.video:
    # Opening the video file
    if not os.path.isfile(args.video):
        print("Input video file ", args.video, " doesn't exist")
        sys.exit(1)
    cap = cv2.VideoCapture(args.video)
    outputFile = args.video[:-4] + '_yolo_out_py.avi'
else:
    # Opening the webcam input
    cap = cv2.VideoCapture(0)

# Getting the video writer initialized to save the output video
if not args.image:
    vid_writer = cv2.VideoWriter(outputFile,
                                 cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                 30,
                                 (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

while cv2.waitKey(1) < 0:

    # Getting the frame from the video
    hasFrame, frame = cap.read()

    # Stopping the program if reached end of video
    if not hasFrame:
        print("Done processing")
        print("Output file is stored as ", outputFile)
        cv2.waitKey(3000)
        # Release device
        cap.release()
        break

    # Creating a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (inp_width, inp_height), [0, 0, 0], 1, crop=False)

    # Setting the input to the network
    net.setInput(blob)

    # Running the forward pass to get output of the output layers
    outs = net.forward(get_output_names(net))

    # Removing the bounding boxes with low confidence
    postprocess(frame, outs)

    # Putting in efficiency information.
    # The function getPerfProfile returns the overall time for inference(t)
    # and the timings for each of the layers(in layersTimes).
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    cv2.putText(frame, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    # Writing the frame with the detection boxes
    if args.image:
        cv2.imwrite(outputFile, frame.astype(np.uint8))
    else:
        vid_writer.write(frame.astype(np.uint8))

    cv2.imshow(winName, frame)

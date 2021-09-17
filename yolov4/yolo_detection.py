import subprocess

import cv2
import matplotlib.pyplot as plt


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


# Define the yolov4 detection function
def yolo_detect():
    subprocess.run([], capture_output=True)

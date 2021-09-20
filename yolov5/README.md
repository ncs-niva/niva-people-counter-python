# Working with `yolov5` from [Ultralytics](https://ultralytics.com/)

## Installation Instructions
The source code for `yolov5` can be found at https://github.com/ultralytics/yolov5. 
To use `yolov5`, first you will need to install the required dependencies, which can be downloaded with `pip` with the
following command line when you get to the root of the `yolov5` repository:
```commandline
pip install -r requiremennts.txt
```

## Usage Instructions
### Long Example
The following example shows batched inference with PIL and OpenCV image sources. 
The results can be printed to console, saved to "runs/hub", showed to screen on supported environments, 
and returned as tensors or pandas dataframes.

```python
import cv2
import torch
from PIL import Image

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Images
for f in ['zidane.jpg', 'bus.jpg']:
    torch.hub.download_url_to_file('https://ultralytics.com/images/' + f, f)  # download 2 images
img1 = Image.open('zidane.jpg')  # PIL image
img2 = cv2.imread('bus.jpg')[..., ::-1]  # OpenCV image (BGR to RGB)
imgs = [img1, img2]  # batch of images

# Inference
results = model(imgs, size=640)  # includes NMS

# Results
results.print()  
results.show()  # or .save()

results.xyxy[0]  # img1 predictions (tensor)
results.pandas().xyxy[0]  # img1 predictions (pandas)
#      xmin    ymin    xmax   ymax  confidence  class    name
# 0  749.50   43.50  1148.0  704.5    0.874023      0  person
# 1  433.50  433.50   517.5  714.5    0.687988     27     tie
# 2  114.75  195.75  1095.0  708.0    0.624512      0  person
# 3  986.00  304.00  1028.0  420.0    0.286865     27     tie
```
# NIVA People Counter in Python
A simple people counter application in Python using line counting

## Author
Kris Stern

## Inspiration
Inspired by https://github.com/IdoGalil/People-counting-system.

## Overview
The system counts the people entering and leaving an entrance as defined by some boundary, 
using a Deep Neural Network as a detector (YOLOv4) and a tracking algorithm to track and count (DCF-CSR/CSRT). 

## Dependencies & Requirements
* Python 3
* GPU with CUDA and cuDNN installed and enabled
* The Python-based packages in [requirements.txt](./requirements.txt)

## How to install the dependencies
For `yolov4` installation instructions, please see [yolov4 docs](./yolov4/README.md).
Otherwise, for installation of all other Python-based dependencies, please run the following command:

```shell
pip install -r requirements.txt
```

## How to generate the `.h5` model file for YOLOv4
Please navigate to [niva-people-counter-python/yolov4/](https://github.com/ncs-niva/niva-people-counter-python/tree/main/yolov4). While at this level, run the script `convert2h5.py` with the command:
```shell
python ./convert2h5.py
```
Once the process is done, the `yolov4.h5` model file can be file in the directory [niva-people-counter-python/yolov4/data/](https://github.com/ncs-niva/niva-people-counter-python/tree/main/yolov4/data).
Remember to check the configuration setting if there is any issue with the running of this script. 

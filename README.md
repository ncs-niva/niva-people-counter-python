# NIVA People Counter in Python - Work in Progress
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
* GPU with CUDA installed
* The Python-based packages in [requirements.txt](./requirements.txt)

## How to install
For `yolov4` installation instructions, please see [yolov4 docs](./yolov4/README.md).
Otherwise, for installation of all other Python-based dependencies, please run the following command:

```shell
pip install -r requirements.txt
```

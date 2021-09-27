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
* GPU with CUDA installed
* The Python-based packages in [requirements.txt](./requirements.txt)

## How to install
For `yolov4` installation instructions, please see [yolov4 docs](./yolov4/README.md).
Otherwise, for installation of all other Python-based dependencies, please run the following command:

```shell
pip install -r requirements.txt
```

## Installing `opencv` with CUDA support for Python
More detailed instructions can be found at https://learnopencv.com/how-to-use-opencv-dnn-module-with-nvidia-gpu-on-windows/. 
But a simplified version can be accessed below.

Make sure you have all the requirements for installing `yolov4` in the `darknet` framework satisfied, these can be found
at [`yolov4`'s README.md](./yolov4/README.md). 

Firstly, set the `opencv` version you would like to compile. For example:
```shell
set opencv-version=4.5.3
```

Then, clone the GitHub `opencv` and `opencv-contrib` repositories, and checkout the specific version desired
with the following commands at a current working directory using the Windows' CMD:

```shell
git clone https://github.com/opencv/opencv.git
cd opencv
git checkout tags/%opencv-version%
```

Then return go the current working directory. 

```shell
git clone https://github.com/opencv/opencv_contrib.git
cd opencv_contrib
git checkout tags/%opencv-version%
```

Next, we build `opencv` with CUDA support by running something similar to the following at the CMD:
```shell
cmake ^
-G "Visual Studio 16 2019" ^
-T host=x64 ^
-DCMAKE_BUILD_TYPE=RELEASE ^
-DCMAKE_INSTALL_PREFIX=C:/Users/kriss/OpenCV-%opencv-version% ^
-DOPENCV_EXTRA_MODULES_PATH=C:/Users/kriss/opencv_contrib/modules ^
-DINSTALL_PYTHON_EXAMPLES=ON ^
-DINSTALL_C_EXAMPLES=ON ^
-DPYTHON_EXECUTABLE=C:/Users/kriss/miniconda3/envs/niva-people-counter-python/python3 ^
-DPYTHON3_LIBRARY=C:/Users/kriss/miniconda3/envs/niva-people-counter-python/libs/python3 ^
-DWITH_CUDA=ON ^
-DWITH_CUDNN=ON ^
-DOPENCV_DNN_CUDA=ON ^
-DWITH_CUBLAS=ON ^
..
```

Note in the above is has been assumed the current working directory to be `C:/Users/kriss`. Also, note that `miniconda3`
has been used in this case in lieu of the alternative of `Anaconda3`. 

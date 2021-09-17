# Compiling `yolov4` in the `darknet` framework on Windows using `vcpkg`

According to https://github.com/AlexeyAB/darknet, this is the recommended approach to build `Darknet` on Windows.

## Preliminaries
Make sure you have the following requirements satisfied:

1. CMake >= 3.18
2. Powershell (already installed on Windows)
3. CUDA >= 10.2
4. OpenCV >= 2.4
5. cuDNN >= 8.0.2
6. GPU with CC >= 3.0

**Remarks**: 
* For info for WSL CUDA users please see https://docs.nvidia.com/cuda/wsl-user-guide/index.html.
* For downloading the CUDA driver please go to: https://developer.nvidia.com/cuda/wsl.
* Some features are restricted and are only available to members of 
the [Microsoft Windows Insider Program](https://insider.windows.com/en-us/getting-started/), as well as to
these members who are also registered in the [NVIDIA Developer Program](https://developer.nvidia.com/developer-program).
* It is recommended to sign up for the [Beta Channel](https://insider.windows.com/en-us/) of the 
Windows Insider Program and upgrade to Windows 11 for a more seamless developer experience.
* Make sure to set the environment variable `PATH` for both `ninja` and `vcpkg` before attempting to compile. 
* You may find the `ninja` executable as part of Visual Studio 2019 Community Edition, at a location similar to
`C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\ninja.exe`
* And for `vcpkg`, it is best to install it at a location called
`C:\src` as suggested in their official docs on GitHub: https://github.com/microsoft/vcpkg. 

## Installation Instructions
1. Install Visual Studio 2019. In case you need to download it, please download the Community Edition. 
Remember to install English language pack, as this is mandatory for `vcpkg`.
2. Install CUDA enabling VS Integration during installation from the link above in the [Preliminaries](#preliminaries).
3. Use Powershell to run the following commands one-by-one, at a directory such as `C:\Users\<username>`:
   ```bash
   Set-ExecutionPolicy unrestricted -Scope CurrentUser -Force
   git clone https://github.com/AlexeyAB/darknet.git
   cd darknet
   .\build.ps1 -UseVCPKG -EnableOPENCV -EnableCUDA -EnableCUDNN -EnableOPENCV_CUDA
   ```

The entire compilation process may take hours, so be prepared to set aside sufficient time to allow for monitoring its
completion. Once finished, you should be able to find the executable `darknet.exe` in the "root" `darknet` directory. 
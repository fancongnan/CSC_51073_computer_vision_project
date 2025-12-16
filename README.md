# CSC_51073_computer_vision_project
This project explores whether full-body gestures, tracked in real time from a webcam, can be used as an expressive and reliable control interface for music. Using Mediapipe for pose/gesture estimation and TouchDesigner for real-time audio-visual synthesis, we build an interactive system where users shape the sound with their body.

# Installing MediaPipe, OpenCV, NumPy, and Other Python Libraries in TouchDesigner

TouchDesigner uses its **own embedded Python environment**, so installing libraries like `mediapipe`, `opencv-python`, `numpy`, `scipy`, etc. requires pointing `pip` to TouchDesigner’s Python interpreter.

This guide explains how to:

1. Find TouchDesigner’s Python path  
2. Install packages using that interpreter   

---

## Find TouchDesigner’s Python Interpreter

Open **TouchDesigner → Textport** (Alt + T), then run:

```python
import sys
print(sys.executable)
```
---

## Install Packages Using TouchDesigner’s Python

You **must run pip using TouchDesigner’s python**, not the system python.

### **macOS install example**
```bash
"<TD_PYTHON_PATH>" -m pip install mediapipe opencv-python numpy
```e

---

# Executables

The executables are found in the MediaPipe/release folder and are the following:
1. cv_auditory_project : control audio samples with MediaPipe 
2. cv_visual_project : import mediapipe and use data to apply image treatment
3. cv_synth_project : synth control with MediaPipe

If cv_auditory_project doesn't work in the indicated folder, you can try with the file in the cv_auditory_project_backup folder.

These files may need some extra-configuration -> see the README for each one.
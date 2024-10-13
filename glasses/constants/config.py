# glasses/constants/config.py
import os
import cv2

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
GLASSES_IMAGES = [
    os.path.join(PROJECT_ROOT, "..", "data", "glasses1.png"),
    os.path.join(PROJECT_ROOT, "..", "data", "glasses2.png"),
    os.path.join(PROJECT_ROOT, "..", "data", "glasses3.png"),
    os.path.join(PROJECT_ROOT, "..", "data", "glasses4.png")
]

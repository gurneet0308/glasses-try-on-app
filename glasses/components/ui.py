# glasses/components/ui.py
import cv2
import numpy as np

def create_sidebar(glasses_images, current_glasses, frame_height):
    sidebar = np.zeros((frame_height, 100, 3), dtype=np.uint8)
    thumbnail_height = frame_height // len(glasses_images)
    for i, img in enumerate(glasses_images):
        y = i * thumbnail_height
        resized = cv2.resize(img[:, :, :3], (80, thumbnail_height - 20))
        sidebar[y + 10:y + thumbnail_height - 10, 10:90] = resized
        if i == current_glasses:
            cv2.rectangle(sidebar, (5, y + 5), (95, y + thumbnail_height - 5), (0, 255, 0), 2)
    return sidebar

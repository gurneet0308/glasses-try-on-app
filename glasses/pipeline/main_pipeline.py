# glasses/pipeline/main_pipeline.py
import cv2
import numpy as np
from glasses.components.image_processing import (
    load_glasses_image,
    overlay_image_alpha,
    rank_glasses_for_oval_face
)
from glasses.components.ui import create_sidebar
from glasses.constants.config import CASCADE_PATH, GLASSES_IMAGES

def main():
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    cap = cv2.VideoCapture(0)

    glasses_images = [load_glasses_image(img_path) for img_path in GLASSES_IMAGES]
    current_glasses = 0

    def mouse_callback(event, x, y, flags, param):
        nonlocal current_glasses
        if event == cv2.EVENT_LBUTTONDOWN:
            if x > frame.shape[1]:  # Click is in the sidebar
                clicked_glasses = y // (frame.shape[0] // len(glasses_images))
                if clicked_glasses < len(glasses_images):
                    current_glasses = clicked_glasses

    cv2.namedWindow('Glasses Try-On App')
    cv2.setMouseCallback('Glasses Try-On App', mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        sidebar = create_sidebar(glasses_images, current_glasses, frame.shape[0])
        combined_frame = np.hstack((frame, sidebar))

        for (x, y, w, h) in faces:
            glasses = cv2.resize(glasses_images[current_glasses], (w, int(h / 3)))
            glasses_pos = (x, y + int(h / 4))
            frame = overlay_image_alpha(frame, glasses, glasses_pos)

            # Calculate score for current glasses
            score = rank_glasses_for_oval_face(glasses.shape[1], w, h, current_glasses)

            # Draw a semi-transparent background for the score
            cv2.rectangle(frame, (10, 10), (250, 80), (0, 0, 0), -1)
            cv2.rectangle(frame, (10, 10), (250, 80), (0, 255, 0), 2)

            # Display the score with larger font
            cv2.putText(frame, f"Score:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"{score:.1f}/10", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        combined_frame = np.hstack((frame, sidebar))
        cv2.imshow('Glasses Try-On App', combined_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('n'):
            current_glasses = (current_glasses + 1) % len(glasses_images)

    cap.release()
    cv2.destroyAllWindows()

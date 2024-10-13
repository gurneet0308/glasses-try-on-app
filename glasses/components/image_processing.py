# glasses/components/image_processing.py
import cv2
import numpy as np
from PIL import Image

def overlay_image_alpha(img, img_overlay, pos):
    """Overlay img_overlay on top of img at the position specified by pos."""
    x, y = pos
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    overlay_image = img_overlay[y1 - y:y2 - y, x1 - x:x2 - x]
    img_crop = img[y1:y2, x1:x2]

    alpha = overlay_image[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha

    for c in range(0, 3):
        img_crop[:, :, c] = alpha * overlay_image[:, :, c] + alpha_inv * img_crop[:, :, c]

    img[y1:y2, x1:x2] = img_crop
    return img

def load_glasses_image(filename):
    """Load an image file and convert it to a format suitable for overlay."""
    img = Image.open(filename).convert("RGBA")
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)

def rank_glasses_for_oval_face(glasses_width, face_width, face_height, glasses_index):
    """Rank glasses for an oval face shape."""
    ideal_ratio = 1.5  # Ideal width-to-height ratio for oval faces
    face_ratio = face_width / face_height
    glasses_face_ratio = glasses_width / face_width

    # Score based on how close the glasses width is to the face width
    width_score = 10 - abs(glasses_face_ratio - 1) * 10

    # Score based on how well the glasses complement the face ratio
    ratio_score = 10 - abs(face_ratio - ideal_ratio) * 5

    # Add a unique factor for each pair of glasses
    unique_factor = [0.8, 1.0, 1.2, 0.9][glasses_index]

    # Combine scores
    total_score = (width_score * 0.5 + ratio_score * 0.3 + unique_factor * 2)
    return min(max(total_score, 0), 10)  # Ensure score is between 0 and 10

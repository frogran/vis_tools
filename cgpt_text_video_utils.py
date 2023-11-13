import cv2
import numpy as np


def get_direction_from_vector(vector):
    magnitude = np.linalg.norm(vector)
    return vector / magnitude


def get_lines(mask_img, vector, thickness):
    # TODO add to strength of line (thickness) based on distance from center (recommendation)
    # TODO add to strength of line (weak gray lines overlap and add up)
    lined_img = mask_img.copy()
    for y in range(0, mask_img.shape[0], thickness):
        for x in range(0, mask_img.shape[1], thickness):
            if mask_img[y, x] > 0:
                end_point = (x + int(vector[0]), y + int(vector[1]))
                # TODO change start and end point to be edges of img
                cv2.line(lined_img, (x, y), end_point, 255, 1)
    return lined_img


def get_sweep_pixel_groups(mask_img, vector, lines_img, thickness):
    pixel_groups = []
    for y in range(0, mask_img.shape[0], thickness):
        for x in range(0, mask_img.shape[1], thickness):
            if mask_img[y, x] > 0:
                # TODO pixel group should be sweep line intersection with lines
                pixel_groups.append((y, x))
    return pixel_groups


def create_video_without_blend(img_set, vw, text_img, show=False):
    for img in img_set:
        vw.write(img)
        if show:
            cv2.imshow('Video', img)
            cv2.waitKey(1)
    vw.write(text_img)
    if show:
        cv2.imshow('Video', text_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def create_video_with_blend(img_set, cap, blend, text_img, show=False):
    pass  # Implement blend functionality as required


def create_image_from_pixel_group(sweep_pixel_group, shape):
    img = np.zeros(shape, dtype=np.uint8)
    for y, x in sweep_pixel_group:
        img[y, x] = 255
    return img

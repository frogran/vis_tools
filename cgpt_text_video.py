import cv2
import numpy as np
import cgpt_text_video_utils as tvutils

class PlaneSweepForText:
    def __init__(self, text_img, vector, thickness=10, blend=None):
        self.text_img = text_img
        self.vector = tvutils.get_direction_from_vector(vector)
        self.thickness = thickness
        self.lined_img = tvutils.get_lines(self.text_img, self.vector, thickness=self.thickness)
        self.blend = blend

    def sweep_plane(self):
        # __ params to add __
        # with imshow
        # control video: text_location, text_size, text_color, text_font, text_thickness, text_background_color

        # keep high level, refactor to utils
        sweep_pixels = tvutils.get_sweep_pixel_groups(self.text_img, self.vector, self.thickness)
        cap = init_video_capture()
        img = self.lined_img
        img_set = []
        for sweep_pixel_group in sweep_pixels:
            img_set.append(tvutils.create_image_from_pixel_group(sweep_pixel_group, img.shape))
        if self.blend:
            tvutils.create_video_with_blend(img_set, cap, self.blend, self.text_img)
        else:
            tvutils.create_video_without_blend(img_set, cap, self.text_img)
        cap.release()

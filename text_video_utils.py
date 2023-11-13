import cv2
import numpy as np
from stitcher import find_available_name


def get_direction_from_vector(vector):
    pass


def get_lines(mask_img, vector, thickness):
    pass


def get_sweep_pixel_groups(mask_img, vector, thickness):
    pass


def create_video_without_blend(img_set, cap, text_img, show=False):
    pass


def create_video_with_blend(img_set, cap, blend, text_img, show=False):
    pass


def create_image_from_pixel_group(sweep_pixel_group, shape):
    pass


def init_capture_video(vid_size):
    vw = cv2.VideoWriter(find_available_name('output.avi'), cv2.VideoWriter_fourcc(*'XVID'), 25, vid_size)
    return vw

#
# def compute_next_frame_wbw(words, frame_idx, vid_size):
#     start_point = (int(vid_size[0] * 0.8), int(vid_size[1] * 0.8))
#     text_to_show = ''.join([word+' ' for word in words[:frame_idx]])
#     text_width = cv2.getTextSize(text_to_show, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]
#     text_start_point = (start_point[0] - text_width, start_point[1])
#     frame = np.zeros(vid_size, dtype=np.uint8)
#     cv2.putText(frame, text_to_show, text_start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1)
#     return frame


def compute_next_frame_wbw(words, frame_idx, vid_size):
    frame = np.zeros(vid_size, dtype=np.uint8)
    line_spacing = 30
    max_width = int(vid_size[0] * 0.8)
    y = int(vid_size[1] * 0.8)
    lines = []
    current_line = ""

    for word in words[:frame_idx]:
        current_line = word + " " + current_line
        line_width = cv2.getTextSize(current_line, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]

        if line_width > max_width:
            lines.insert(0, current_line.strip())
            current_line = word + " "
            line_width = cv2.getTextSize(current_line, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]

            if len(lines) * line_spacing > vid_size[1] - line_spacing:
                lines.pop()

    lines.insert(0, current_line.strip())

    for idx, line in enumerate(lines):
        text_width = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]
        text_start_point = (max_width - text_width, y - idx * line_spacing)
        cv2.putText(frame, line, text_start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1)

    return frame



def cgpt2_compute_next_frame_wbw(words, frame_idx, vid_size):
    frame = np.zeros(vid_size, dtype=np.uint8)
    line_spacing = 30
    max_width = int(vid_size[0] * 0.8)
    y = int(vid_size[1] * 0.8)
    lines = []
    current_line = ""

    for word in words[:frame_idx]:
        current_line = word + " " + current_line
        line_width = cv2.getTextSize(current_line, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]

        if line_width > max_width:
            lines.insert(0, current_line.strip())
            current_line = word + " "
            line_width = cv2.getTextSize(current_line, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]

            if len(lines) * line_spacing > vid_size[1] - line_spacing:
                lines.pop()

    lines.insert(0, current_line.strip())

    for idx, line in enumerate(lines):
        cv2.putText(frame, line, (0, y - idx * line_spacing), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1)

    return frame


def cgpt_compute_next_frame_wbw(words, frame_idx, vid_size):
    frame = np.zeros(vid_size, dtype=np.uint8)
    line_spacing = 30
    max_width = int(vid_size[0] * 0.8)
    y = int(vid_size[1] * 0.8)
    text_line = ""
    line_width = 0

    for word in words[:frame_idx]:
        new_line = text_line + word + " "
        new_line_width = cv2.getTextSize(new_line, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]

        if new_line_width > max_width:
            cv2.putText(frame, text_line, (0, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1)
            text_line = word + " "
            line_width = cv2.getTextSize(text_line, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]
            y -= line_spacing
        else:
            text_line = new_line
            line_width = new_line_width

    cv2.putText(frame, text_line, (0, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1)
    return frame


def draw_spiral_text(text, img_size):
    words = text.split()
    frame = np.zeros(img_size, dtype=np.uint8)

    angle = 0
    scale_factor = 1
    x, y = img_size[0] // 2, img_size[1] // 2
    radius = 0

    for word in words[::]:
        angle -= np.pi / 4
        radius += 15
        scale = 0.5 + scale_factor * 0.05
        scale_factor *= 0.9

        text_size = cv2.getTextSize(word, cv2.FONT_HERSHEY_SIMPLEX, scale, 1)[0]
        x += int(radius * np.cos(angle))
        # y += int(radius * np.sin(angle))

        x = max(min(x, img_size[0] - text_size[0]), 0)
        y = max(min(y, img_size[1] - text_size[1]), 0)

        cv2.putText(frame, word, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, 255, 1)

    return frame
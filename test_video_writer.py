import cv2
import numpy as np

def create_color_transition_video(output_file, color1, color2, width=800, height=600, fps=30):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    num_frames = 100
    for i in range(num_frames):
        t = i / (num_frames - 1)
        frame_color = ((1 - t) * np.array(color1) + t * np.array(color2)).astype(np.uint8)
        frame = np.full((height, width, 3), frame_color, dtype=np.uint8)
        video_writer.write(frame)

    video_writer.release()

if __name__ == "__main__":
    create_color_transition_video("color_transition.avi", (0, 0, 255), (0, 255, 0))

import cv2
import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
import text_video_utils as tvutils

class OrthogonalEdgeDetection:
    def __init__(self, text_file, output_video, vector_1, vector_2):
        self.text_file = text_file
        self.output_video = output_video
        self.font_size = 20
        self.white_color = (255, 255, 255)
        self.text = self.read_text_file()
        self.text_img = self.create_text_image()
        self.orig_edges = self.get_edges()
        self.edges = self.orig_edges
        self.elongate_edges(vector_1, vector_2)

    def read_text_file(self):
        with open(self.text_file, 'r') as f:
            return f.read()

    def create_text_image(self):
        img = np.zeros((600, 800, 3), np.uint8)
        cv2.putText(img, self.text, (40, self.font_size * 2), cv2.FONT_HERSHEY_SIMPLEX, 1, self.white_color, 2)
        return img

    def get_edges(self):
        gray = cv2.cvtColor(self.text_img, cv2.COLOR_BGR2GRAY)
        blurred_img = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred_img, 50, 150, apertureSize=3)
        return edges

    def elongate_edges(self, v1, v2):
        cv2.namedWindow('edges', 0)
        print('starting')
        cv2.startWindowThread()

        def elongate(vec1, vec2):
            for y in range(self.edges.shape[0]):
                for x in range(self.edges.shape[1]):
                    if self.orig_edges[y, x] > 0:
                        end_point1 = (x + vec1[0], y + vec1[1])
                        end_point2 = (x + vec2[0], y + vec2[1])
                        cv2.line(self.edges, (x, y), end_point1, self.white_color, 1)
                        cv2.line(self.edges, (x, y), end_point2, self.white_color, 1)
                    cv2.imshow('edges', self.edges)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print('breaking')
                        return

        elongate(v1, v2)
        cv2.destroyAllWindows()

    #
    # def elongate_edges(self):
    #     import time
    #     cv2.namedWindow('edges', 0)
    #     print('starting')
    #     cv2.startWindowThread()
    #     print('continuing')
    #     for y in range(self.edges.shape[0]):
    #         for x in range(self.edges.shape[1]):
    #             if self.orig_edges[y, x] > 0:
    #                 cv2.line(self.edges, (x, y), (self.edges.shape[1] - 1, y), self.white_color, 1)
    #                 cv2.line(self.edges, (x, y), (x, self.edges.shape[0] - 1), self.white_color, 1)
    #             cv2.imshow('edges', self.edges)
    #             if x % 50 == 0:
    #                 print(x)
    #             if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 print('breaking')
    #                 break
    #     cv2.destroyAllWindows()
    #

    def create_video(self):
        video_writer = cv2.VideoWriter(self.output_video, cv2.VideoWriter_fourcc(*'MJPG'), 10,
                                       (self.edges.shape[1], self.edges.shape[0]))
        for _ in range(100):
            video_writer.write(cv2.cvtColor(self.edges, cv2.COLOR_GRAY2BGR))
        video_writer.release()


class PlaneSweepForText:
    def __init__(self, text_img, vector, thickness=10, blend=None):
        self.text_img = text_img
        self.vector = tvutils.get_direction_from_vecotor(vector)
        self.thickness = thickness
        self.lined_img = tvutils.get_lines(self, text_img, vector, thickness=thickness)
        self.blend = blend


    def sweep_plane(self):
        # __ params 2 add __
        # with imshow
        # control video: text_location, text_size, text_color, text_font, text_thickness, text_background_color

        # keep high level, refactor to utils
        sweep_pixels = self.get_sweep_pixel_groups(self.text_img, self.vector, self.thickness)
        cap = tvutils.init_capture_video()
        img = self.lined_image
        img_set = []
        for sweep_pixel_group in sweep_pixels:
            img_set.append(tvutils.create_image_from_pixel_group(sweep_pixel_group, img.shape))
        if self.blend:
            tvutils.create_video_with_blend(img_set, cap, self.blend, self.text_img)
        else:
            tvutils.create_video_without_blend(img_set, cap, self.text_img)
        cap.release()


class WordByWord:
    def __init__(self, string, vid_size, rate):
        self.words = string.split()
        self.rate = int(rate * 25)
        self.vid_size = vid_size

    def create_video(self):
        cv2.namedWindow('word_by_word', 0)
        print('starting wbw')
        cv2.startWindowThread()
        vw = tvutils.init_capture_video(self.vid_size)

        def create_and_write_video(vw):
            word_idx = 0
            for frame_idx in range(len(self.words) * self.rate + 25):
                if frame_idx % self.rate == 0:
                    frame = tvutils.compute_next_frame_wbw(self.words, word_idx, self.vid_size)
                    word_idx = min(word_idx + 1, len(self.words))
                cv2.imshow('word_by_word', frame)
                vw.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return

        create_and_write_video(vw)
        vw.release()
        cv2.destroyAllWindows()

    def split_text_to_lines(self):
        for i in range(len(self.words)):
            pass


class VideoTextFromFunc:
    def __init__(self, func, text, vid_size, rate):
        self.func = func
        self.text = text
        self.rate = int(rate * 25)
        self.vid_size = vid_size

    def create_video(self):
        cv2.namedWindow('word_by_word', 0)
        print('starting wbw')
        cv2.startWindowThread()
        video_writer = tvutils.init_capture_video(self.vid_size)

        def create_and_write_video(vw):
            frame = 0
            word_idx = 1
            frame_num = len(self.text.split()) * self.rate + 25
            for frame_idx in range(frame_num):
                if frame_idx % self.rate == 0:
                    words = [word+' ' for word in self.text.split()]
                    frame = self.func(''.join(words[:word_idx]), self.vid_size)
                    word_idx = min(word_idx + 1, len(self.text)-1)
                cv2.imshow('word_by_word', frame)
                vw.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return

        create_and_write_video(video_writer)
        video_writer.release()
        cv2.destroyAllWindows()


def add_brightness_along_line(image, angle, coordinate, brightness_increase=100):
    width, height = image.size
    x, y = coordinate
    x = width - x
    y = height - y

    radians = np.deg2rad(angle)
    tan_angle = np.tan(radians)

    start_x = int(x - (y / tan_angle)) if tan_angle != 0 else 0
    start_y = int(y - (x * tan_angle))
    end_x = int(x + ((height - y) / tan_angle)) if tan_angle != 0 else width
    end_y = int(y + ((width - x) * tan_angle))

    np_image = np.array(image.convert('RGBA'))
    line_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(line_image)
    draw.line([(start_x, start_y), (end_x, end_y)], fill=(brightness_increase, brightness_increase, brightness_increase, 255), width=1)

    np_line_image = np.array(line_image)
    np_output_image = np_image + np_line_image
    np_output_image = np.clip(np_output_image, 0, 255)

    output_image = Image.fromarray(np_output_image.astype(np.uint8), 'RGBA')
    return output_image

# Example usage
image = Image.open("input_image.png")
angle = 45
coordinate = (100, 100)
output_image = add_brightness_along_line(image, angle, coordinate)
output_image.save("output_image.png")



if __name__ == '__main__':
    # wbw = WordByWord("hello my dear world, I hope it's time", (400, 400), 2)
    # wbw.create_video()

    txt = "hello my dear world, I hope it's time for us to come together and make a change"
    VideoTextFromFunc(tvutils.draw_spiral_text, txt, (800, 800), 0.7).create_video()


    #
    #
    # vector1 = (8, 14)  # Change these vectors to your desired values
    # vector2 = (-3, 50)
    # oed = OrthogonalEdgeDetection('input_text.txt', 'output_video.avi', vector1, vector2)
    # oed.create_video()

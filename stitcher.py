import string

import cv2
import os
import numpy as np
from PIL import Image


def find_available_name(out_name: string) -> string:
    name, ext = os.path.splitext(out_name)
    i = 0
    while os.path.exists(out_name):
        out_name = f"{name}_v{i}{ext}"
        i += 1
    return out_name

def stitch_media1(files, output_size, stitch_method, output_name, sizes=None, fade=False):


    def create_grid(images, grid_size, output_size):
        output = Image.new('RGB', output_size)
        x_step = output_size[0] // grid_size[1]
        y_step = output_size[1] // grid_size[0]
        i = 0
        for y in range(0, output_size[1], y_step):
            for x in range(0, output_size[0], x_step):
                if i < len(images):
                    img = images[i].resize((x_step, y_step), Image.ANTIALIAS)
                    output.paste(img, (x, y))
                    i += 1
        return output

    def create_line(images, output_size, orientation='horizontal'):
        if orientation == 'horizontal':
            output = Image.new('RGB', (len(images) * output_size[0], output_size[1]))
            for i, img in enumerate(images):
                img = img.resize(output_size, Image.ANTIALIAS)
                output.paste(img, (i * output_size[0], 0))
        else:
            output = Image.new('RGB', (output_size[0], len(images) * output_size[1]))
            for i, img in enumerate(images):
                img = img.resize(output_size, Image.ANTIALIAS)
                output.paste(img, (0, i * output_size[1]))
        return output

    from PIL import Image, ImageDraw
    import math

    def create_circle(images, output_size, method):
        """
        Creates a circular image by stitching together the given images around the center of the image.
        The split between images is a line of the middle angle between them.
        """
        # calculate the radius of the circle
        radius = min(output_size) // 2

        # create a new image for the output
        output = Image.new('RGBA', output_size, (0, 0, 0, 0))

        # calculate the angle between images
        angle_between_images = 360.0 / len(images)

        # loop through the images and paste them onto the output
        for i, image in enumerate(images):
            # calculate the angle for this image
            angle = i * angle_between_images

            # rotate the image to the correct angle
            # rotated_image = image.rotate(-angle, resample=Image.BICUBIC, expand=True)

            # calculate the position for this image
            x = int(math.cos(math.radians(angle)) * radius + output_size[0] // 2)
            y = int(math.sin(math.radians(angle)) * radius + output_size[1] // 2)

            # paste the rotated image onto the output
            # output.paste(image, (x, y), image)z

            # draw a line to separate the images
            if method == 'line':
                draw = ImageDraw.Draw(output)
                start_angle = (angle + angle_between_images / 2) % 360
                start_x = int(math.cos(math.radians(start_angle)) * radius + output_size[0] // 2)
                start_y = int(math.sin(math.radians(start_angle)) * radius + output_size[1] // 2)
                end_x = int(math.cos(math.radians(start_angle + 180)) * radius + output_size[0] // 2)
                end_y = int(math.sin(math.radians(start_angle + 180)) * radius + output_size[1] // 2)
                draw.line((start_x, start_y, end_x, end_y), fill=(255, 255, 255, 255), width=1)

        return output

    images = []
    videos = []

    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            images.append(Image.open(file))
        elif file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            videos.append(file)

    if len(videos) == 0:
        if stitch_method == 'grid':
            grid_size = (int(np.ceil(np.sqrt(len(images)))) * 2)
            output_image = create_grid(images, grid_size, output_size)
        elif stitch_method == 'horizontal':
            output_image = create_line(images, output_size, 'horizontal')
        elif stitch_method == 'vertical':
            output_image = create_line(images, output_size, 'vertical')
        elif stitch_method in ['clockwise_circle', 'random_circles', 'circle']:
            output_image = create_circle(images, output_size, stitch_method)
        else:
            raise ValueError(f"Unknown stitching method: {stitch_method}")

        output_name = find_available_name(output_name)
        output_image.save(output_name)

    else:
        # TODO: Implement video stitching
        pass

    return output_name



def stitch_media(files, output_size, stitch_type, output_name, dimensions=None, fade=False):
    def get_available_filename(filename):
        i = 0
        while os.path.exists(filename):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_v{i}{ext}"
            i += 1
        return filename

    def stitch_images(images, stitch_type, output_size, dimensions):
        # Add your implementation for each stitch type here
        pass

    def stitch_videos(videos, stitch_type, output_size, dimensions, fade):
        # Add your implementation for each stitch type here
        pass

    images = []
    videos = []

    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            images.append(file)
        elif file.lower().endswith(('.mp4', '.avi', '.mov')):
            videos.append(file)

    if len(images) > 0 and len(videos) == 0:
        stitched_image = stitch_images(images, stitch_type, output_size, dimensions)
        output_name = get_available_filename(output_name)
        stitched_image.save(output_name)
        print(f"Stitched image saved as {output_name}")
    elif len(videos) > 0:
        stitch_videos(videos, stitch_type, output_size, dimensions, fade)
        print("Stitched video saved")
    else:
        print("No valid files found")



def resize_image(input_path, output_path, size, crop=False):
    """
    Resizes an image at input_path to the given size (width, height) and saves it to output_path.
    If crop is True, the image will be cropped to the aspect ratio of the given size before resizing.
    """
    with Image.open(input_path) as image:
        if crop:
            # crop the image to the aspect ratio of the given size
            aspect_ratio = float(size[0]) / size[1]
            image_aspect_ratio = float(image.size[0]) / image.size[1]
            if image_aspect_ratio < aspect_ratio:
                # crop the height
                new_height = int(image.size[0] / aspect_ratio)
                center_y = int(image.size[1] / 2)
                top_y = center_y - int(new_height / 2)
                bottom_y = center_y + int(new_height / 2)
                image = image.crop((0, top_y, image.size[0], bottom_y))
            else:
                # crop the width
                new_width = int(image.size[1] * aspect_ratio)
                center_x = int(image.size[0] / 2)
                left_x = center_x - int(new_width / 2)
                right_x = center_x + int(new_width / 2)
                image = image.crop((left_x, 0, right_x, image.size[1]))

        # resize the image
        image = image.resize(size)

        # save the resized image to the output file
        image.save(output_path)


from PIL import Image, ImageDraw
import math

def create_circle(images, output_size, method):
    """
    Creates a circular image by stitching together the given images around the center of the image.
    The split between images is a line of the middle angle between them.
    """
    images = [Image.open(images[i]) for i in range(len(images))]
    # calculate the radius of the circle
    radius = min(output_size) // 2

    # create a new image for the output
    output = Image.new('RGBA', output_size, (0, 0, 0, 0))

    # create a mask for the output
    mask = Image.new('L', output_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, output_size[0], output_size[1]), fill=255)

    # calculate the angle between images
    angle_between_images = 360.0 / len(images)

    # loop through the images and paste them onto the output
    for i, image in enumerate(images):
        # calculate the angle for this image
        angle = i * angle_between_images

        # calculate the position for this image
        x = int(math.cos(math.radians(angle)) * radius + output_size[0] // 2)
        y = int(math.sin(math.radians(angle)) * radius + output_size[1] // 2)

        # calculate the crop box for this image
        crop_box = (x - radius, y - radius, x + radius, y + radius)

        # paste the image onto the output using the mask
        output.paste(image, crop_box, mask)

        # draw a line to separate the images
        if method == 'line':
            draw = ImageDraw.Draw(output)
            start_angle = (angle + angle_between_images / 2) % 360
            start_x = int(math.cos(math.radians(start_angle)) * radius + output_size[0] // 2)
            start_y = int(math.sin(math.radians(start_angle)) * radius + output_size[1] // 2)
            end_x = int(math.cos(math.radians(start_angle + 180)) * radius + output_size[0] // 2)
            end_y = int(math.sin(math.radians(start_angle + 180)) * radius + output_size[1] // 2)
            draw.line((start_x, start_y, end_x, end_y), fill=(255, 255, 255, 255), width=1)

    return output


if __name__ == '__main__':
    # Example usage
    files = ["ophir_v0.jpg",
             "gal_v0.png",
             "avshi2_v0.jpeg"]

    method = 'line'
    result = create_circle(files, (1080,1080), method)
    result.save('output1.png')

    new_files = []
    # for file in files:
    #     new_files.append(find_available_name(file))
    #     resize_image(file, new_files[-1], (900, 667), crop=True)


    output_size = (1080, 1080)
    stitch_type = "circle"
    output_name = "output.jpg"
    dimensions = [667, 667, 667]

    #stitch_media1(files, output_size, stitch_type, output_name, fade=False)


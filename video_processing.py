import os
import cv2
import numpy as np


def frames_to_video(input_folder, output_video, start_index, end_index):
    # Get the list of image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    image_files = sorted(image_files)

    # Get the path of the first image
    first_image_path = os.path.join(input_folder, f'{start_index:04d}.png')

    # Read the first image to get the dimensions
    frame = cv2.imread(first_image_path)
    h, w, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video, fourcc, 20.0, (w, h))

    # Loop through each image and write it to the video
    for i in range(start_index, end_index + 1):
        img_path = os.path.join(input_folder, f'{i:04d}.png')
        img = cv2.imread(img_path)
        out.write(img)

    # Release the video writer object
    out.release()
    print("Done!")


def frames_to_video2(frame_folder, out_file, file_ext='MP4V'):
    # List all files in frame_folder and sort them
    # 'XVID', 'MP4V', 'MJPG'
    files = sorted([f for f in os.listdir(frame_folder) if f.endswith('.jpg') ])
    print(files[0])
    print(files[1])
    if not files:
        print("No frames in the specified directory!")
        return

    # Define the codec and create VideoWriter object
    # The video size is determined based on the first image
    first_image = cv2.imread(os.path.join(frame_folder, files[0]))
    height, width, layers = first_image.shape
    fourcc = cv2.VideoWriter_fourcc(*file_ext)
    out = cv2.VideoWriter(out_file, fourcc, 10.0, (width, height))

    for f in files:
        img = cv2.imread(os.path.join(frame_folder, f))
        out.write(img)

    out.release()
    cv2.destroyAllWindows()
    print("Video created successfully!")


def video_to_frames(video_path, output_folder):
    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Loop through each frame and save it as an image in the output folder
    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame as an image
        output_path = os.path.join(output_folder, f'frame_{i:04d}.png')
        cv2.imwrite(output_path, frame)

    # Release the video capture object
    cap.release()
    print("Done!")


def rotate_images(directory):
    # Get the list of all .png files in the directory
    image_files = [f for f in os.listdir(directory) if f.endswith('.png')]

    for image_file in image_files:
        # Construct the full path to the image file
        image_path = os.path.join(directory, image_file)

        # Read the image
        img = cv2.imread(image_path)

        # Rotate the image by 180 degrees
        rotated_img = cv2.rotate(img, cv2.ROTATE_180)

        # Save the rotated image
        # If you want to save to a different directory, modify the path here
        cv2.imwrite(image_path, rotated_img)

    print(f"Rotated {len(image_files)} images by 180 degrees.")


def green_screen_basic(file_name, out_file):
  cap = cv2.VideoCapture(file_name)
  ret, frame = cap.read()
  height, width, layers = frame.shape
  fourcc = cv2.VideoWriter_fourcc(*'MP4V')
  out = cv2.VideoWriter(out_file, fourcc, 20.0, (height, width))
  cap = cv2.VideoCapture(file_name)
  while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
          break
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      lower_green = np.array([36, 35, 35])
      upper_green = np.array([86, 255, 255])
      mask = cv2.inRange(hsv, lower_green, upper_green)
      mask_inv = cv2.bitwise_not(mask)
      frame_out = cv2.bitwise_and(frame, frame, mask=mask_inv)

      out.write(frame_out)

  cap.release()
  out.release()



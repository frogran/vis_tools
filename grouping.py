import shutil
import numpy as np
import os
import cv2


def sort_images_by_color_ratio(folder_path):
    # Function to calculate the blue+green to red ratio of an image
    def calculate_ratio(image):
        # Calculate the sum of the blue and green channels
        blue_green_sum = np.sum(image[:, :, 0]) + np.sum(image[:, :, 1])  # Blue is channel 0, green is channel 1 in BGR
        # Calculate the sum of the red channel
        red_sum = np.sum(image[:, :, 2])  # Red is channel 2 in BGR
        # Avoid division by zero
        if red_sum == 0:
            return 0
        # Return the ratio of (blue+green) / red
        return blue_green_sum / red_sum

    # Get a list of image file paths
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Calculate the color ratio for each image and store in a list
    ratios = []
    for file_name in image_files:
        file_path = os.path.join(folder_path, file_name)
        image = cv2.imread(file_path)
        if image is not None:
            ratio = calculate_ratio(image)
            ratios.append((file_name, ratio))

    # Sort the images by the color ratio from highest to lowest
    ratios.sort(key=lambda x: x[1], reverse=True)

    # Print the sorted file names
    sorted_file_names = [file_name for file_name, ratio in ratios]
    print("Sorted file names from bluest/greenest to reddest:")
    sorted_folder_path = os.path.join(folder_path, 'sorted')
    if not os.path.exists(sorted_folder_path):
        os.makedirs(sorted_folder_path)
    for i, file_name in enumerate(sorted_file_names):
        original_file_path = os.path.join(folder_path, file_name)
        new_file_name = f"{i+1:04d}.jpg"
        new_file_path = os.path.join(sorted_folder_path, new_file_name)
        shutil.copy2(original_file_path, new_file_path)


def calculate_red_black_content(image):
    # Convert image to RGB (OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Set thresholds for red and black colors
    # You might need to adjust these thresholds depending on your definition of 'red' and 'black'
    red_lower = np.array([100, 0, 0])
    red_upper = np.array([255, 100, 100])
    black_lower = np.array([0, 0, 0])
    black_upper = np.array([50, 50, 50])

    # Create masks for red and black
    red_mask = cv2.inRange(image_rgb, red_lower, red_upper)
    black_mask = cv2.inRange(image_rgb, black_lower, black_upper)

    # Calculate the amount of red and black pixels
    red_content = np.sum(red_mask > 0)
    black_content = np.sum(black_mask > 0)

    # Return the combined amount of red and black
    return red_content + black_content


def sort_photos_by_color(folder_path):
    # Create a sorted folder within the given folder_path
    sorted_folder_path = os.path.join(folder_path, 'sorted')
    if not os.path.exists(sorted_folder_path):
        os.makedirs(sorted_folder_path)

    # Get a list of image file paths
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Calculate the amount of red and black in each photo
    color_content = []
    for file_name in image_files:
        file_path = os.path.join(folder_path, file_name)
        image = cv2.imread(file_path)
        if image is not None:
            color_amount = calculate_red_black_content(image)
            color_content.append((file_name, color_amount))

    # Sort the images by the amount of red and black (ascending order)
    color_content.sort(key=lambda x: x[1], reverse=True)  # Most red and black last

    # Copy files to the new folder in sorted order and rename them
    for i, (file_name, _) in enumerate(color_content):
        original_file_path = os.path.join(folder_path, file_name)
        new_file_name = f"{i+1:04d}_{file_name}"
        new_file_path = os.path.join(sorted_folder_path, new_file_name)
        shutil.copy2(original_file_path, new_file_path)

    print(f"Photos have been sorted and copied to {sorted_folder_path}")

# Usage
folder_path = '/content/drive/MyDrive/words/burn1'
sort_photos_by_color(folder_path)

# Usage
# folder_path = '/content/drive/MyDrive/words/burn1'
# sorted_photos = sort_photos_by_color(folder_path)
# The sorted_photos list will contain tuples of (file_name, color_amount), sorted by color_amount

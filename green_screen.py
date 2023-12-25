import cv2
import numpy as np

cap = cv2.VideoCapture('videos/green_prayer.mov')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter("videos/output.mp4", fourcc, 30.0, size)

cap = cv2.VideoCapture('videos/green_prayer.mov')
# Loop over every frame in the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = np.array([36, 25, 25])
    upper_green = np.array([86, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Invert mask to get parts that are not green
    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of green screen in the frame
    frame_out = cv2.bitwise_and(frame, frame, mask=mask_inv)


    # Save the resulting frame
    out.write(frame_out)

    # Display the resulting frame
    cv2.imshow('frame', frame_out)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when done
cap.release()
out.release()
cv2.destroyAllWindows()

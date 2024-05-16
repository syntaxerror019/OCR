import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # optional addition for tesseract. (Windows...)

# Function to convert hex to BGR
def hex_to_bgr(hex_color.lstrip('#')):
    return tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))

# Specific hex color you want to keep in the image (TEXT Color)
hex_color = '#7d502f'  #fffff would be white..
bgr_color = hex_to_bgr(hex_color)

# open up the image
image = cv2.imread(r'C:\Path\To\Your\Image\file.png')

# create masks
lower = np.array(bgr_color)
upper = np.array(bgr_color)
mask = cv2.inRange(image, lower, upper)

#filter using the newly created masks
result = cv2.bitwise_and(image, image, mask=mask)

# Convert the filtered image to grayscale
gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

# Apply threshold to get a binary image (black text on white background)
_, binary_result = cv2.threshold(gray_result, 1, 255, cv2.THRESH_BINARY_INV)

# Scale down the images by 0.5
scale_factor = 0.5
image_small = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor)
binary_result_small = cv2.resize(binary_result, (0, 0), fx=scale_factor, fy=scale_factor)

# Perform OCR on the binary image
custom_config = r'--oem 3 --psm 6' # <-- This is very useful!
detection_data = pytesseract.image_to_data(binary_result, config=custom_config, output_type=pytesseract.Output.DICT)

# Extract the text and their positions
num_boxes = len(detection_data['level'])
for i in range(num_boxes):
    (x, y, w, h) = (detection_data['left'][i], detection_data['top'][i], detection_data['width'][i], detection_data['height'][i])
    text = detection_data['text'][i]
    if text.strip():  # Check if the text is not empty (sometimes it generated weird results...)
        
        print(f'Text: {text}, X: {x}, Y: {y}, Width: {w}, Height: {h}')
        
        cv2.rectangle(binary_result, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(binary_result, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Scale down the annotated binary result
binary_result_annotated_small = cv2.resize(binary_result, (0, 0), fx=scale_factor, fy=scale_factor)

# Display the original and the result images
cv2.imshow('Original Image', image_small)
cv2.imshow('out', binary_result_annotated_small)
cv2.waitKey(0)
cv2.destroyAllWindows()

from os import listdir
from cv2 import imread, imwrite
from cv2 import GaussianBlur, Laplacian
from cv2 import morphologyEx, MORPH_ELLIPSE, MORPH_CLOSE, getStructuringElement
from cv2 import cvtColor, inRange, COLOR_BGR2GRAY, CV_64F, COLOR_BGR2HSV
from cv2 import threshold, THRESH_BINARY, THRESH_OTSU, erode
from cv2 import bitwise_and, bitwise_not, bitwise_or
from numpy import dstack, absolute, uint8, full, array
from matplotlib.pyplot import imshow

INPUT_FOLDER = '/home/jovyan/work/INPUT/'
OUTPUT_FOLDER = '/home/jovyan/work/OUTPUT/'
list_of_files = listdir(INPUT_FOLDER)
for filename in list_of_files:
    # read image
    original = imread(INPUT_FOLDER + filename)
    gray = cvtColor(original, COLOR_BGR2GRAY)

    # create threshold for hairs and hairy clothes
    filtered = uint8(absolute(Laplacian(gray, CV_64F)))
    r, light_thresh = threshold(filtered, 0, 255, THRESH_BINARY + THRESH_OTSU)

    # create threshold for skin areas
    lower = array([0, 10, 80], dtype="uint8")
    upper = array([20, 255, 255], dtype="uint8")
    hsv = cvtColor(original, COLOR_BGR2HSV)
    skin = inRange(hsv, lower, upper)
    ret, medium_thresh = threshold(skin, 0, 255, THRESH_BINARY + THRESH_OTSU)

    # create threshold for dark areas
    blur = GaussianBlur(gray, (7, 7), 1)
    ret, dark_thresh = threshold(blur, 110, 255, THRESH_BINARY)
    dark_thresh = bitwise_not(dark_thresh)
    dark_thresh = erode(dark_thresh, (5, 5), iterations=3)
    ellipse = getStructuringElement(MORPH_ELLIPSE, (35, 35))
    dark_thresh = morphologyEx(dark_thresh, MORPH_CLOSE, ellipse)
    dark_thresh = erode(dark_thresh, (5, 5), iterations=3)

    # create a mask
    thresh = bitwise_or(light_thresh, dark_thresh)
    thresh = bitwise_or(thresh, medium_thresh)
    mask = dstack([thresh]*3)

    # combine the masks and save result
    mask = dstack([thresh]*3)
    white = full(original.shape, 255, dtype=uint8)
    foreground = bitwise_and(original, mask)
    background = bitwise_and(white, bitwise_not(mask))
    result = bitwise_or(foreground, background)
    imwrite(OUTPUT_FOLDER + 'result_' + filename, result)

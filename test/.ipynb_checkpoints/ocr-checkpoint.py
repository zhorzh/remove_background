# from PIL import Image
import sys
import cv2
# from cv2 import imread
# from cv2 import imshow
from matplotlib.pyplot import imshow
from matplotlib.pyplot import show
from numpy import zeros, dstack

%matplotlib inline

BLUR = 21
CANNY_THRESH_1 = 10
CANNY_THRESH_2 = 200
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10
MASK_COLOR = (0.0, 0.0, 1.0)

default_jupyter_folder = '/home/jovyan/work/notebooks/INPUT/'
output_folder = '/home/jovyan/work/notebooks/OUTPUT/'
filename = '4060868456445_05617_3377215_m0.jpg'
image = cv2.imread(default_jupyter_folder + filename)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
edges = cv2.dilate(edges, None)
edges = cv2.erode(edges, None)

contour_info = []
_, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
for c in contours:
    contour_info.append((
        c,
        cv2.isContourConvex(c),
        cv2.contourArea(c),
    ))
contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
max_contour = contour_info[0]

mask = zeros(edges.shape)
cv2.fillConvexPoly(mask, max_contour[0], (255))

mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
####################################################################
####################################################################
mask_stack = dstack([mask]*3)

mask_stack = mask_stack.astype('float32') / 255.0          # Use float matrices,
image = image.astype('float32') / 255.0                 #  for easy blending
masked = (mask_stack * image) + ((1-mask_stack) * MASK_COLOR) # Blend
masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit


cv2.imwrite(output_folder + filename, masked)           # Save
####################################################################
image = cv2.imread(filename)
imshow(masked)
%ls


# split image into channels
c_red, c_green, c_blue = cv2.split(image)

# merge with mask got on one of a previous steps
img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))

# show on screen (optional in jupiter)
imshow(img_a)

# save to disk
cv2.imwrite('test.jpg', img_a*255)

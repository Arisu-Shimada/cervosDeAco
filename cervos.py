import cv2
import numpy as np

img = cv2.imread("reta.png")

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# apply binary thresholding
ret, thresh = cv2.threshold(imgGray, 150, 255, cv2.THRESH_BINARY_INV)

# Apply Canny Edge Detector
edges = cv2.Canny(thresh, 50, 150)

# Detect lines using HoughLinesP
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=100, maxLineGap=10)

# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
                              
for line in lines:
    x1, y1, x2, y2 = line[0]

# draw contours on the original image
image_copy = img.copy()
cv2.line(image_copy, (x1, y1), (x2, y2), (0,255,0), 5)
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)
cv2.line(image_copy,(235,0),(235,1000),(0,0,255),5)
cv2.line(image_copy,(0,235),(1000,235),(0,0,255),5)
cv2.circle(image_copy,(x1, y1), 10, (0,255,0), -1)              
# see the results
cv2.imshow('None approximation', image_copy)
cv2.waitKey(0)
cv2.imwrite('contours_none_image1.jpg', image_copy)
cv2.destroyAllWindows()
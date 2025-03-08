import numpy as np
import cv2

img = cv2.imread("./resources/test_images/2012-09-20_10_09_24.jpg", cv2.IMREAD_ANYCOLOR)

start1 = (139, 165)
end1 = (162, 205)

color = (0, 0, 255)
thickness = 2

cv2.rectangle(img, start1, end1, color, thickness)

start2 = (21, 446)
end2 = (55, 494)

color2 = (255, 0, 0)

cv2.rectangle(img, start2, end2, color2, thickness)

cv2.imshow("image", img)

cv2.waitKey(0)  

cv2.destroyAllWindows()
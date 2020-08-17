import cv2

img = cv2.imread('Lenna.jpg', 2)
ret, img2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

cv2.imwrite('BinaryLenna.jpg', img2)
cv2.imwrite('BinaryLenna.png', img2)
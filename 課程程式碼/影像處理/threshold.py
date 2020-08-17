import cv2

img = cv2.imread('Lenna.jpg', 2)
cv2.imshow('img', img)

# 將亮度超過127的像素指定為255,其餘歸0
ret, img2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

cv2.imshow('img2', img2)
cv2.waitKey(0)

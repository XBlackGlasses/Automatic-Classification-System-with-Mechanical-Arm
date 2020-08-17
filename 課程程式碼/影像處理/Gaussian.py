import cv2

img = cv2.imread('Lenna.jpg')
cv2.imshow('img', img)

# 使用3x3的模糊方框
img2 = cv2.GaussianBlur(img, (3,3), 0)
# 使用7x7的模糊方框
img3 = cv2.GaussianBlur(img, (7,7), 0)

cv2.imshow('img2',img2)
cv2.imshow('img3', img3)
cv2.waitKey(0)
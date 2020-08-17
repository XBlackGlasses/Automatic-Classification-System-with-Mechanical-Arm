import cv2

img = cv2.imread('Lenna.jpg')
cv2.imshow('img', img)

# 指定陣列範圍
# [ y的起點:y的終點, x的起點:x的終點 ]
img2 = img[30:100, 30:100]

cv2.imshow('img2', img2)
cv2.waitKey(0)
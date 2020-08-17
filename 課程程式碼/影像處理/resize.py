import cv2

img = cv2.imread('Lenna.jpg')
cv2.imshow('img', img)

# 將影像變為200x200大小
# 並使用INTER_CUBIC的差補算法
img = cv2.resize(img, (200,200), interpolation=cv2.INTER_CUBIC)
cv2.imshow('img2', img)

cv2.waitKey(0)
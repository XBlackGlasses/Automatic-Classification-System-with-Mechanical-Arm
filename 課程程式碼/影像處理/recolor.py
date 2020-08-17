import cv2

img = cv2.imread('Lenna.jpg')
cv2.imshow('img', img)

#將區塊變為黑色
img[:40,:40] = 0

# 將區塊變為白色
img[:40,40:80] = 255

# 將區塊保留紅色
img[40:80,0:40,0:2] = 0

# 將區塊保留藍色
img[40:80,40:80,1:3] = 0

# 將區塊保留綠色
img[40:80,80:120,2] = 0
img[40:80,80:120,0] = 0

cv2.imshow('img2', img)
cv2.waitKey(0)
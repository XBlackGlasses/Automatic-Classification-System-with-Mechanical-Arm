import cv2

img = cv2.imread('Lenna.jpg')
cv2.imshow('img',img)
print('img shape:' + str(img.shape))

# opencv的顏色轉換函式
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print('img2 shape:' + str(img2.shape))
cv2.imshow('img2',img2)
cv2.waitKey(0)
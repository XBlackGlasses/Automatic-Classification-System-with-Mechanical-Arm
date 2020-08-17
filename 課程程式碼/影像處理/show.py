# import 影像處理的OpenCV
import cv2

# 使用cv2.imread()將檔案載入
# 注意()內是填寫路徑
# 而預設路徑為Terminal中所在的當下目錄
img = cv2.imread('Lenna.jpg')

print(type(img))
print(img.shape)
print(img)

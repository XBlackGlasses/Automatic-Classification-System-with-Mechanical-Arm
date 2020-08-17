# import Thread所需函示庫
import threading

# 定義稍後Thread所要執行的function，
# counterID: 識別Thread用
# addNum: 累加步數
# maxSum: 累加上限
def counter(counterID, addNum, maxSum):
    sum = 0
    while(sum<=maxSum):
        sum = sum + addNum
        print('This is counter' + str(counterID) + ': ' + str(sum))

# 實作Thread的物件，並將所要執行的function及參數帶入
counter1 = threading.Thread(target=counter, args=(1,1,4))
counter2 = threading.Thread(target=counter, args=(2,2,4))
#啟動Tread的運作
counter1.start()
counter2.start()
import threading # Thread所需函式庫
import time # 使程式產生延遲
import random # 亂數產生

# 建立變數(預設即為全域)
progressRate = 0

# 學生所執行函式
def do_homework():
    #導入全域變數
    global progressRate
    while(progressRate<100):
        #避免進度超過100所以取min
        progressRate = min(progressRate + random.randint(5,15),100)
        #\033[94m 及 \033[0m為print的顏色改變
        print('\033[94m(Student) doing homework...' + str(progressRate) + '%\033[0m')
        #延遲一秒
        time.sleep(1)

#老師所執行的函式
def check_homework():
    global progressRate
    while(progressRate<100):
        #使用亂數產生30%機率
        if random.randint(1,3) == 1:
            print('\033[91m(Teacher) Check homework...' + str(progressRate) + '%\033[0m')
        time.sleep(1)


student = threading.Thread(target=do_homework)
teacher = threading.Thread(target=check_homework)
student.start()
teacher.start()
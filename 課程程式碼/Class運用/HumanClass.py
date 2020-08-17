class Human():

    # Human 的建構含式，__init__為Python定義與法，
    # 程式可透過該函式產生一個Object儲存於記憶體中。
    # input中的self代表物件本身，也就是獨立存在記憶體中的Human型態資料，
    def __init__(self, name, height, weight):
        self.name = name
        self.height = height
        self.weight = weight

    # 不回傳任何資料，僅印出字串
    def say_my_name(self):
        print('My name is ' + self.name)

    # 回傳經過計算的BMI
    def getBMI(self):
        bmi = (self.weight / (self.height/100)**2)
        return bmi
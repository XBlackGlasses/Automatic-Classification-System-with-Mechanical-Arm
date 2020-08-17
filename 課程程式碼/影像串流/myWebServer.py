# import flask所需函式庫
from flask import Flask

# 使用本module建立Flask物件
app = Flask(__name__)

# 建立Web Server的路由路徑
# 意思是說可透過IP或是網域名稱加上路徑即可導向該函式
# 以下若以網址的角度看則為: 127.0.0.1:5000/
# flask預設port為5000
@app.route("/")
def hello():
    # 將Hello World字串回傳給連接端
    return "Hello World!"

# if __name__ == "__main__"為python專用語法
# 可避免其他Module呼叫此Module時不小心執行到以下程式
# 代表必須要以本檔案為啟動程式，才會執行到app.run()
if __name__ == "__main__":
    app.run()
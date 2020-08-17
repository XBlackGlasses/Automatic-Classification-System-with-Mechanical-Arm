from flask import Flask
# request用來讀取連接連接傳送的內容
from flask import request
# 將回傳給連接端的內容轉為json格式
import json
app = Flask(__name__)

# 建立user的class，並且新增兩個user至list中
class user:
    def __init__(self, id, name, score):
        self.id = id
        self.name = name
        self.score = score
user = [user(0, 'Jone', 70), user(1,'Rose', 80)]

# 查詢userData的GET /user-data
# 將user id用URL的方式傳入Web Server
@app.route("/user-data", method=['GET'])
def get_user_by_id():
    # 使用request將URL問號後的參數讀取出來
    id = request.args.get('id')
    # 查詢相同id的user
    for u in users:
        if u.id == int(id):
            # 回傳json格式的user，u.__dict__為列出user內的所有屬性
            return json.dumps({'user':u.__dict__})
    return 'Can\'t find!'

# 更新userData的PUT /user-data
# 輸入資料使用json放置body裡頭
@app.route("user-data", method=['PUT'])
def update_user_by_id():
    # 將body內的json讀出
    user = request.json
    # 查詢相同id，並更新
    for u in users:
        if u.id == user['id']:
            u.name = user['name']
            u.score = user['score']
    return 'OK'


if __name__ == "__main__":
    app.run()
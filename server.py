from flask import Flask,request,jsonify
import business
import redis
import game
from game import newGame
from utils import form_resp
 
app = Flask(__name__)

def format_str(input):
    return "\""+input+"\"" 

# 配置Redis连接
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# 配置限流参数
MAX_REQUESTS_PER_MINUTE = 2  # 每个IP每分钟最多允许10次请求
REQUEST_WINDOW_IN_SECONDS = 60  # 时间窗口，以秒为单位

def is_rate_limited(ip):
    """检查IP是否被限流"""
    key = f'request_count:{ip}'
    current_count = redis_client.incr(key)
    redis_client.expire(key, REQUEST_WINDOW_IN_SECONDS)
    return current_count > MAX_REQUESTS_PER_MINUTE

@app.route('/hello', methods=['GET'])
def hello_world():
    name = request.args.get('name', 'Martin')  # 如果'name'不存在，则返回'默认值'  
    age = request.args.get('age', type=int)
    return business.hello_world(name,age)
    # sql = "INSERT INTO test (name, age) VALUES ({},{})".format(format_str(name),age)
    # cursor.execute(sql)
    # db.commit()
    #return "{} record inserted.".format(cursor.rowcount)

### test
@app.route('/test/list', methods=['GET'])
def listTest():
    return business.listTest()

@app.route('/test/add', methods=['POST'])
def AddTest():
    name = request.json.get('name')  # 如果'name'不存在，则返回'默认值'  
    age = request.json.get('age')
    return business.addTest(name,age)

@app.route('/test/delete', methods=['GET'])
def DeleteTest():
    id = request.args.get('id', type=int)
    return business.deleteTest(id)

### login
@app.route('/login/list', methods=['GET'])
def ListLogin():
    return business.listLogin()

@app.route('/login/login', methods=['POST'])
def UserLogin():
    username = request.json.get('username')
    password = request.json.get('password')
    return business.userLogin(username,password)

@app.route('/login/register', methods=['POST'])
def UserRegister():
    username = request.json.get('username')
    age = request.json.get('age')
    gender = request.json.get('gender')
    mobile_no = request.json.get('mobile_no')
    password = request.json.get('password')
    repeat_password = request.json.get('repeat_password')
    return business.userRegister(username,age,gender,mobile_no,password,repeat_password)

### user
@app.route('/user/list', methods=['GET'])
def ListUser():
    return business.listUser()

@app.route('/user/listv2', methods=['GET'])
def ListUserByPage():
    limit = request.args.get('limit', 10)  # 如果'name'不存在，则返回'默认值'  
    offset = request.args.get('offset', 0)
    return business.listUserByPage(limit,offset)

@app.route('/user/add', methods=['POST'])
def AddUser():
    name = request.json.get('name')  # 如果'name'不存在，则返回'默认值'  
    age = request.json.get('age')
    gender = request.json.get('gender')
    mobile_no = request.json.get('mobile_no')
    return business.addUser(name,age,gender,mobile_no)

@app.route('/user/delete', methods=['GET'])
def DeleteUser():
    id = request.args.get('id', type=int)
    return business.deleteUser(id)

@app.route('/chat/bot', methods=['POST'])
def ChatWithBot():
    ip = request.remote_addr
    if is_rate_limited(ip):
        return form_resp(500,"You could only send at most 2 requests every minute !","")
    #prompt = request.args.get('prompt', type=str)
    prompt = request.json.get('prompt')
    model = request.json.get('model')
    return business.chatWithBot(prompt,model)

@app.route('/game/play', methods=['POST'])
def play():
    inputNum = int(request.json.get('inputNum'))
    return game.play(newGame,inputNum)

@app.route('/game/getScore', methods=['GET'])
def getScore():
    return game.getScore(newGame)

@app.route('/game/restart', methods=['POST'])
def restart():
    return game.restart(newGame)

if __name__ == '__main__':
    app.run(debug=True)

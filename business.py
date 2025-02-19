import test_db_connector
import user_db_connector
import login_db_connector
import random
import sparkPython_functionCall
from openai import OpenAI
from utils import form_resp

def hello_world(name, age):
    resp = 'Hello, World! Your name is {}, age is {}'.format(name,age)
    return form_resp(200,"OK",resp)

### test
def listTest():
    res = test_db_connector.List()
    print(res)
    return form_resp(200,"OK",res)

def addTest(name,age):
    res = test_db_connector.Create(name,age)
    return form_resp(200,"OK",res)

def deleteTest(id):
    res = test_db_connector.Delete(id)
    return form_resp(200,"OK",res)

### user
def listUser():
    res = user_db_connector.List()
    print(res)
    return form_resp(200,"OK",res)

def listUserByPage(limit,offset):
    count = user_db_connector.Count()[0]
    res = user_db_connector.ListByPage(limit,offset)
    if len(res)==0:
        res = {'count':count}
    else:
        res['count']=count
    return form_resp(200,"OK",res)

def addUser(name,age,gender,mobile_no):
    res = user_db_connector.Create(name,age,gender,mobile_no)
    return form_resp(200,"OK",res)

def deleteUser(id):
    res = user_db_connector.Delete(id)
    return form_resp(200,"OK",res)

### login
def listLogin():
    res = login_db_connector.List()
    return form_resp(200,"OK",res)

def userLogin(username, password):
    ## check if username exist
    loginInfo, lenLogin = login_db_connector.QueryByUserName(username)
    if lenLogin == 0:
        return form_resp(1001,"Username doesn't exist!",loginInfo)
    ## check if password is correct
    passwordDB = loginInfo['dataList'][0]['password']
    if passwordDB != password:
        return form_resp(2001,"Password incorrect!","")
    return form_resp(200,"OK",loginInfo)

def userRegister(username,age,gender,mobile_no,password,repeat_password):
    ## check if username exist
    loginInfo, lenLogin = login_db_connector.QueryByUserName(username)
    if lenLogin > 0:
        return form_resp(1002,"Username already exists!",'')
    ## check password
    if password != repeat_password:
        return form_resp(2002,"Repeated password is not consistent!",'')
    ## start transaction
    ## create login info
    res = login_db_connector.Create(username,password)
    ## create user info
    res = user_db_connector.Create(username,age,gender,mobile_no)
    return form_resp(200,"OK",res)

def addLogin(username,password):
    res = login_db_connector.Create(username,password)
    return form_resp(200,"OK",res)

def checkLogin(username,password):
    res,num = login_db_connector.QueryByUserName(username)
    if num==0:
        return form_resp(500,"username doesn't exist!",res)
    else:
        passwdDB = res['dataList'][0]['password']
        if passwdDB != password: 
            return form_resp(501,"password incorrect!",res)
        else:
            return form_resp(200,"OK",res)

def chatWithBot2(prompt):
    number = random.randint(0,100)
    res = "Your prompt is:{}, your number is:{}".format(prompt,number)
    return form_resp(200,"OK",res)

def chatWithSpark(prompt):
    res = sparkPython_functionCall.sendQuestion(prompt)
    return form_resp(200,"OK",res)

def chatWithDeepSeek(prompt):

    client = OpenAI(api_key="YOUR-API-KEY", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            ##{"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    res = response.choices[0].message.content
    return form_resp(200,"OK",res)

def chatWithBot(prompt,model):
    if model=="deepseek-v3":
        return chatWithDeepSeek(prompt)
    elif model=="spark-4.0-ultra":
        return chatWithSpark(prompt)
    else:
        return chatWithDeepSeek(prompt)

def getRandom():
    res = random.randint(1, 100)
    return form_resp(200,"OK",res)

def main():
    res = listUserByPage(10,2)
    print(res)

if __name__ == "__main__":
    main()

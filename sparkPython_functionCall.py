import sparkApi_functionCall
#以下密钥信息从控制台获取

appid = "Your-APP-ID"     #填写控制台中获取的 APPID 信息
api_secret = "Your-API-SECRET"   #填写控制台中获取的 APISecret 信息
api_key ="Your-API-KEY"    #填写控制台中获取的 APIKey 信息

#配置大模型版本
#domain = "generalv3.5"    # Max版本
domain = "4.0Ultra"    # v4.0版本


#云端环境的服务地址

#Spark_url = "ws://spark-api.xf-yun.com/v3.5/chat"  # v3.5环境的地址
Spark_url = "wss://spark-api.xf-yun.com/v4.0/chat"  # v4.0环境的地址

text =[]

# length = 0

def getText(role,content):
    text.clear()
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    
def sendQuestion(prompt):
    question = [{"role":"user","content":prompt}]
    sparkApi_functionCall.answer = ""
    sparkApi_functionCall.main(appid,api_key,api_secret,Spark_url,domain,question)
    return ''.join(sparkApi_functionCall.answer)
    #for chunk in sparkApi_functionCall.answer:
    #    yield f"{chunk}\n"
    #    time.sleep(0.1)

if __name__ == '__main__':

    question = [{"role":"user","content":"今天是星期几?"}]
    sparkApi_functionCall.answer =""
    print("星火:",end = "")
    sparkApi_functionCall.main(appid,api_key,api_secret,Spark_url,domain,question)
    i=0
    for chunk in sparkApi_functionCall.answer:
        i=i+1
        print("chunk:{}, text:{}".format(i,chunk))



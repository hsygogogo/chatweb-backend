from utils import form_resp
import random

class Player():
    def __init__(self,name):
        self.name=name
        self.score=0
        self.num=0

class Game():
    def __init__(self,name1,name2):
        self.PlayerA = Player(name1)
        self.PlayerB = Player(name2)

    def judge(self,number):
        oppo_number = random.randint(1,10)
        if number > oppo_number:
            self.updateScore('A')
        elif number < oppo_number:
            self.updateScore('B')
        return number, oppo_number

    def updateScore(self,player):
        if player=='A':
            self.PlayerA.score += 100
        elif player=='B':
            self.PlayerB.score += 100

    def getScores(self):
        return self.PlayerA.score, self.PlayerB.score
    
    def reset(self):
        self.PlayerA.score=0
        self.PlayerB.score=0
        self.PlayerA.num=0
        self.PlayerB.num=0

newGame = Game("hsy","cpu")

def play(game,inputScore):
    number,oppo_number = game.judge(inputScore)
    resp = {}
    resp['numA']=number
    resp['numB']=oppo_number
    resp['scoreA'],resp['scoreB']=game.getScores()
    return form_resp(200,"OK",resp)

def getScore(game):
    resp = {}
    resp['scoreA'],resp['scoreB']=game.getScores()
    return form_resp(200,"OK",resp)

def restart(game):
    resp = "Game restarts successfully!"
    game.reset()
    return form_resp(200,"OK",resp)

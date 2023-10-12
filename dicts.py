from utils import *
from constants import *

argDict = {
    "n":setn,
    "t":settempreture,
    "savet": save_template,
    "load": load_template,
    "quit": save_chat,
    "exit": save_chat,
    "q": save_chat,
    "q!":exit,
    "reinput": reinput_line,
    "4":setgpt4,
    "3":setgpt3,
    "sys":System,
    "user":common_user,
    "print":lambda :betterPrint(history),
}

defaultFunc=[
    # longText,
    # minBill
]

conDict = {
    "history": history,
    "request": request,
}

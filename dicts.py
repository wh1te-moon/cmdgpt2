from utils import *
from constants import *

argDict = {
    "n":setn,
    "t":settempreture,
    "savet": saveTemplate,
    "load": load_template,
    "quit": saveChat,
    "exit": saveChat,
    "q": saveChat,
    "q!":exit,
    "reinput": reinput_line,
    "4":setgpt4,
    "3":setgpt3,
    "sys":System,
    "user":common_user,
    "print":lambda arg:betterPrint(arg),
    "afresh":afreshAnswer,
    "long":longInput,
}

defaultFunc=[
    # longText,
    # minBill
]

conDict = {
    "history": history,
    "request": request,
}

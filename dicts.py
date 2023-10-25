from utils import *
from constants import *

argDict = {
    "n":setn,
    "t":settempreture,
    "savet": saveTemplate,
    "loadt": load_template,
    "quit": saveChat,
    "exit": saveChat,
    "q": saveChat,
    "q!":exit,
    "reinput": lambda target:reinput_line(target),
    "4":setgpt4,
    "3":setgpt3,
    "sys":System,
    "user":common_user,
    "print":lambda arg:betterPrint(arg),
    "afresh":afreshAnswer,
    "long":longInput,
    "history":showAllHistory,
    "continue":keepAnswering
}

defaultFunc=[
    # longText,
    # minBill
]

conDict = {
    "history": history,
    "request": request,
}

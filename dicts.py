from utils import *
from constants import *

argDict = {
    "n":setn,
    "t":settempreture,
    "save": save_template,
    "load": load_template,
    "quit": save_chat(history),
    "exit": save_chat(history),
    "q": save_chat(history),
    "q!":exit,
    "reinput": reinput_line,
    "4":setgpt4
}

defaultFunc=[
    # longText,
    # minBill
]

conDict = {
    "history": history,
    "request": request,
}
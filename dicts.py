from Utils import Utils
from Constants import constants

from sys import exit

argDict = {
    "n":Utils.setn,
    "t":Utils.settempreture,
    "savet": lambda:constants.waitList.append(Utils.saveTemplate),
    "loadt": Utils.loadTemplate,
    "quit": Utils.saveChat,
    "exit": Utils.saveChat,
    "q": Utils.saveChat,
    "q!":exit,
    "reinput": lambda target:Utils.reinput_line(target),
    "4":Utils.setgpt4,
    "3":Utils.setgpt3,
    "sys":Utils.System,
    "user":Utils.common_user,
    "print":lambda arg:Utils.betterPrint(arg),
    "afresh":Utils.afreshAnswer,
    "long":Utils.longInput,
    "history":Utils.showAllHistory,
    "continue":Utils.keepAnswering,
    "help":lambda:Utils.betterPrint(argDict.keys()),
    "i":Utils.imageInput,
}

defaultFunc=[
    # longText,
    # minBill
    Utils.transfer_slash,
]

conDict = {
    "history": constants.history,
    "request": constants.chatRequest,
}

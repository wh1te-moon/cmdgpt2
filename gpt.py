from chatRequestBody import chatRequestBody,singleContent,message,user
from utils import betterInput, get_response, show_answer
from argsAnalyze import argsAnalyze
from constants import *


def inputProcess(user_input:str, history: list[message], request: chatRequestBody):
    user_input = argsAnalyze(user_input.replace("\\", "/"))
    if user_input:
        history[-1].addContent(singleContent(user_input))
    else:
        return inputProcess(betterInput() if input_pattern[0] == "long" else input(str(index) + f" > {user}: "), history, request)
    request.messages = history
    get_response(request)
    show_answer()
    return


if __name__ == "__main__":
    while (True):
        history.append(message())
        user_input = betterInput() if input_pattern[0] == "long" else input(str(index) + f" > {user}: ")
        inputProcess(user_input, history, chatRequest)
        index += 1

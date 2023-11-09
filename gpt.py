from classes import RequestBody,singleContent,message
from utils import betterInput, get_response, show_answer
from argsAnalyze import argsAnalyze
from constants import *


def inputProcess(user_input:str, history: list[message], request: RequestBody):
    history.append(message())
    user_input = argsAnalyze(user_input.replace("\\", "/"))
    if user_input:
        history[-1].addContent(singleContent(user_input))
    else:
        return inputProcess(betterInput() if input_pattern[0] == "long" else input(str(index) + " > user: "), history, request)
    request.messages = history
    get_response(request)
    show_answer()
    return


if __name__ == "__main__":
    while (True):
        user_input = betterInput() if input_pattern[0] == "long" else input(str(index) + " > user: ")
        inputProcess(user_input, history, request)
        index += 1

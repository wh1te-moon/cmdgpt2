import os
import openai

from classes import RequestBody
from utils import betterInput, get_response, show_answer
from argsAnalyze import argsAnalyze
from constants import *

openai.api_key = os.getenv("OPENAI_API_KEY")


def inputProcess(user_input, history: list, request: RequestBody):
    user_input = argsAnalyze(user_input)
    if user_input:
        history.append(
            {"role": constants["current_role"], "content": user_input})
    else:
        return inputProcess(betterInput() if input_pattern[0] == "long" else input(str(index) + " > user: "), history, request)
    request.message = history
    constants["response"] = get_response(request)
    show_answer()
    return


if __name__ == "__main__":
    while (True):
        user_input = betterInput() if input_pattern[0] == "long" else input(str(index) + " > user: ")
        inputProcess(user_input, history, request)
        index += 1

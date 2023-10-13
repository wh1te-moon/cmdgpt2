import os
import openai

from time import sleep
from classes import RequestBody
from utils import betterInput
from argsAnalyze import argsAnalyze
from constants import *

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_response(request: RequestBody, count=1):
    try:
        response = openai.ChatCompletion.create(
            model=request.model,
            messages=request.message,
            temperature=request.temperature,
            top_p=request.top_p,
            n=request.n,
            stream=request.stream,
            stop=request.stop,
            max_tokens=request.max_tokens,
            presence_penalty=request.presence_penalty,
            logit_bias=request.logit_bias,
            user=request.user
        )
    except Exception as e:
        request.model(gpt3)
        sleep(6*count)
        return get_response(request, count=count+1)
    return response


def inputProcess(user_input, history: list, request: RequestBody):
    user_input = argsAnalyze(user_input)
    if user_input:
        history.append(
            {"role": constants["current_role"], "content": user_input})
    else:
        return inputProcess(betterInput() if input_pattern == "long" else input(str(i) + " > user: "), history, request)
    request.message = history
    constants["response"] = get_response(request)
    print(f" > chatgpt :")
    if (request.stream):
        stream_messages = ""
        for chunk in constants["response"]:
            delta = chunk['choices'][0]['delta']
            if 'content' in delta:
                print(delta['content'], end="")
                stream_messages += delta['content']
        print()
        history.append({"role": "assistant", "content": stream_messages})
    else:
        for choice in request.n:
            print(f" > chatgpt choice {choice} :")
            print(constants["response"]["choices"]
                  [choice]["message"]["content"])
            history.append(
                {"role": "assistant", "content": f"choice {choice}:" +
                 constants["response"]["choices"][choice]["message"]["content"]})
    return


if __name__ == "__main__":
    i = 1
    while (True):
        user_input = betterInput() if input_pattern == "long" else input(str(i) + " > user: ")
        inputProcess(user_input, history, request)
        i += 1

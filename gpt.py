import os
import sys
import openai

from time import sleep
from classes import RequestBody
from utils import betterInput
from argsAnalyze import argsAnalyze
from constants import *

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_response(request: RequestBody,count=1):
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
        request.model(gpt3_long)
        request.max_tokens=16000
        return get_response(request,count=count+1)
    return response


def inputProcess(user_input, history: list, request: RequestBody):
    user_input = argsAnalyze(user_input)
    history.append({"role": constants["current_role"], "content": user_input})
    request.message = history
    constants["response"] = get_response(request)
    for choice in range(request.n):
        print(f"> ChatGPT choice {choice}: ")
        if (request.stream):
            stream_messages = ""
            for chunk in constants["response"]:
                delta = chunk['choices'][choice]['delta']
                if 'content' in delta:
                    print(delta['content'], end="")
                    stream_messages += delta['content']
            print()
            history.append({"role": "assistant", "content": f"choice {choice}:{stream_messages}"})
        else:
            print(constants["response"]["choices"][choice]["message"]["content"])
            history.append(
                {"role": "assistant", "content":f"choice {choice}:"+constants["response"]["choices"][choice]["message"]["content"]})


if __name__ == "__main__":
    i = 1
    while (True):
        user_input = betterInput() if input_pattern == "long" else input(str(i) + " > user: ")
        inputProcess(user_input, history, request)
        i+=1

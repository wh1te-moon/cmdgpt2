import os
import time
import sys
import openai

import tiktoken
from constants import *


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
        time.sleep(6*count)
        return get_response(request, count=count+1)
    return response


def show_answer():
    if (request.stream):
        print(f" > chatgpt :")
        stream_messages = ""
        for chunk in constants["response"]:
            delta = chunk['choices'][0]['delta']
            if 'content' in delta:
                print(delta['content'], end="")
                stream_messages += delta['content']
        print()
        history.append({"role": "assistant", "content": stream_messages})
    else:
        for choice in range(request.n):
            print(f" > chatgpt choice {choice} :")
            print(constants["response"]["choices"]
                  [choice]["message"]["content"])
            history.append(
                {"role": "assistant", "content": f"choice {choice}:" +
                 constants["response"]["choices"][choice]["message"]["content"]})


def setn(n):
    n = int(n)
    request.n = n
    request.stream = False if n >= 2 else True


def settempreture(t):
    t = float(t)
    request.temperature = t


def saveChat():
    with open(
        f"{historyLocation}/{time.asctime( time.localtime(time.time())).replace(' ','_').replace(':','_')}.csv", mode="w", encoding="utf8"
    ) as file:
        for message in history:
            file.write(message["role"] + ": " + message["content"] + "\n\n")
    print("save success")
    exit()


def reinput_line(target):
    target = int(target)
    if len(history) > 2 * target - 1:
        for i in range(2 * target - 1, len(history)):
            if history[i]["role"] == "user":
                history[i]["content"] = input(
                    "> reinput your " + str(target) + " line:"
                )
                print()
                break
        else:
            print(f"No user message found for line {target}")
    else:
        print("Input error\n")


def afreshAnswer():
    history.pop()
    request.message = history
    constants["response"] = get_response(request)
    show_answer()


def saveTemplate():
    file_name = f"{templateLocation}/" + \
        input("Enter file name to load the chat history:")
    with open(file_name, "w", encoding="utf8") as f:
        for message in history:
            if (message['role'] == 'user'):
                f.write(message["role"] + ": " + message["content"] + "\n")
    print("Chat history saved successfully\n")


def System():
    constants["current_role"] = "system"


def common_user():
    constants["current_role"] = "user"


def load_template():
    file_name = input("Enter file name to load the chat history: ")
    try:
        with open(f"{templateLocation}/"+file_name, "r", encoding="utf8") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() != "":
                    if line[0] == "u":
                        history.append(
                            {"role": "user", "content": line[5:].strip()})
                    elif line[0] == "a":
                        history.append(
                            {"role": "assistant", "content": line[5:].strip()})
                    else:
                        history.append(
                            {"role": "system", "content": line[7:].strip()})
            print("Chat history loaded successfully")
    except FileNotFoundError:
        print("File not found\n")


def longInput():
    input_pattern[0]="long"
    print("long input mode")

def betterInput():
    print(" > user: ")
    lines = ""
    while True:
        aLine = sys.stdin.readline()
        if aLine == "END\n":
            break
        lines += aLine
    input_pattern[0]=""
    return lines


def betterPrint(arg):
    if (type(arg) == str):
        print(arg)
    else:
        for i in arg:
            print(i)


def setgpt4():
    request.model = gpt4


def setgpt3():
    request.model = gpt3


def longText(message):
    enc = tiktoken.get_encoding("cl100k_base")
    if (len(enc.encode(message))) > request.max_tokens:
        request.model = gpt3
    return message


def minBill(message):
    return message

def showAllHistory():
    for file in os.listdir(historyLocation):
        print(file)
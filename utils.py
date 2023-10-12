import time
import sys

import tiktoken
from constants import *


def setn(n):
    n = int(n)
    request.n = n
    request.stream = False if n >= 2 else True


def settempreture(t):
    t = float(t)
    request.temperature = t


def save_chat():
    with open(
        f"./history/{time.asctime( time.localtime(time.time())).replace(' ','_').replace(':','_')}.csv", mode="w", encoding="utf8"
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


def save_template():
    file_name = "./template/" + \
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
        with open("./template/"+file_name, "r", encoding="utf8") as f:
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


def betterInput():
    print(" > user: ")
    lines = ""
    while True:
        aLine = sys.stdin.readline()
        if aLine == "END\n":
            break
        lines += aLine
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
        request.model = gpt3_long
        request.max_tokens = 16000
    return message


def minBill(message):
    return message

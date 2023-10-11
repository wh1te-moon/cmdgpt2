import time
import sys

import tiktoken
from constants import *


def setn(n):
    n=int(n)
    request.n=n
def settempreture(t):
    t=float(t)
    request.temperature=t

def save_chat():
    with open(
        f"./history/{time.asctime( time.localtime(time.time())).replace(' ','_')}.csv", mode="w", encoding="utf8"
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


def save_template(history):
    file_name = "./templates/" + \
        input("Enter file name to load the chat history:")
    with open(file_name, "w") as f:
        for message in history:
            f.write(message["role"] + ": " + message["content"] + "\n")
    print("Chat history saved successfully\n")


def System():
    constants["current_role"]="system"


def load_template(history:list):
    file_name = input("Enter file name to load the chat history: ")
    try:
        with open("./templates/"+file_name, "r") as f:
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
            print("Chat history loaded successfully\n")
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

def setgpt4():
    request.model=gpt4


def longText(message):
    enc = tiktoken.get_encoding("cl100k_base")
    if(len(enc.encode(message)))>request.max_tokens:
        request.model=gpt3_long
    return message

def minBill(message):
    return message
from io import TextIOWrapper
import json
import os
import time
import sys

from requests import Response

# import tiktoken
# from requests import get,post,sessions
from constants import *
from chatRequestBody import chatRequestBody, singleContent, contentType, message, roleChoice
from classConfig import user


def get_response(count=1):
    try:
        constants["response"] = chatRequest.get_response()
    except Exception as e:
        chatRequest.model = gpt3
        time.sleep(6*count)
        get_response(chatRequest, count=count+1)


def show_answer():
    if (chatRequest.stream):
        print(f" > {chatRequest.model} :")
        stream_messages = ""
        for chunk in constants["response"].iter_lines(decode_unicode=True):
            try:
                if chunk:
                    chunk = json.loads(chunk[chunk.index('{'):])
                    index = chunk['choices'][0]['index']
                    delta = chunk['choices'][0]['delta']
                    if 'content' in delta:
                        print(delta['content'], end="")
                        stream_messages += delta['content']
            except ValueError as e:
                break
        print()
        history.append({"role": "assistant", "content": stream_messages})
    else:
        for choice in range(chatRequest.n):
            answer = json.loads(constants["response"].text)
            print(f" > {chatRequest.model} choice {choice} :")
            print(answer["choices"][choice]["message"]["content"])
        if chatRequest.n > 1:
            try:
                temp = int(input("which one is better:"))
                history.append(
                    {"role": "assistant", "content": stream_messages[temp-1]})
            except:
                print("input error")
                history.append(
                    {"role": "assistant", "content": stream_messages[0]})
        else:
            history.append({"role": "assistant", "content": answer["choices"]
                            [0]["message"]["content"]})


def setn(n):
    n = int(n)
    chatRequest.n = n
    chatRequest.stream = False if n >= 2 else True


def settempreture(t):
    t = float(t)
    chatRequest.temperature = t

def save(file:TextIOWrapper):
    for message in history[:-1]:
            file.write(f"{message['role']}:")
            if type(message["content"])==str:
                file.write(message["content"])
            else:
                for singleContent in message["content"]:
                    # maybe switch is better
                    if (singleContent["type"] == contentType.text):
                        file.write(singleContent["text"])
                    else:
                        file.write("![]{"+singleContent['image_url']+'}')
            file.write("\n\n")

def saveChat():
    with open(
        f"{historyLocation}/{time.asctime( time.localtime(time.time())).replace(' ','_').replace(':','_')}.md", mode="w", encoding="utf8"
    ) as file:
        save(file)
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
    chatRequest.messages = history
    constants["response"] = get_response(chatRequest)
    show_answer()


def keepAnswering():
    constants["response"] = get_response(chatRequest)
    show_answer()


def saveTemplate():
    file_name = f"{templateLocation}/" + \
        input("Enter file name to load the chat history:")
    with open(file_name, "w", encoding="utf8") as file:
        save(file)
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
                            {"role": "assistant", "content": line[9:].strip()})
                    else:
                        history.append(
                            {"role": "system", "content": line[6:].strip()})
            print("Chat history loaded successfully")
    except FileNotFoundError:
        print("File not found\n")


def longInput():
    input_pattern[0] = "long"
    print("long input mode")


def betterInput():
    print(f" > {user}: ")
    lines = ""
    while True:
        aLine = input()
        if aLine == "END":
            break
        lines += aLine
        lines += '\n'
    input_pattern[0] = ""
    return lines


def betterPrint(arg):
    if (type(arg) == str):
        print(arg)
    else:
        for i in arg:
            print(i)


def setgpt4():
    chatRequest.model = gpt4


def setgpt3():
    chatRequest.model = gpt3


# def longText(message):
#     enc = tiktoken.get_encoding("cl100k_base")
#     if (len(enc.encode(message))) > request.max_tokens:
#         request.model = gpt3
#     return message


def minBill(message):
    """default func

    Args:
        message (_type_): _description_

    Returns:
        _type_: _description_
    """
    return message


def showAllHistory():
    for filename in os.listdir(historyLocation):
        file_path = os.path.join(historyLocation, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                first_line = file.readline()
                print(f"{filename}:\n{first_line}")


def imageInput(imageUrl):
    while (os.path.exists(imageUrl) is not True):
        imageUrl = input("image not found,enter image path:")
    history[-1].addContent(singleContent(imageUrl, contentType.image_url))

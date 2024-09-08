import asyncio
import json
from chatRequestBody import chatRequestBody, singleContent, Message
from audioRequestBody import audioRequestBody
from Utils import Utils
from argsAnalyzer import argsAnalyzer
from Constants import constants
from classConfig import mode,user


def textInputProcess(user_input: str, history: list[Message], request: chatRequestBody):
    user_input = argsAnalyzer(user_input.replace("\\", "/"))
    if user_input:
        history[-1].addContent(singleContent(user_input))
    else:
        return textInputProcess(Utils.betterInput() if constants.input_pattern[0] == "long" else input(str(constants.index) + f" > {user}: "), history, request)
    request.messages = history
    for func in constants.waitList:
        func()
    Utils.get_response(request)
    Utils.showAnswer()
    return


def audioInputProcess(history: list[Message], request: chatRequestBody):
    input = asyncio.run(Utils.inputAudio2Text())
    if input:
        history[-1].addContent(singleContent(input))
    else:
        return audioInputProcess(history, request)
    print(input)
    request.messages = history
    for func in constants.waitList:
        func()
    if constants.chatRequest.stream:
        constants.chatRequest.stream = False
    Utils.get_response(request)
    answer = json.loads(constants.cons["response"].text)
    answer = answer["choices"][0]["message"]["content"]
    constants.history.append({"role": "assistant", "content": answer})
    print(answer)
    asyncio.run(Utils.playText2Audio(answer))


if __name__ == "__main__":
    constants.history.append({"role":"system","content":"You are a helpful assistant"})
    while True:
        match mode:
            case "audio":
                constants.history.append(Message())
                audioInputProcess(constants.history, constants.chatRequest)
                constants.index += 1
                user_input = input("Press Enter to continue,or input command:",end="")
                user_input = argsAnalyzer(user_input.replace("\\", "/"))
            case "text":
                constants.history.append(Message())
                user_input = Utils.betterInput() if constants.input_pattern[0] == "long" else input(
                    str(constants.index) + f" > {user}: ")
                textInputProcess(user_input, constants.history, constants.chatRequest)
                constants.index += 1
            case "_":
                pass
    
    

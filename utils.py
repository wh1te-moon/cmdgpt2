import asyncio
from io import TextIOWrapper
import json
import os
import time
import wave

import numpy as np
import pyaudio
from requests import Response

# import tiktoken
# from requests import get,post,sessions
from Constants import constants
from chatRequestBody import chatRequestBody, singleContent, contentType, Message, roleChoice
from classConfig import user, threshold


class Utils:
    @staticmethod
    def get_response(count=1) -> Response:
        try:
            constants.cons["response"] = constants.chatRequest.get_response(
            )
        except Exception as e:
            constants.chatRequest.model = constants.gpt3
            time.sleep(6*count)
            Utils.get_response(constants.chatRequest, count=count+1)

    # @staticmethod
    # def playStreamAnswer():
    #     stream_messages = ""
    #     for chunk in constants.cons["response"].iter_lines(decode_unicode=True):
    #         try:
    #             if chunk:
    #                 chunk = json.loads(chunk[chunk.index('{'):])
    #                 index = chunk['choices'][0]['index']
    #                 delta = chunk['choices'][0]['delta']
    #                 if 'content' in delta:
    #                     # print(delta['content'], end="")

    #                     stream_messages += delta['content']
    #         except ValueError as e:
    #             break
    #     pass

    @staticmethod
    def showAnswer():
        if (constants.chatRequest.stream):
            print(f" > {constants.chatRequest.model} :")
            stream_messages = ""
            for chunk in constants.cons["response"].iter_lines(decode_unicode=True):
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
            constants.history.append(
                {"role": "assistant", "content": stream_messages})
        else:
            for choice in range(constants.chatRequest.n):
                answer = json.loads(constants.cons["response"].text)
                print(f" > {constants.chatRequest.model} choice {choice} :")
                print(answer["choices"][choice]["message"]["content"])
            if constants.chatRequest.n > 1:
                try:
                    temp = int(input("which one is better:"))
                    constants.history.append(
                        {"role": "assistant", "content": stream_messages[temp-1]})
                except ValueError:
                    print("input error")
                    constants.history.append(
                        {"role": "assistant", "content": stream_messages[0]})
            else:
                constants.history.append({"role": "assistant", "content": answer["choices"]
                                          [0]["message"]["content"]})

    @staticmethod
    def setn(n):
        n = int(n)
        constants.chatRequest.n = n
        constants.chatRequest.stream = False if n >= 2 else True

    @staticmethod
    def settempreture(t):
        t = float(t)
        constants.chatRequest.temperature = t

    @staticmethod
    def save(file: TextIOWrapper):
        for m in constants.history:
            try:
                if not m["content"]:
                    break
            except KeyError:
                break
            file.write(f"{m['role']}:")
            if type(m["content"]) is str:
                file.write(m["content"])
            else:
                for singleContent in m["content"]:
                    # maybe switch is better
                    if (singleContent["type"] == contentType.text):
                        file.write(singleContent["text"])
                    else:
                        file.write("![]{"+singleContent['image_url']+'}')
            file.write("\n\n")

    @staticmethod
    def saveChat():
        with open(
            f"{constants.historyLocation}/{time.asctime( time.localtime(time.time())).replace(' ','_').replace(':','_')}.md", mode="w", encoding="utf8"
        ) as file:
            Utils.save(file)
        print("save success")
        exit()

    @staticmethod
    def reinput_line(target):
        target = int(target)
        if len(constants.history) > 2 * target - 1:
            for i in range(2 * target - 1, len(constants.history)):
                if constants.history[i]["role"] == "user":
                    constants.history[i]["content"] = input(
                        "> reinput your " + str(target) + " line:"
                    )
                    print()
                    break
            else:
                print(f"No user message found for line {target}")
        else:
            print("Input error\n")

    @staticmethod
    def afreshAnswer():
        constants.history.pop()
        constants.chatRequest.messages = constants.history
        constants.cons["response"] = Utils.get_response(
            constants.chatRequest)
        Utils.showAnswer()

    @staticmethod
    def keepAnswering():
        constants.cons["response"] = Utils.get_response(
            constants.chatRequest)
        Utils.showAnswer()

    @staticmethod
    def saveTemplate():
        file_name = f"{constants.templateLocation}/" + \
            input("Enter file name to load the chat history:")
        with open(file_name, "w", encoding="utf8") as file:
            Utils.save(file)
        print("Chat history saved successfully\n")

    @staticmethod
    def System():
        constants.cons["current_role"] = "system"

    @staticmethod
    def common_user():
        constants.cons["current_role"] = "user"

    @staticmethod
    def loadTemplate():
        file_name = input("Enter file name to load the chat history: ")
        try:
            with open(f"{constants.templateLocation}/{file_name}", "r", encoding="utf8") as f:
                content = f.read()
                
                # Splitting the file content based on role indicators
                sections = content.splitlines()
                role, buffer = None, []
                
                for line in sections:
                    # Identify the role and reset the buffer
                    if line.startswith("user:"):
                        if buffer:  # If buffer is not empty, append the previous role's content
                            constants.history.append({"role": role, "content": "\n".join(buffer).strip()})
                        role = "user"
                        buffer = [line[5:].strip()]  # Start new buffer for the role's content
                    elif line.startswith("assistant:"):
                        if buffer:
                            constants.history.append({"role": role, "content": "\n".join(buffer).strip()})
                        role = "assistant"
                        buffer = [line[9:].strip()]
                    elif line.startswith("system:"):
                        if buffer:
                            constants.history.append({"role": role, "content": "\n".join(buffer).strip()})
                        role = "system"
                        buffer = [line[7:].strip()]
                    else:
                        buffer.append(line)  # Accumulate content if it's a continuation of the current role
                
                # Append the last role's content if there's anything left
                if buffer:
                    constants.history.append({"role": role, "content": "\n".join(buffer).strip()})
                    
                print("Chat history loaded successfully")

        except FileNotFoundError:
            print("File not found\n")

    @staticmethod
    def longInput():
        constants.input_pattern[0] = "long"
        print("long input mode")

    @staticmethod
    def betterInput():
        print(f" > {user}: ")
        lines = ""
        while True:
            aLine = input()
            if aLine == "END":
                break
            lines += aLine
            lines += '\n'
        constants.input_pattern[0] = ""
        print("LONG INPUT END")
        return lines

    @staticmethod
    def betterPrint(arg):
        if (type(arg) is str):
            print(arg)
        else:
            for i in arg:
                print(i)

    @staticmethod
    def setgpt4():
        constants.chatRequest.model = constants.gpt4

    @staticmethod
    def setgpt3():
        constants.chatRequest.model = constants.gpt3

    # def longText(message):
    #     enc = tiktoken.get_encoding("cl100k_base")
    #     if (len(enc.encode(message))) > request.max_tokens:
    #         request.model = gpt3
    #     return message

    @staticmethod
    def showAllHistory():
        for filename in os.listdir(constants.historyLocation):
            file_path = os.path.join(constants.historyLocation, filename)

            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    first_line = file.readline()
                    print(f"{filename}:\n{first_line}")

    @staticmethod
    def imageInput(imageUrl):
        while (os.path.exists(imageUrl) is not True):
            imageUrl = input("image not found,enter image path:")
        constants.history[-1].addContent(singleContent(imageUrl,
                                         contentType.image_url))

    @staticmethod
    def transfer_slash(m: str) -> str:
        return m.replace("\\", "/")

    # def fineTuningData(filename, questions, answers):
    #     with open(filename, "w+", encoding="utf8") as f:
    #         for i in range(len(answers)):
    #             d: list[message] = []
    #             d.append(message(roleChoice.system))
    #             d[-1].addContent(singleContent("你是一个网店客服"))
    #             d.append(message())
    #             d[-1].addContent(singleContent(questions[i]))
    #             d.append(message(roleChoice.assistant))
    #             answer = ""
    #             for j in answers[i]:
    #                 answer += j if j else ""
    #             if not answer:
    #                 continue
    #             d[-1].addContent(singleContent(answer))
    #             for t in d:
    #                 t.content = t.content[0].text
    #                 t["content"] = t.content
    #             data = {"messages": d}
    #             f.write(json.dumps(data, ensure_ascii=False)+"\n")

    @staticmethod
    def bytes2np(inp: bytes, sampleWidth: int = 2) -> np.ndarray:
        """
        将音频二进制数据转换为numpy类型
        :param inp: 输入音频二进制流
        :param sampleWidth: 音频采样宽度
        :return: 音频numpy数组
        """

        # 使用np.frombuffer函数将字节序列转换为numpy数组
        tmp = np.frombuffer(
            inp, dtype=np.int16 if sampleWidth == 2 else np.int8)
        # 确保tmp为numpy数组
        tmp = np.asarray(tmp)

        # 获取tmp数组元素的数据类型信息
        i = np.iinfo(tmp.dtype)
        # 计算tmp元素的绝对最大值
        absmax = 2 ** (i.bits - 1)
        # 计算tmp元素的偏移量
        offset = i.min + absmax

        # 将tmp数组元素转换为浮点型，并进行归一化
        array = np.frombuffer(
            (tmp.astype(np.float32) - offset) / absmax, dtype=np.float32)

        # 返回转换后的numpy数组
        return array

    @staticmethod
    def audioPredict(audio: bytes) -> str:
        """
        语音识别
        :param audio: 输入的音频bytes
        :return: 输出识别的字符串结果
        """
        audio = Utils.bytes2np(audio)
        return constants.model.transcribe(audio.astype(np.float32))["text"]

    @staticmethod
    async def playText2Audio(text: str) -> bytes:
        """
        播放音频
        :param audio: 输入的音频bytes
        """
        audio = constants.audioRequest.get_response(text)
        audio_bytes_stream = b""
        stream = constants.audioPlayer.open(
            output=True, channels=1, rate=24000, format=pyaudio.paInt16, output_device_index=3)
        stream.start_stream()
        for chunk in audio.iter_content(chunk_size=2048):
            if chunk:
                print(len(chunk))
                stream.write(chunk)
                audio_bytes_stream += chunk
        stream.stop_stream()
        stream.close()
        return audio_bytes_stream
        # constants.audioPlayer.write(audio)

    @staticmethod
    def audioCallback(in_data, frame_count, time_info, status):
        """
        回调函数
        :param in_data: 输入数据
        :param frame_count: 帧数
        :param time_info: 时间信息
        :param status: 状态
        :return: 输出数据和状态
        """
        now = time.time()
        numpy_data = np.frombuffer(in_data, dtype=np.int16)
        volume = np.abs(numpy_data).mean()
        # 判断是否检测到声音
        if volume >= threshold:
            constants.audio_data.append(in_data)
            constants.last_active_time = now
        else:
            if now - constants.last_active_time > 1:
                if constants.audio_data:
                    constants.audio_segments.append(
                        b''.join(constants.audio_data))
                    constants.audio_data = []
                else:
                    # should not happen
                    raise Exception("no audio data")
                
                if now - constants.last_active_time > 2.5:
                    constants.audioRecording = False
                else:
                    # if interruption lasts less than 2.5 seconds, do nothing
                    pass
            else:
                constants.audio_data.append(in_data)

        return (in_data, pyaudio.paContinue)

    @staticmethod
    async def inputAudio2Text() -> str:
        text = ""
        constants.audioRecording = True
        print("start recording")
        stream = constants.audioRecorder.open(input=True, channels=1, rate=16000, format=pyaudio.paInt16,
                                              input_device_index=1, stream_callback=Utils.audioCallback)
        constants.last_active_time = time.time()
        stream.start_stream()
        # f = wave.open("testrecord.wav", "wb")
        # f.setnchannels(1)
        # f.setsampwidth(constants.audioRecorder.get_sample_size(pyaudio.paInt16))
        # f.setframerate(16000)
        while constants.audioRecording:
            if constants.audio_segments:
                audio = constants.audio_segments.pop(0)
                text += Utils.audioPredict(audio)
                # f.writeframes(audio)
            else:
                await asyncio.sleep(0.1)
        stream.stop_stream()
        stream.close()
        print("recording stop")
        # f.close()
        return text


if __name__ == "__main__":
    # async def main():
    #     text = await Utils.inputAudio2Text()
    #     print(text)

    # asyncio.run(main())
    audio = constants.audioRequest.get_response(
        "Hello! Yes, I can \"hear\" you in the sense that I can read and respond to your messages. How can I assist you today?")
    audio_bytes_stream = b""
    stream = constants.audioPlayer.open(
        output=True, channels=1, rate=24000, format=pyaudio.paInt16, output_device_index=3)
    stream.start_stream()
    for chunk in audio.iter_content(chunk_size=2048):
        if chunk:
            stream.write(chunk)
            audio_bytes_stream += chunk

    # with open("testaudio.wav", "rb") as f:
    #     audio = f.read()
    #     stream.write(audio)
    #     audio_bytes_stream += audio
    stream.stop_stream()
    stream.close()

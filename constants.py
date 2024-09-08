import time
import numpy as np
import whisper
import pyaudio

from chatRequestBody import chatRequestBody, Message
from audioRequestBody import audioRequestBody
from classes import ClearableList

class Constants:
    def __init__(self) -> None:
        self.chatRequest = chatRequestBody()
        self.audioRequest = audioRequestBody()
        self.history: list[Message] = []
        self.cons = {
            "current_role": "user",
            "response": None,
        }
        
        self.audioRecorder=pyaudio.PyAudio()
        self.audioPlayer=pyaudio.PyAudio()
        
        self.audio_segments=[]
        self.audio_data = []
        self.last_active_time = time.time()
        self.audioRecording=True

        self.waitList = ClearableList([])

        self.input_pattern = [""]

        self.index = 1
        self.gpt3 = "gpt-4o-mini"
        self.gpt4 = "gpt-4o-mini"

        self.historyLocation = "./history"
        self.templateLocation = "./template"

        # self.model = whisper.load_model("small.en", device="cuda")
        
constants = Constants()

if __name__=="__main__":
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print((i,dev['name'],dev['maxInputChannels']))
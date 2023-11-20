from chatRequestBody import chatRequestBody,message
from audioRequestBody import audioRequestBody

chatRequest = chatRequestBody()
audioRequest = audioRequestBody()

history:list[message] = []
constants = {
    "current_role": "user",
    "response": None,
}

input_pattern = [""]
index = 1
gpt3 = "gpt-3.5-turbo-16k-0613"
gpt4 = "gpt-4-vision-preview"

historyLocation = "./history"
templateLocation = "./template"

import os
import requests
import base64
from enum import Enum
from sys import exit

user = "xhm"
model = "gpt-4-vision-preview"
temperature = 0.5
top_p = 1
n = 1
stream = False
stop = None
max_tokens = 128000
logit_bias = None
presense_penalty = 0
size = "1024x1024"
response_format = "url"


class roleChoice(str, Enum):
    user = "user"
    system = "system"
    assistant = "assistant"
    function = "function"


class function_callChoice(str, Enum):
    none = "none"
    auto = "auto"


class contentType(str, Enum):
    text = "text"
    image_url = "image_url"


class singleContent(dict):
    type: contentType
    text: str
    image_url: dict

    def __init__(self, text_url, type=contentType.text):
        if (type == contentType.text):
            self.type = contentType.text
            self.text = text_url
            self["type"] = contentType.text
            self["text"] = text_url
        else:
            self.type = contentType.image_url
            with open(text_url, "rb") as image_file:
                self.image_url = {
                    "url": f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"}
                self["type"] = contentType.image_url
                self["image_url"] = self.image_url


class message(dict):
    role: roleChoice
    content: list[singleContent] = []
    name: str = ""
    function_call: object = None

    def __init__(self,user=roleChoice.user, name=user):
        self.role = user
        self.name = name
        self["role"] = user
        self["name"] = name

    def addContent(self,content:singleContent):
        self.content.append(content)
        self["content"] = self.content

class function():
    name: str = ""
    description: str = ""
    parameters: dict = {}


###
class RequestBody():
    model: str = model
    messages: list[message] = []
    functions: list[function] = []
    function_call: function_callChoice = "none"
    temperature: float = temperature
    top_p: float = top_p
    # choices
    n: int = n
    stream: bool = stream
    stop: str or list[str] = stop
    max_tokens: int = max_tokens
    presence_penalty: float = presense_penalty
    logit_bias: dict = logit_bias
    user: str = user

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key is None:
            print("OPENAI_API_KEY environment variable not found.")
            exit()
        self.base_url = 'https://api.openai.com/v1'
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        })

    def get_response(self):
        url = f'{self.base_url}/chat/completions'
        data = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.stream,
            "presence_penalty": self.presence_penalty,
            "user": self.user
        }
        if self.max_tokens:
            data["max_tokens"] = self.max_tokens
        if self.logit_bias:
            data["logit_bias"] = self.logit_bias
        if self.stop:
            data["stop"] = self.stop
        response = self.session.post(url, json=data)

        if response.status_code == 200:
            return response
        else:
            raise Exception(response.status_code, response.text)

###


class completions():
    model: str = model
    prompt: str or list[str] or list[list[str]]
    suffix: str = "null"
    max_tokens: int = max_tokens
    temperature: float = temperature
    top_p: float = top_p
    n: int = n
    stream: bool = stream
    logprobs: int = None
    echo: bool = False
    stop: str or list[str] = stop
    presence_penalty: float = presense_penalty
    frequency_penalty: float = 0
    best_of: int = 1
    logit_bias: dict = None
    user: str = user


class sizeChoice(str, Enum):
    small = "256x256"
    medium = "512x512"
    large = "1024x1024"


class responseChoice(str, Enum):
    url = "url"
    base64 = "base64"


###
class ImageGenerationRequest():
    prompt: str
    n: int = n
    size: sizeChoice = size
    response_format: responseChoice = response_format
    user: str = user


###
class ImageEditingRequest():
    image: str
    mask: str = None
    prompt: str
    n: int = n
    size: sizeChoice = size
    response_format: responseChoice = response_format
    user: str = user


###
class ImageVariationRequest():
    image: str
    n: int = n
    size: sizeChoice = size
    response_format: responseChoice = response_format
    user: str = user

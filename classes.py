from pydantic import BaseModel
from enum import Enum

user = "xhm"
model = "gpt-4-0314"
temperature = 0.5
top_p = 1
n = 1
stream = True
stop = None
max_tokens = None
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


class message(BaseModel):
    role: roleChoice
    content: str
    name: str = ""
    function_call: object = {}


class function(BaseModel):
    name: str = ""
    description: str = ""
    parameters: dict = {}


###
class RequestBody(BaseModel):
    model: str = model
    message: list[dict] = []
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
    logit_bias: dict = {}
    user: str = user


###
class completions(BaseModel):
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
class ImageGenerationRequest(BaseModel):
    prompt: str
    n: int = n
    size: sizeChoice = size
    response_format: responseChoice = response_format
    user: str = user


###
class ImageEditingRequest(BaseModel):
    image: str
    mask: str = None
    prompt: str
    n: int = n
    size: sizeChoice = size
    response_format: responseChoice = response_format
    user: str = user


###
class ImageVariationRequest(BaseModel):
    image: str
    n: int = n
    size: sizeChoice = size
    response_format: responseChoice = response_format
    user: str = user

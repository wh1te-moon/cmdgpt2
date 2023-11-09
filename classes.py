from enum import Enum
from classConfig import user, chatModel, chatTemperature, top_p, n, stream, stop, max_tokens, logit_bias, presense_penalty, size, imageResponseFormat

class completions():
    model: str = chatModel
    prompt: str or list[str] or list[list[str]]
    suffix: str = "null"
    max_tokens: int = max_tokens
    temperature: float = chatTemperature
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
    responseFormat: responseChoice = imageResponseFormat
    user: str = user


###
class ImageEditingRequest():
    image: str
    mask: str = None
    prompt: str
    n: int = n
    size: sizeChoice = size
    responseFormat: responseChoice = imageResponseFormat
    user: str = user


###
class ImageVariationRequest():
    image: str
    n: int = n
    size: sizeChoice = size
    responseFormat: responseChoice = imageResponseFormat
    user: str = user

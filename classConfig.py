import os


user = "xhm"

#gpt-4-1106-preview gpt-4-vision-preview
chatModel = "gpt-4-vision-preview"
chatTemperature = 0.5
top_p = 1
n = 1
stream = True
stop = None
max_tokens = 4096
logit_bias = None
presense_penalty = 0


audioModel = "tts-1"
voice = "alloy"  # alloy, echo, fable, onyx, nova, and shimmer.
audioResponseFormat = "mp3"
speed = 1.0


translationModel = "whisper-1"
translationResponseFormat = "json"
translationTemprature = 0.5

size = "1024x1024"
imageResponseFormat = "url"


baseUrl="https://api.openai.com/v1"
apiKey=os.environ["OPENAI_API_KEY"]
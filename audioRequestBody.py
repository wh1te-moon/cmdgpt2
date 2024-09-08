import time
import requests

from sys import exit

from classConfig import audioModel, voice, audioResponseFormat, speed, baseUrl, apiKey


class audioRequestBody():
    model: str = audioModel
    inputContent: str
    voice: str = voice
    response_format: str = audioResponseFormat
    speed: float = speed

    def __init__(self) -> None:
        self.baseUrl = baseUrl
        self.apiKey = apiKey
        if self.apiKey is None:
            print("OPENAI_API_KEY environment variable not found.")
            exit()
        self.session = requests.session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.apiKey}',
            'Content-Type': 'application/json',
        })

    def get_response(self, input: str) -> requests.Response:
        self.inputContent = input
        url = f'{self.baseUrl}/audio/speech'
        data = {
            "model": self.model,
            "input": self.inputContent,
            "voice": self.voice,
            "response_format": self.response_format,
            "speed": self.speed,
        }
        response = self.session.post(url, json=data, stream=True)

        if response.status_code == 200:
            # with open("./audio_cache/audio.mp3", "wb") as f:
            #     f.write(response.content)
            response.encoding = 'utf8'
            return response
        else:
            raise Exception(response.status_code, response.text)


if __name__ == "__main__":
    a = audioRequestBody()
    response = a.get_response(
        "Hello! Yes, I can \"hear\" you in the sense that I can read and respond to your messages. How can I assist you today?")
    with open("./testaudio.wav", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

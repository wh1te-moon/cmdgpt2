import json
import os
import requests

from sys import exit

from classConfig import apiKey, translationModel, translationResponseFormat, translationTemprature, baseUrl


class translationRequestBody():
    file: str
    model: str = translationModel
    propmt: str = None
    responseFormat: str = translationResponseFormat
    temperature: float = translationTemprature

    def __init__(self) -> None:
        self.baseUrl = baseUrl
        self.apiKey = apiKey
        if self.apiKey is None:
            print("OPENAI_API_KEY environment variable not found.")
            exit()
        self.session = requests.session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.apiKey}',
            'Content-Type': 'multipart/form-data',
        })

    def get_response(self):
        url = f'{self.baseUrl}/audio/translations'
        data = {
            "model": self.model,
            "prompt": self.propmt,
            "response_format": self.responseFormat,
            "temperature": self.temperature,
        }
        # error
        # response = self.session.post(url, json=data, files={'file': (os.path.basename(self.file), open(self.file, 'rb'), 'application/octet-stream'),
        #                                                     'json': (None, json.dumps(data), 'application/json'), })
        # if response.status_code == 200:
        #     return response
        # else:
        #     raise Exception(response.status_code, response.text)


if __name__ == "__main__":
    a = translationRequestBody()
    a.file = "./audio.mp3"
    a.get_response()
    print(a.get_response().text)

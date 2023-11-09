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
            # 'Content-Type': 'multipart/form-data',
        })

    def get_response(self):
        url = f'{self.baseUrl}/audio/translations'
        data = {
            "file": open(self.file, "rb"),
            # "name": os.path.basename(self.file),
            "model": (None,self.model),
            "response_format": (None,self.responseFormat),
            "temperature": (None,str(self.temperature)),
        }
        if self.propmt:
            data["propmt"]=self.propmt
        response = self.session.post(url, files=data)
        if response.status_code == 200:
            return response
        else:
            raise Exception(response.status_code, response.text)


if __name__ == "__main__":
    a = translationRequestBody()
    a.file = "./audio.mp3"
    a.get_response()
    print(a.get_response().text)

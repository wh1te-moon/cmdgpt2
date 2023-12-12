import requests
import os


class API():
    embedding: str = "https://api.openai.com/v1/embeddings"

authroization = f"Bearer {os.environ['OPENAI_API_KEY']}"
vector1 = requests.post(API().embedding, headers={
    "Content-Type": "application/json", "Authorization":authroization},
    json={"input": "能不能尽快发货?亲，请您耐心等待，我们会尽快为您发货的。如有其他问题，请随时告诉我哦。", "model": "text-embedding-ada-002"})
vector2 = requests.post(API().embedding, headers={
    "Content-Type": "application/json", "Authorization":authroization},
    json={"input": "什么时候发货?亲，请您耐心等待，我们会尽快为您发货的。如有其他问题，请随时告诉我哦。", "model": "text-embedding-ada-002"})
input("Press Enter to continue...")


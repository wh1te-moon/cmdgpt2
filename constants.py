from classes import RequestBody,message

request = RequestBody()
history:list[message] = []
constants = {
    "current_role": "user",
    "response": None,
}

input_pattern = [""]
index = 1
gpt3 = "gpt-3.5-turbo-16k-0613"
gpt4 = "gpt-4-0314"

historyLocation = "./history"
templateLocation = "./template"

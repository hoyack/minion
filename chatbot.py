# chatbot.py
import requests
import json
import os
from datetime import datetime
from sseclient import SSEClient

class ChatSession:
    def __init__(self, history_file=None):
        self.url = "http://192.168.0.113:5000/v1/chat/completions"
        self.headers = {"Content-Type": "application/json"}
        self.history_file = history_file
        self.history = self.load_history()

    def load_history(self):
        if self.history_file and os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                return json.load(file)
        return []

    def save_history(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}.json"
        with open(filename, 'w') as file:
            json.dump(self.history, file, indent=4)

    def get_response(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        data = {
            "mode": "instruct",
            "stream": True,
            "messages": self.history
        }

        response = requests.post(self.url, headers=self.headers, json=data, verify=False, stream=True)
        client = SSEClient(response)

        assistant_message = ''
        try:
            for event in client.events():
                if event.data:
                    payload = json.loads(event.data)
                    chunk = payload['choices'][0]['message']['content']
                    assistant_message += chunk
        except Exception as e:
            print("An error occurred:", e)

        self.history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

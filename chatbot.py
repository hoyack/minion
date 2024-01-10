# chatbot.py
# export PYTHONIOENCODING=utf-8
import requests
import json
import os
from datetime import datetime
from sseclient import SSEClient
from dotenv import load_dotenv
from compare import calculate_similarity  # Import for similarity calculation
from rephraser import Rephraser  # Import the Rephraser class
from colorama import Fore, Style

class ChatSession:
    def __init__(self, history_file=None):
        load_dotenv()
        print("Environment variables loaded.")

        base_url = os.getenv('OPENAPI_ENDPOINT', 'http://localhost:5000')
        self.url = f"{base_url}/v1/chat/completions"
        self.headers = {"Content-Type": "application/json"}

        self.history_file = history_file
        self.history = []
        self.rephraser = Rephraser(self.url, self.headers)  # Initialize the Rephraser

    def load_history(self):
        if self.history_file and os.path.exists(self.history_file):
            print(f"Loading history from file: {self.history_file}")
            with open(self.history_file, 'r') as file:
                self.history = json.load(file)
            print(f"Chat history loaded. Current history: {self.history}")
        else:
            print("No existing history file found. Starting with an empty history.")

    def get_response(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        print(f"User message added to history: {user_message}")

        data = {
            "mode": "instruct",
            "stream": True,
            "messages": self.history
        }
        print(f"Sending request to API: {data}")

        response = requests.post(self.url, headers=self.headers, json=data, verify=False, stream=True)
        print(f"Response received. Status code: {response.status_code}")

        client = SSEClient(response)

        assistant_message = ''
        try:
            for event in client.events():
                print(f"Received event: {event}")
                if event.data:
                    payload = json.loads(event.data)
                    chunk = payload['choices'][0]['message']['content']
                    assistant_message += chunk
                    print(f"Received chunk: {chunk}")
        except Exception as e:
            print("An error occurred:", e)

        # Check similarity and initiate rephrase routine if necessary
        while self.check_rephrase_needed(assistant_message):
            assistant_message = self.rephraser.rephrase(user_message)

        # Append the final assistant message to history
        self.history.append({"role": "assistant", "content": assistant_message})
        print(Fore.RED + "HISTORY APPENDED WITH NEW CONTENT" + Style.RESET_ALL)
        return assistant_message

    def check_rephrase_needed(self, assistant_message):
        # Find the last assistant's message in the history
        last_assistant_message = None
        for message in reversed(self.history):
            if message["role"] == "assistant":
                last_assistant_message = message["content"]
                break

        if last_assistant_message is not None:
            similarity_percentage = calculate_similarity(assistant_message, last_assistant_message)
            threshold = float(os.getenv('threshold', '70'))  # Default to 70%
            print(f"Similarity: {similarity_percentage}%, Threshold: {threshold}%")
            return similarity_percentage > threshold
        else:
            print("No previous assistant message to compare.")
            return False
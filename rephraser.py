# rephraser.py
import requests

class Rephraser:
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.headers = headers

    def rephrase(self, original_text):
        """
        Send a request to rephrase the given text.

        Args:
        original_text (str): The text to be rephrased.

        Returns:
        str: The rephrased text.
        """
        return self.send_rephrase_request(original_text)

    def send_rephrase_request(self, text):
        """
        Send a rephrase request to the API.

        Args:
        text (str): The text to be rephrased.

        Returns:
        str: The rephrased text returned by the API.
        """
        rephrase_prompt = ""
        data = {
            "mode": "instruct",
            "messages": [{"role": "user", "content": rephrase_prompt + text}]
        }

        response = requests.post(self.api_url, headers=self.headers, json=data, verify=False)
        if response.status_code == 200:
            payload = response.json()
            return payload['choices'][0]['message']['content']
        else:
            print(f"Error in rephrasing request: {response.status_code}")
            return text  # Return the original text in case of an error

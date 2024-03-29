from chatbot import ChatSession
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to send a message and get a response
def send_message_and_get_response(history_filename, user_message):
    # Create a chat session
    chat_session = ChatSession(history_filename)
    chat_session.load_history()  # Load the history here

    # Send the message and get a response
    response = chat_session.get_response(user_message)
    print(response)

    # Modify the response and send it as an API call
    modified_response = f"say {response}"
    webserver_port = os.getenv('WEBSERVER_PORT', '5500')  # Default to 5500 if not specified
    api_url = f"http://localhost:{webserver_port}/send_message"
    payload = {"message": modified_response}

    # Make the POST request
    response = requests.post(api_url, json=payload)

    # Print the API response
    print(response.text)

# Example usage
# send_message_and_get_response("your_history_file.json", "Hello, how are you?")

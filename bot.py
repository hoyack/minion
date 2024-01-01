from chatbot import ChatSession
import requests

# Function to send a message and get a response
def send_message_and_get_response(history_filename, user_message):
    # Create a chat session
    chat_session = ChatSession(history_filename)

    # Send the message and get a response
    response = chat_session.get_response(user_message)
    print(response)

    # Modify the response and send it as an API call
    modified_response = f"say {response}"
    api_url = "http://localhost:5500/send_message"
    payload = {"message": modified_response}

    # Make the POST request
    response = requests.post(api_url, json=payload)

    # Print the API response
    print(response.text)
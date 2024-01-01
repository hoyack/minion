import json
from bs4 import BeautifulSoup
from bot import send_message_and_get_response

# Function to clean HTML content
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

# Function to transform a message
def transform_message(say_text):
    if say_text.startswith("You say, "):
        role = "assistant"
        content = say_text[len("You say, \""):-1]  # Remove "You say, \"" and trailing quote
    else:
        role = "user"
        content = say_text.split(", \"", 1)[1][:-1] if ", \"" in say_text else say_text
    return {"role": role, "content": content}

# Function to handle messages and write to JSON file
async def handle_message(message):
    data = json.loads(message)
    if data[0] == "text" and "type" in data[2] and data[2]["type"] == "say":
        cleaned_text = clean_html(data[1][0])
        transformed_message = transform_message(cleaned_text)

        # Load existing data from file, append new message, and write back
        try:
            with open("general.json", "r") as file:
                response_data = json.load(file)
        except FileNotFoundError:
            response_data = []

        response_data.append(transformed_message)

        with open("general.json", "w") as file:
            json.dump(response_data, file, indent=4)

        # If the role is "user", send the message to bot.py
        if transformed_message["role"] == "user":
            send_message_and_get_response("general.json", transformed_message["content"])

# Example usage
# await handle_message(your_message)

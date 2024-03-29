from flask import Flask, request, jsonify
import asyncio
import websockets
import json
import threading
import os
from dotenv import load_dotenv
from worldparser import handle_message

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

ws_queue = asyncio.Queue()
ws_loop = asyncio.new_event_loop()

# Global variable to store the last sent message
last_sent_message = None

async def relay_messages(websocket):
    while True:
        message = await ws_queue.get()
        if message is None:
            break
        await websocket.send(message)

@app.route('/send_message', methods=['POST'])
def send_message():
    global last_sent_message
    message = request.json.get("message")
    formatted_message = json.dumps(["text", [message], {"cmdid": 1}])
    last_sent_message = formatted_message  # Store the last sent message
    asyncio.run_coroutine_threadsafe(ws_queue.put(formatted_message), ws_loop)
    return jsonify({"status": "message sent"})

async def websocket_client():
    global last_sent_message
    uri = os.getenv('EVENNIA_WEBSOCKET', 'ws://localhost:4002')
    username = os.getenv("username")
    password = os.getenv("password")

    while True:  # Loop for reconnection attempts
        try:
            async with websockets.connect(uri) as websocket:
                print("WebSocket client connected to Evennia server.")
                connect_command = json.dumps(["text", [f"connect {username} {password}"], {"cmdid": 0}])
                await websocket.send(connect_command)

                if last_sent_message:
                    await websocket.send(last_sent_message)  # Resend the last message after reconnection

                relay_task = asyncio.create_task(relay_messages(websocket))

                while True:
                    try:
                        message = await websocket.recv()
                        print(f"Received: {message}")
                        await handle_message(message)
                    except websockets.exceptions.ConnectionClosed:
                        print("WebSocket connection closed. Attempting to reconnect...")
                        break  # Breaks the inner loop to reconnect

                relay_task.cancel()
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
        await asyncio.sleep(5)  # Wait before attempting to reconnect

def run_flask_app():
    port = int(os.getenv('WEBSERVER_PORT', 5500))  # Default value if not set in .env
    app.run(port=port, use_reloader=False)

def run_websocket_client():
    ws_loop.run_until_complete(websocket_client())

def main():
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    ws_thread = threading.Thread(target=run_websocket_client, daemon=True)

    flask_thread.start()
    ws_thread.start()

    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        # Send "quit" message to the WebSocket server
        quit_message = json.dumps(["text", ["quit"], {"cmdid": 999}])
        asyncio.run_coroutine_threadsafe(ws_queue.put(quit_message), ws_loop).result()
        asyncio.run_coroutine_threadsafe(ws_queue.put(None), ws_loop).result()
        ws_thread.join()
        ws_loop.call_soon_threadsafe(ws_loop.stop)
        flask_thread.join()
        print("Server shutdown complete.")

if __name__ == "__main__":
    main()
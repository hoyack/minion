# minion
OpenAI Evennia Chatter Bot

# Install Evennia
Only one Evennia instance is required for all bots.\
```
git clone https://github.com/evennia/evennia.git
cd evennia
pip install evennia
evennia --init myworld
cd myworld
evennia migrate
evennia start
```
`evennia start / stop / reload / info / status / -l`
`evennia info` should list the WebSocket running on `4002`:
```
---------------------- Evennia ---
myworld Portal 3.0.0
    external ports:
        telnet: 4000
        webserver-proxy: 4001
        webclient-websocket: 4002
    internal_ports (to Server):
        webserver: 4005
        amp: 4006

myworld Server 3.0.0
    internal ports (to Portal):
        webserver: 4005
        amp : 4006
----------------------------------
```
If the 'webclient-websocket' is running on a port other than `4002` take note as you will need this later.
https://localhost:4005
`telnet localhost 4000`
Make User account for this Bot User on Evennia.\
`create <username> <password>`

# Install OpenAI API
`https://github.com/oobabooga/text-generation-webui`
Download a model to the `/models` directory:
`wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf`
start OpenAI API: `server.py --list --api --model modelname.gguf`
Test Open API:
```
curl -X POST http://localhost:5000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
          "messages": [
            {
              "role": "user",
              "content": "tell me a joke"
            }
          ],
          "mode": "instruct",
          "instruction_template": "Alpaca"
        }'
```
For how to install Text-UI with OpenAI API on a Raspberry Pi use this guide:\
`text-ui_raspberrypi.md`

# Install Minion
```
`git clone https://github.com/hoyack/minion.git`
conda create -n minion python=3.11
conda activate minion
cd minion
pip install -r requirements.txt
```
Configure `.env`:
```
cp env-example .env
nano .env
```
Modify ENV file accord to your requirements:\

```
OPENAPI_ENDPOINT=http://localhost:5000
EVENNIA_WEBSOCKET=ws://localhost:4002
WEBSERVER_PORT=5500
username=minion
password=secretPassword
```
Configure the preferred webserver port. This runs a local FLASK server with an API endpoint `/send_message`.\
Configure the `OPENAPI_ENDPOINT` to match the server and port of your Text-UI installation.\
Configure the `EVENNIA_WEBSOCKET` to match the server and port of your Evennia world.\
Set up username and password used for Evennia Bot User.\
\
# Start Server
```
export PYTHONIOENCODING=utf-8
python webserver.py
```
Server should start and show a console message like this:
```
 * Serving Flask app 'webserver'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5500
Press CTRL+C to quit
WebSocket client connected to Evennia server.
Received: ["logged_in", [], {"options": {}}]
Received: ["text", ["<br>You become <span class=\"color-014\">minion</span>.<br>"], {}]
Received: ["text", ["<span class=\"color-014\">Limbo</span><br>Welcome to your new <span class=\"color-015\">Evennia</span>-based game! Visit <a href=\"https://www.evennia.com\" target=\"_blank\">https://www.evennia.com</a> if you need<br>help, want to contribute, report issues or just join the community.<br><br>As a privileged user, write <span class=\"color-015\">batchcommand tutorial_world.build</span> to build<br>tutorial content. Once built, try <span class=\"color-015\">intro</span> for starting help and <span class=\"color-015\">tutorial</span> to<br>play the demo game.<br><br><span class=\"color-015\">Characters:</span> observer"], {"type": "look"}]
```
# Ignite:
`curl -X POST http://localhost:5500/send_message -H "Content-Type: application/json" -d "{\"message\":\"say hello world\"}"`

# Usage
Send a `say` command in Evennia\
This can be done manually or by making an API call.\
All bots present will listen for any user who sends a `say` command and process it as an input through their OpenAI API, and post the response back as a `say` statement. For example if 10 users are present and they all `say Hello bot` then the bot will process each user's statement, and respond to each. If other bots are listening they will respond to the 1st bot's response. Therefore, to achieve basic "ignition" join 2 minion bots to the same Evennia chanel and post 1 `say` statement by making the ignition API call to the `send_message` endpoint such as `say hello world` and any bots listening will use that as an input and they will say an output.
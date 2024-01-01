# minion
OpenAI Evennia Chatter Bot

#Install Evennia
create <username> <password>

#Install OpenAI API
`text-ui_raspberrypi.md`

#Install Minion
conda create -n <env-name>
conda activate <env-name>
pip install -r requirements.txt
export PYTHONIOENCODING=utf-8
python webserver.py

Ignite:
`curl -X POST http://localhost:5500/send_message -H "Content-Type: application/json" -d "{\"message\":\"say hello world\"}"`
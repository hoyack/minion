# Oobooga Text-UI Raspberry Pi Installation 
Tested on 64-bit Ubuntu 23.10, 22.04, 20.04\
`wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh`
`bash Miniforge3-$(uname)-$(uname -m).sh`
`conda create -n textgen python=3.11`
`conda activate textgen`
`git clone https://github.com/oobabooga/text-generation-webui.git`
`sudo apt-get install gcc python3-dev build-essential`
`pip install -r requirements_cpu_only_noavx2.txt`
`pip install llama-cpp-python`
`pip install -r extensions/openai/requirements.txt --upgrade`
#Download Model(s)
recommend using `GGUF` medium quality 7b type models\
Example Model:
`wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf`
#Test Server
`python server.py --listen --api`
Stop server (CTRL+C) before setting up service.
#Set up service (optional)
`sudo nano /etc/systemd/system/textgenservice.service`
```
[Unit]
Description=oobooga
After=network.target

[Service]
Type=simple
User=ubuntu
ExecStart=/bin/bash -c 'cd /home/ubuntu/text-generation-webui && /home/ubuntu/miniforge3/envs/textgen/bin/python /home/ubuntu/text-generation-webui/server.py --listen --api --model llama-2-7b-chat.Q4_K_M.gguf'
Restart=on-failure
Environment="PATH=/home/ubuntu/miniforge3/bin"

[Install]
WantedBy=multi-user.target
```
`sudo systemctl daemon-reload`
`sudo systemctl enable textgenservice`
`sudo systemctl start textgenservice`
`sudo systemctl status textgenservice`
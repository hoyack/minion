# oobabooga Text-UI Raspberry Pi Installation 
Tested on 8GB Pi 4 with 64-bit Ubuntu 23.10, 22.04, 20.04
```
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh
bash Miniforge3-$(uname)-$(uname -m).sh
conda create -n textgen python=3.11
conda activate textgen
git clone https://github.com/oobabooga/text-generation-webui.git
sudo apt-get install gcc python3-dev build-essential
pip install -r requirements_cpu_only_noavx2.txt
pip install llama-cpp-python
pip install -r extensions/openai/requirements.txt --upgrade
```
# Download Model(s)
recommend using `GGUF` medium quality 7b type models\
Example Model:
`wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf`

# Test Server
`python server.py --listen --api`\
Stop server (CTRL+C) before setting up service.

# Set up service (optional)
`sudo nano /etc/systemd/system/textgenservice.service`
```
[Unit]
Description=oobabooga
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
# Start Service
```
sudo systemctl daemon-reload
sudo systemctl enable textgenservice
sudo systemctl start textgenservice
sudo systemctl status textgenservice
```
# Test Service
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
#advanced mounting
`sudo blkid`\
----| /dev/nvme1n1p1: UUID="2a5ffb6d-dca0-4485-aabe-efac685a4a51" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="d6e0e41a-b50c-46aa-91a9-121954ffcc95"\
`sudo nano /etc/fstab`
```
UUID=2a5ffb6d-dca0-4485-aabe-efac685a4a51  /media/ubuntu/2a5ffb6d-dca0-4485-aabe-efac685a4a51  ext4  defaults  0  0
```
save\
`sudo mkdir -p /media/ubuntu/2a5ffb6d-dca0-4485-aabe-efac685a4a51`\
`sudo mount -a`\

`which conda`\
----| /home/ubuntu/anaconda3/bin/conda\
`conda env list`\
----| textgen                  /home/ubuntu/anaconda3/envs/textgen\
`sudo nano /etc/systemd/system/textgenservice.service`
```
[Unit]
Description=oobabooga
After=network.target
RequiresMountsFor=/media/ubuntu/2a5ffb6d-dca0-4485-aabe-efac685a4a51

[Service]
Type=simple
User=hoyack
ExecStart=/bin/bash -c 'cd /media/ubuntu/2a5ffb6d-dca0-4485-aabe-efac685a4a51/ai/text-generation-webui && /home/ubuntu/anaconda3/envs/textgen/bin/python /media/ubuntu/2a5ffb6d-dca0-4485-aabe-efac685a4a51/ai/text-generation-webui/server.py --listen --api --model llama-2-13b-chat.Q5_K_M.gguf'
Restart=on-failure
Environment="PATH=/home/ubuntu/anaconda3/bin"

[Install]
WantedBy=multi-user.target
```

# MikTelBot
This is a Telegram interactive bot that can communicate with Mikrotik via Rest Api

# Credentials
Edit the config.py file to enter your mikrotik credentials

# Usage [ Manual ]
```
sudo apt update -y
```
```
sudo apt install python3 python3-pip -y
```
```
pip3 install pyTelegramBotAPI requests

```
```
git clone https://github.com/safrinnetwork/MikTelBot/
```
```
cd MikTelBot
```
```
python3 bot.py
```
# Auto Start Bot
make this bot run automatically when your server restarts
```
sudo nano /etc/systemd/system/telegram_bot.service

```
```
[Unit]
Description=Telegram Bot
After=network.target

[Service]
User=yourusername
WorkingDirectory=/path/to/your/bot
ExecStart=/path/to/your/bot-env/bin/python3 /path/to/your/bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target

```
```
sudo systemctl daemon-reload
```
```
sudo systemctl enable telegram_bot.service
```
```
sudo systemctl start telegram_bot.service

```

# Full Tutorial
https://youtu.be/7hX_8HCjgJc

# Error Report
admin@ombulo.net

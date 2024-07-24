# MikTelBot
This is a Telegram interactive bot that can communicate with Mikrotik via Rest Api

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
# Button Func
| Button   | Description |
|----------|-------------|
| Interface | Main menu for interface-related options. |
| List | Displays a list of existing interfaces. |
| Disable | Disables the selected interface from the list of interfaces. |
| Enable | Enables the selected interface from the list of interfaces. |
| Monitor | Monitors traffic on the selected interface from the list of interfaces. |
| Rename | Renames the selected interface from the list of interfaces. After selecting, the bot will ask for a new name. |
| Back | Returns to the main menu from the Interface submenu or the Hotspot submenu. |
| Hotspot | Main menu for hotspot-related options. |
| Total | Displays the total number of users, active users, and hosts on the hotspot. |
| Search | Displays a form to search for hotspot users. After entering the user's name, the bot will display the search results. |
| Detail | Displays a form to view details of a hotspot user. After entering the user's name, the bot will display the user's details. |
| Delete | Displays a form to delete a hotspot user. After entering the user's name, the bot will delete that user. |
| Kick | Displays a form to kick an active user from the hotspot. After entering the user's name, the bot will kick that user out. |
| Profile | Displays a list of hotspot profiles. |
| Binding | Displays a list of IP bindings for the hotspot. |
| Generate | Generates new hotspot vouchers. The bot will ask for the profile, number of vouchers, and voucher digit length. |
| Stop | Stops monitoring traffic on the interface that is being monitored. |

# Error Report
admin@ombulo.net

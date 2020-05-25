# system-check
A small script for checking if the instance is idle, and alert user via telegram


In order to run the python code, you need libraries

* telepot 12.7
* psutil 5.7.0


In order to make it run, you should create a config.py file which has following variables inside.

```
TGBOT_AUTH_KEY="YOUR_AUTH_KEY"
ALLOWED_USER="your_username"
ALLOWED_CHAT_ID="blank"
CPU_THRES=100 # Threshold for cpu usage
MEM_THRES=100 # Threshold for memory allocation
WAKEUP_TIME = 20 # In seconds
TRIGGER = 20 # Number of consecutive idle checks

```

In order to get chat id, add your bot from telegram app and simply send <b>alter</b> to the telegram group. It will know where to send idle logs. Remember it is only allowed to ALLOWED_USER.

Use with your own care. This may not be the solution if you are on production.

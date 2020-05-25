import telepot
import time
import config
import logging

from telepot.loop import MessageLoop

bot = None

def start_bot(**kwargs):
    global bot

    assert config.TGBOT_AUTH_KEY != ""
    assert config.ALLOWED_USER != ""

    bot = telepot.Bot(config.TGBOT_AUTH_KEY)
    
    def handle(msg):

        content_type, chat_type, chat_id = telepot.glance(msg)
        logging.info("Message arrived {} {} {}".format(
            content_type, chat_type, chat_id))
        chat_member = bot.getChat(chat_id)
        if chat_member["username"] == config.ALLOWED_USER:
            if content_type == "text" and msg["text"] == "alter":
                define_chat_id(chat_id)
                logging.info("Chat id defined")
        
        return
    MessageLoop(bot, {'chat': handle}).run_as_thread()
    # bot.message_loop(handle)

def define_chat_id(chat_id):
    config.ALLOWED_CHAT_ID=chat_id
    with open("config.py", "r+") as fd:
        everyline = fd.readlines()
        outstr = ""
        for line in everyline:
            if line.find("ALLOWED_CHAT_ID=") == -1:
                outstr += line
            else:
                outstr += 'ALLOWED_CHAT_ID="{}"\n'.format(chat_id)
            
        fd.seek(0)
        fd.write(outstr)

def send_message(msg):
    global bot
    bot.sendMessage(config.ALLOWED_CHAT_ID, msg)
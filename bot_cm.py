#!/usr/bin/env python3

from pyfiles.utils import *
import telebot as telebot
from pyfiles.ProcessEvent import ProcessMsg
import sqlite3
import json
import requests
import logging

logging.basicConfig(level=logging.INFO, filename="bot_cm.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


def main():
    token = read_token()
    replicas = read_replicas()
    bot = telebot.TeleBot(token, parse_mode='html')
    connection = sqlite3.connect('variables/bot_cm.db', check_same_thread=False)
    cursor = connection.cursor()

    # print(replicas)

    @bot.message_handler(content_types=['text', 'photo'])
    def get_msg(msg):
        print(msg)
        ProcessMsg(replicas, cursor, connection, bot, msg, 'msg')

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        ProcessMsg(replicas, connection, bot, call, 'call')

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    try:
        if True:
            main()
    except Exception as e:
        logging.error(e)
        print(e)
        exit()

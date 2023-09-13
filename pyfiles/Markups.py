from telebot import types
import json


# def inline_mu():
#     markup_inline = types.InlineKeyboardMarkup()
#     markup_inline.row_width = 2
#     item1 = types.InlineKeyboardButton(text='Лазерная резка', callback_data='laser')
#     item2 = types.InlineKeyboardButton(text='Сборка', callback_data='build')
#     item3 = types.InlineKeyboardButton(text='Упаковка', callback_data='pack')
#     item4 = types.InlineKeyboardButton(text='Покраска', callback_data='paint')
#     markup_inline.add(item1, item2, item3, item4)
#     return markup_inline


def reply_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.one_time_keyboard = True
    markup.resize_keyboard = True

    texts = [replicas["add_user"], replicas["get_user"]]

    for i in texts:
        markup.add(types.KeyboardButton(i))

    return markup


def reply_back():
    markup = types.ReplyKeyboardMarkup()
    markup.one_time_keyboard = True
    markup.resize_keyboard = True

    texts = [replicas["cancel"]]

    for i in texts:
        markup.add(types.KeyboardButton(i))

    return markup


def reply_back_picture():
    markup = types.ReplyKeyboardMarkup()
    markup.one_time_keyboard = True
    markup.resize_keyboard = True

    texts = [replicas["default_picture"], replicas["cancel"]]

    for i in texts:
        markup.add(types.KeyboardButton(i))

    return markup


def read_replicas():
    with open('variables/replicas.json', 'r') as f:
        json_data = json.loads(f.read())
        return json_data


replicas = read_replicas()

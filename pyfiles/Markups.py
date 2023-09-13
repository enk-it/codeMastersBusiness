from telebot import types
import json




def inline_suggest_cards(profiles):
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.row_width = len(profiles)

    for profile in profiles:
        teleid, uuid, name, surname, position, project, regdate, picture = profile

        item = types.InlineKeyboardButton(text=f'{name} {surname} {project} {position}', callback_data='choose:' + uuid)
        markup_inline.add(item)

    to_start = types.InlineKeyboardButton(text=replicas["to_start"], callback_data='to_start')
    markup_inline.add(to_start)

    return markup_inline


def inline_profile_card(uuid):
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.row_width = 2
    item1 = types.InlineKeyboardButton(text=replicas["edit"], callback_data='edit:' + uuid)
    item2 = types.InlineKeyboardButton(text=replicas["delete"], callback_data='delete:' + uuid)
    item3 = types.InlineKeyboardButton(text=replicas["to_start"], callback_data='to_start')
    markup_inline.add(item1, item2)
    markup_inline.add(item3)
    return markup_inline


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

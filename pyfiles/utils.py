import logging
import json
import requests

logging.basicConfig(level=logging.INFO, filename="bot_cm.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


def make_unique_name(name, names):
    if name not in names:
        return name
    i = 1
    while True:
        if (temp_name := name + ' ({i})'.format(i=i)) not in names:
            return temp_name
        i += 1


def format_profile_data(data):
    text = "ℹ️ Информация о сотруднике:\n"
    text += "🆔 Ф.И: {name} {surname}\n".format(name=data['name'], surname=data['surname'])
    text += "📊 Должность: {position}\n".format(position=data['position'])
    text += "🛠 Проект: {project}\n".format(project=data['project'])
    text += "🗓 Дата регистрации: {regdate}".format(regdate=data['regdate'])

    return text


def get_default_picture():
    with open("variables/default_picture.png", 'rb') as f:
        bytes = f.read()
        return bytes


def get_picture(url):
    photo = requests.get(url)
    if photo.status_code == 200:
        return photo.content
    else:
        raise Exception(photo.reason)


def read_replicas():
    with open('variables/replicas.json', 'r') as f:
        json_data = json.loads(f.read())
        return json_data


def read_token():
    with open('variables/token.json', 'r') as f:
        json_data = json.loads(f.read())
        return json_data["token"]


def filter_profiles(criteria, profiles):
    res = []
    criteria = criteria.strip().lower().split(' ')

    for profile in profiles:
        teleid, uuid, name, surname, position, project, regdate, picture = profile

        if len(criteria) == 1:
            if name.lower() == criteria[0] or surname.lower() == criteria[0]:
                res.append(profile)
        elif len(criteria) == 2:
            if (name.lower() == criteria[0] and surname.lower() == criteria[1]) or (
                    name.lower() == criteria[1] and surname.lower() == criteria[0]):
                res.append(profile)

    return res

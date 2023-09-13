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

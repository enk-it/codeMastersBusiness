from pyfiles.Markups import *
from pyfiles.DataBaseController import DataBaseController as dbc
from pyfiles.utils import *
import logging
import json
import uuid
import time

logging.basicConfig(level=logging.INFO, filename="bot_cm.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


class ProcessMsg:
    def __init__(self, replicas, cursor, connection, bot, msg, actionType):

        logging.log(20, 'Message Received: {message}'.format(message=msg))

        self.replicas = replicas
        self.bot = bot
        self.msg = msg
        self.userID = self.msg.from_user.id
        self.dbc = dbc(cursor, connection, self.userID)

        try:
            self.state = self.dbc.get_state()
        except Exception as e:
            self.dbc.reg_user()
            self.state = self.dbc.get_state()

        self.stateManager = {
            'first_start': self.first_start,
            'menu': self.menu,
            'wait_choice': self.wait_choice,
            'wait_name': self.wait_name,
            'wait_surname': self.wait_surname,
            'wait_position': self.wait_position,
            'wait_project': self.wait_project,
            'wait_picture': self.wait_picture,

            'wait_name_find': self.wait_name_find,
            'wait_choose_doubles': self.wait_choose_doubles,
            'wait_choose_action': self.wait_choose_action
        }

        if actionType == 'msg':

            self.user_name = self.msg.from_user.first_name

            self.chatID = self.msg.chat.id
            self.msgID = self.msg.message_id

            if self.msg.text == '/start':
                print('User started or restarted bot')
                self.state = self.dbc.set_state('first_start')
            elif self.msg.text == self.replicas["to_start"]:
                print('User be back to menu')
                self.state = self.dbc.set_state('menu')
            elif self.msg.text == self.replicas["cancel"]:
                print('User cancelled the process')
                self.state = self.dbc.set_state('menu')

            if self.msg.content_type == "photo" and self.state not in ["wait_picture"]:
                return

            # else:
            #     if self.state is None:
            #         self.dbc.reg_user()
            #     self.state = self.dbc.get_state()
        elif actionType == 'call':
            self.reply_markup_data = self.msg.data
            self.chatID = self.msg.message.chat.id

            if self.state not in ["wait_choose_action", "wait_choose_doubles"]:
                return

        self.stateManager[self.state]()

    # первый запуска бота или рестарт /start
    def first_start(self):
        self.bot.send_message(self.chatID, self.replicas['greeting'].format(username=self.user_name),
                              reply_markup=reply_menu())
        self.state = self.dbc.set_state('wait_choice')

    def menu(self):
        self.bot.send_message(self.chatID, self.replicas['menu'], reply_markup=reply_menu())
        self.state = self.dbc.set_state('wait_choice')

    def wait_choice(self):
        if self.msg.text == self.replicas["add_user"]:
            self.bot.send_message(self.chatID, self.replicas['enter_name'], reply_markup=reply_back())
            self.state = self.dbc.set_state('wait_name')
        elif self.msg.text == self.replicas["get_user"]:
            self.bot.send_message(self.chatID, self.replicas['enter_id_to_find'], reply_markup=reply_back())
            self.state = self.dbc.set_state('wait_name_find')
        else:
            self.bot.send_message(self.chatID, self.replicas['not_found_command'], reply_markup=reply_menu())
            self.state = self.dbc.set_state("menu")

    def wait_name_find(self):
        search_criteria = self.msg.text

        all_profiles = self.dbc.get_profiles()

        suggested_profiles = filter_profiles(search_criteria, all_profiles)

        if len(suggested_profiles) == 0:
            self.bot.send_message(self.chatID, self.replicas['not_found_profiles'], reply_markup=reply_menu())
            self.state = self.dbc.set_state("menu")
        elif len(suggested_profiles) == 1:
            profile = suggested_profiles[0]

            teleid, uuid, name, surname, position, project, regdate, picture = profile
            data = {"name": name, "surname": surname, "position": position, "project": project, "regdate": regdate}

            self.bot.send_photo(self.chatID, picture, caption=format_profile_data(data),
                                reply_markup=inline_profile_card(uuid))
            self.state = self.dbc.set_state("wait_choose_action")
        else:
            self.bot.send_message(self.chatID, self.replicas["found_more_than_one"],
                                  reply_markup=inline_suggest_cards(suggested_profiles))
            self.state = self.dbc.set_state("wait_choose_doubles")

    def wait_choose_doubles(self):
        if self.reply_markup_data == "to_start":
            self.state = self.dbc.set_state("menu")
            self.menu()
        else:
            # todo
            pass


    def wait_choose_action(self):
        if self.reply_markup_data == "to_start":
            self.state = self.dbc.set_state("menu")
            self.menu()
        elif "edit:" in self.reply_markup_data:
            # todo
            pass
        elif "delete:" in self.reply_markup_data:
            uuid = self.reply_markup_data.split(':')[1]
            try:
                self.dbc.delete_profile(uuid)
                self.bot.send_message(self.chatID, self.replicas["deleted_succesfully"], reply_markup=reply_menu())
            except Exception as e:
                logging.error(e)
                print(e)
            finally:
                self.state = self.dbc.set_state("menu")
                self.menu()


    def wait_name(self):
        name = self.msg.text.strip()

        data = self.dbc.get_temp_user()
        data['name'] = name
        self.dbc.set_temp_user(data)

        self.bot.send_message(self.chatID, self.replicas['enter_surname'], reply_markup=reply_back())
        self.state = self.dbc.set_state('wait_surname')

    def wait_surname(self):
        surname = self.msg.text.strip()

        data = self.dbc.get_temp_user()
        data['surname'] = surname
        self.dbc.set_temp_user(data)

        self.bot.send_message(self.chatID, self.replicas['enter_position'], reply_markup=reply_back())
        self.state = self.dbc.set_state('wait_position')

    def wait_position(self):
        position = self.msg.text.strip()

        data = self.dbc.get_temp_user()
        data['position'] = position
        self.dbc.set_temp_user(data)

        self.bot.send_message(self.chatID, self.replicas['enter_project'], reply_markup=reply_back())
        self.state = self.dbc.set_state('wait_project')

    def wait_project(self):
        project = self.msg.text.strip()

        data = self.dbc.get_temp_user()
        data['project'] = project
        self.dbc.set_temp_user(data)

        # self.bot.send_message(self.chatID, str(data))
        self.bot.send_message(self.chatID, self.replicas['enter_picture'], reply_markup=reply_back_picture())
        self.state = self.dbc.set_state('wait_picture')

    def wait_picture(self):
        bytes_picture = None

        if self.msg.text == self.replicas["default_picture"]:
            bytes_picture = get_default_picture()
        elif self.msg.content_type == "photo":
            try:
                photo = self.msg.photo[2]
            except Exception as e:
                logging.error(e)
                print('Не удалось уменьшить картинку')
                photo = self.msg.photo[0]
            file_id = photo.file_id
            file_url = self.bot.get_file_url(file_id)
            try:
                bytes_picture = get_picture(file_url)
            except Exception as e:
                logging.error(e)
                print(e)
                self.state = self.dbc.set_state('menu')
                self.menu()
                return
        else:
            return

        data = self.dbc.get_temp_user()

        data["regdate"] = time.strftime('%d.%m.%Y %H:%M')
        data["uuid"] = str(uuid.uuid4())

        try:
            self.dbc.reg_profile(data["uuid"], data["name"], data["surname"], data["position"], data["project"],
                                 data["regdate"], bytes_picture)
        except Exception as e:
            logging.error(e)
            print(e)
            self.dbc.set_temp_user({})
            self.bot.send_message(self.chatID, self.replicas['error_while_adding'])
            self.state = self.dbc.set_state('menu')
        else:
            self.dbc.set_temp_user({})
            self.bot.send_photo(self.chatID, bytes_picture, caption=format_profile_data(data),
                                reply_markup=inline_profile_card(data["uuid"]))
            self.state = self.dbc.set_state('wait_choose_action')

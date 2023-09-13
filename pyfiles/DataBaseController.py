import threading
import json


class DataBaseController:
    def __init__(self, cursor, connection, user_id=None):
        self.cursor = cursor
        self.connection = connection
        self.user_id = user_id

    def reg_user(self):
        sqlite_insert_query = "INSERT INTO users (telegramID) VALUES ({uid});".format(uid=self.user_id)
        count = self.cursor.execute(sqlite_insert_query)
        self.connection.commit()

    def get_state(self):
        self.cursor.execute("SELECT state FROM users where telegramID={uid};".format(uid=self.user_id))
        return self.cursor.fetchone()[0]

    def set_state(self, state):
        sql_update_query = "Update users set state='{new_state}' where telegramID={uid};".format(new_state=state,
                                                                                                 uid=self.user_id)
        # print(sql_update_query)
        self.cursor.execute(sql_update_query)
        self.connection.commit()
        return state

    def get_message_id(self):
        self.cursor.execute("SELECT messageID FROM users where telegramID={uid};".format(uid=self.user_id))
        return self.cursor.fetchone()[0]

    def set_message_id(self, id):
        sql_update_query = "Update users set messageID='{new_id}' where telegramID={uid};".format(new_id=id,
                                                                                                  uid=self.user_id)
        # print(sql_update_query)
        self.cursor.execute(sql_update_query)
        self.connection.commit()

    def get_temp_user(self) -> {}:
        self.cursor.execute("SELECT temp_employee FROM users where telegramID={uid};".format(uid=self.user_id))

        data = self.cursor.fetchone()[0]

        return json.loads(data)

    def set_temp_user(self, temp_user: {}):
        data = json.dumps(temp_user)

        sql_update_query = "Update users set temp_employee='{data}' where telegramID={uid};".format(data=data,
                                                                                                    uid=self.user_id)
        # print(sql_update_query)
        self.cursor.execute(sql_update_query)
        self.connection.commit()

    def get_all_entries(self):
        sql_query = "SELECT * from users"

        self.cursor.execute(sql_query)
        data = self.cursor.fetchall()

        return data

    def reg_profile(self, uuid: str, name: str, surname: str, position: str, project: str, regdate: str, picture: bytes):
        sqlite_insert_query = "INSERT INTO profiles (telegramID, uuid, name, surname, position, project, regdate, picture) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
        data_tuple = (self.user_id, uuid, name, surname, position, project, regdate, picture)
        count = self.cursor.execute(sqlite_insert_query, data_tuple)
        self.connection.commit()

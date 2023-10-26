import sqlite3 as sq
from create_bot import bot, dp
import datetime

class last_message:

    def __init__(self):
        self._base = sq.connect('omlaut_dataBase.db')
        self._cur = self._base.cursor()

        if self._base:
            print('Data base connected OK!')

        self._base.execute('''
        CREATE TABLE IF NOT EXISTS last_messages (
          chat_id int NOT NULL UNIQUE,
          message_bot_id INT NOT NULL UNIQUE
        )
      ''')

        self._base.commit()

    def update_last_message(self, chat_id, message_bot_id):
        try:
            # Попытка обновления записи, если она уже существует
            self._cur.execute('''
                UPDATE last_messages
                SET message_bot_id = ?
                WHERE chat_id = ?
            ''', (message_bot_id, chat_id))

            if self._cur.rowcount == 0:
                # Если обновления не произошло, значит, записи нет, нужно вставить новую
                self._cur.execute('''
                    INSERT INTO last_messages (chat_id, message_bot_id)
                    VALUES (?, ?)
                ''', (chat_id, message_bot_id))

            self._base.commit()

        except Exception as e:
            print(f"Ошибка при обновлении последнего сообщения: {e}")

    def get_last_message(self, chat_id):
        try:
            self._cur.execute('''
                   SELECT message_bot_id
                   FROM last_messages
                   WHERE chat_id = ?
               ''', (chat_id,))

            result = self._cur.fetchone()

            if result:
                return result[0]  # Возвращаем message_bot_id последнего сообщения бота
            else:
                return None  # Если запись не найдена, возвращаем None

        except Exception as e:
            print(f"Ошибка при получении последнего сообщения: {e}")
            return None  # В случае ошибки также возвращаем None

last_message = last_message()
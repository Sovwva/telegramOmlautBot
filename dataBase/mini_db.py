import asyncio

import aiosqlite
from create_bot import bot, dp
import datetime

class LastMessage:

    def __init__(self):
        self._db_file = 'omlaut_dataBase.db'
        asyncio.run(self.initialize())

    async def initialize(self):
        self._db = await aiosqlite.connect(self._db_file)
        if self._db:
            print('Data base connected OK!')

        await self._db.execute('''
            CREATE TABLE IF NOT EXISTS last_messages (
              chat_id int NOT NULL UNIQUE,
              message_bot_id INT NOT NULL UNIQUE
            )
        ''')
        await self._db.commit()


    async def update_last_message(self, chat_id: int, message_bot_id: int):
        try:
            async with self._db.execute('''
                UPDATE last_messages
                SET message_bot_id = ?
                WHERE chat_id = ?
            ''', (message_bot_id, chat_id)) as cursor:

                if cursor.rowcount == 0:
                    await self._db.execute('''
                        INSERT INTO last_messages (chat_id, message_bot_id)
                        VALUES (?, ?)
                    ''', (chat_id, message_bot_id))

                await self._db.commit()

        except Exception as e:
            print(f"Ошибка при обновлении последнего сообщения: {e}")

    async def get_last_message(self, chat_id) -> int:
        try:
            async with self._db.execute('''
                SELECT message_bot_id
                FROM last_messages
                WHERE chat_id = ?
            ''', (chat_id,)) as cursor:

                result = await cursor.fetchone()

                if result:
                    return result[0]  # Возвращаем message_bot_id последнего сообщения бота
                else:
                    return None  # Если запись не найдена, возвращаем None

        except Exception as e:
            print(f"Ошибка при получении последнего сообщения: {e}")
            return None  # В случае ошибки также возвращаем None


last_message = LastMessage()
import sqlite3 as sq
from create_bot import bot, dp
import datetime


def sql_start():
    global base, cur
    base = sq.connect('omlaut_dataBase.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS cakes (img TEXT, name TEXT, weight INT, price_cake INT, price_dec INT, '
                 'date DATETIME, description TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        if checkTime(ret[5]):
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nВес {ret[2]}\nЦена {ret[3]}\nЦена декорации {ret[4]}\nДата {ret[5]}\nОписание {ret[-1]}')

def checkTime(ret):
    one = str(ret).split("-")
    two = str(datetime.date.today()).split("-")
    if (int(one[0]) >= int(two[0])):
        if (int(one[1]) >= int(two[1])):
            if (int(one[2]) > int(two[2])):
                return True
            else: return False
        else: return False
    else: return False
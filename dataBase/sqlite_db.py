import sqlite3 as sq
from create_bot import bot, dp
import datetime


class OrganizationManager:

    def __init__(self):
        self._base = sq.connect('omlaut_dataBase.db')
        self._cur = self._base.cursor()

        if self._base:
            print('Data base main connected OK!')

        self._base.execute('''
        CREATE TABLE IF NOT EXISTS organizations (
          id INTEGER PRIMARY KEY AUTOINCREMENT,  
          admin_id INTEGER NOT NULL,
          name TEXT NOT NULL UNIQUE,
          password TEXT NOT NULL
        )
      ''')

        self._base.commit()

        self._base.execute('''
          CREATE TABLE IF NOT EXISTS users_organizations (
            chat_id INTEGER NOT NULL UNIQUE,
            organization_id INTEGER NOT NULL,
            FOREIGN KEY (organization_id) REFERENCES organizations(id)
          )
        ''')

        self._base.commit()

        # Создание таблиц шаблонов
        self._base.execute('''
          CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY, 
            name TEXT,
            organization_id INTEGER NOT NULL,
            UNIQUE(name, organization_id)
          )
        ''')

        self._base.commit()

        self._base.execute('''
          CREATE TABLE IF NOT EXISTS template_fields (
            id INTEGER PRIMARY KEY,
            template_id INTEGER NOT NULL,
            name TEXT,
            required INTEGER, 
            FOREIGN KEY (template_id) REFERENCES templates(id)
          )  
        ''')

        self._base.commit()

        self._base.execute('''
          CREATE TABLE IF NOT EXISTS expense_templates (
            id INTEGER PRIMARY KEY, 
            name TEXT,
            organization_id INTEGER NOT NULL,
            UNIQUE(name, organization_id)
          )
        ''')

        self._base.commit()

        self._base.execute('''
          CREATE TABLE IF NOT EXISTS expense_template_fields (
            id INTEGER PRIMARY KEY,
            template_id INTEGER NOT NULL,
            name TEXT,
            required INTEGER, 
            FOREIGN KEY (template_id) REFERENCES templates(id)
          )  
        ''')

        self._base.commit()

    # 1. Создание организации
    def create_organization(self, admin_id, name, password):
        self._base.execute("INSERT INTO organizations (admin_id, name, password) VALUES (?, ?, ?)",
                           (admin_id, name, password))
        self._base.commit()

    # 2. Получение пароля
    def get_organization_password(self, org_id, org_name):
        self._cur.execute("SELECT password FROM organizations WHERE id = ? AND name = ?",
                          (org_id, org_name))
        return self._cur.fetchone()[0]

    # 3. Смена пароля
    def change_password(self, admin_id, org_name, new_password):
        old_password = self.get_organization_password(self, admin_id, org_name)
        if old_password:
            self._base.execute("UPDATE organizations SET password = ? WHERE id = ?",
                               (new_password, admin_id))
            self._base.commit()
        else:
            print("Ошибка смены пароля")

    # 4. Добавление пользователя
    def add_user_to_organization(self, chat_id, org_name, password):
        # Проверка данных
        correct_password = self.get_organization_password(self, chat_id, org_name)
        if not correct_password or correct_password != password:
            print("Неверный пароль организации")
            return

        # Удаление пользователя из других организаций
        self._base.execute("DELETE FROM users_organizations WHERE chat_id = ?", (chat_id,))

        # Добавление в новую
        self._base.execute("INSERT INTO users_organizations (chat_id, organization_id) VALUES (?, ?)",
                           (chat_id, correct_password))

        self._base.commit()

    # 5. Создание шаблона
    def create_template(self, name, organization_id):
        self._base.execute("INSERT INTO templates (name, organization_id) VALUES (?, ?)",
                           (name, organization_id))

    # 6. Добавление поля в шаблон
    def add_template_field(self, template_id, name, required=0):
        self._base.execute("INSERT INTO template_fields (template_id, name, required) VALUES (?, ?, ?)",
                           (template_id, name, required))

    #7. Получение шаблонов
    def get_temlates(self, organization_id):
        self._cur.execute("SELECT name FROM templates WHERE organization_id=?", (organization_id))
        return self._cur.fetchall()

    # # 7. Получение полей шаблона
    # def get_template_fields(self, name, organization):
    #     self._cur.execute("SELECT * FROM template_fields WHERE template_id=?", (template_id,))
    #     return self._cur.fetchall()
    #
    #     # Аналогично для расходов - expense_templates и expense_template_fields

    def create_template(self, name, organization_id):
        self._base.execute("INSERT INTO templates (name, organization_id) VALUES (?, ?)",
                           (name, organization_id))

    # 6. Добавление поля в шаблон
    def add_template_field(self, template_id, name, required=0):
        self._base.execute("INSERT INTO template_fields (template_id, name, required) VALUES (?, ?, ?)",
                           (template_id, name, required))

    # 8. Создание заказа из шаблона:
    # template = get_template(template_id)
    # for field in template:
    #     value = input_field_value(field)  # запросить у пользователя
    #     store_order_field(order_id, field, value)


manager = OrganizationManager()

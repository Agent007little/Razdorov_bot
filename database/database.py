import psycopg2

from config_data.config import load_database, DataBase

# Загружаем данные БД
db: DataBase = load_database()
# Переменная для установки соединения с БД
connection = psycopg2.connect(
    host="localhost",
    user=db.user_db,
    password=db.user_password,
    database=db.name_db)
# Автоматическое сохранение запросов к БД.
connection.autocommit = True


def init_db(force: bool = False):
    """Создаём нужные таблицы если их ещё нет.
    Параметр force в значении True создаст таблицы в базе данных
    или очистит их если они уже созданы и заполнены данными."""
    with connection.cursor() as c:
        if force:
            c.execute("DROP TABLE IF EXISTS users CASCADE")

            c.execute("CREATE TABLE users("
                      "id serial PRIMARY KEY,"
                      "chat_id integer NOT NULL,"
                      "phone integer,"
                      "consultation boolean default FALSE);")


async def save_user(chat_id: int):
    """Функция сохраняющая нового пользователя в БД. Таблица users. """
    with connection.cursor() as c:
        c.execute("INSERT INTO users(chat_id)"
                  "SELECT (%s)"
                  "WHERE NOT EXISTS (SELECT 1 FROM users WHERE chat_id = (%s));", (chat_id, chat_id))


async def get_phone_from_db(chat_id: int):
    """Функция возвращает телефон пользователя по его chatId"""
    with connection.cursor() as c:
        c.execute("SELECT phone "
                  "FROM users "
                  "WHERE chat_id = (%s);", (chat_id,))
        fetchone = c.fetchone()[0]
        return str(fetchone)


async def save_record_in_db(chat_id: int):
    """Функция меняет поле consultation на True"""
    with connection.cursor() as c:
        c.execute("UPDATE users "
                  "SET consultation = true "
                  "WHERE chat_id = (%s);", (chat_id,))

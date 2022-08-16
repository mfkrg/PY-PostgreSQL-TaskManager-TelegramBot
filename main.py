import psycopg2
import telebot
import requests
from config import host, user, password, db_name
connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
connection.autocommit = True
cursor = connection.cursor()
postgreSQL_select_Query = "select * from tasks"
getnickname="select nickname from users"

bot = telebot.TeleBot('5323448846:AAHhQHdJTTEH7uzNRhTjpt8vOYdhlv91KF0')

@bot.message_handler(commands=['start'])
def start(message):
    startMessage = f'Привет, <b><u>{message.from_user.first_name}</u></b>. Для того что бы посмотреть все свои задачи напиши /tasks. Если ты хочешь добавить свою задачу напиши /addtask.'
    bot.send_message(message.chat.id, startMessage, parse_mode='html')

@bot.message_handler(commands=['register'])
def registration(message):
    current_user_nickname = message.from_user.username
    current_user_first_name = message.from_user.first_name
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE nickname = '{current_user_nickname}'")

    res = cursor.fetchall()[0][0]
    if res == 0:
        print(res)
        print("can")
        bot.send_message(message.chat.id, "Ого, тебя нет в списке!\nСейчас я занесу тебя в базу данных, не волнуйся\nПодожди пару секунд и отправь команду еще раз.")
        cursor.execute(f'''INSERT INTO users (first_name, nickname) VALUES ('{current_user_first_name}', '{current_user_nickname}');''')

    else:
        print(res)
        print("already")
        bot.send_message(message.chat.id, "Сейчас ты в базе данных.")
@bot.message_handler(commands=['tasks'])
def get_user_text(message):
    cursor.execute(postgreSQL_select_Query)
    users_records = cursor.fetchall()
    text = '\n\n'.join([', '.join(map(str, x)) for x in users_records])
    bot.send_message(message.chat.id, (str(text)))




bot.polling(none_stop=True)
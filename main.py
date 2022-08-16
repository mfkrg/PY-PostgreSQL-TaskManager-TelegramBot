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

bot = telebot.TeleBot('5323448846:AAHhQHdJTTEH7uzNRhTjpt8vOYdhlv91KF0')

@bot.message_handler(commands=['start'])
def start(message):
    startMessage = f'Привет, <b><u>{message.from_user.first_name}</u></b>. Для того что бы посмотреть все свои задачи напиши /tasks. Если ты хочешь добавить свою задачу напиши /addtask.'
    bot.send_message(message.chat.id, startMessage, parse_mode='html')

@bot.message_handler()
def get_user_text(message):
    if message.text == "/tasks":
        postgreSQL_select_Query = "select * from tasks"
        cursor.execute(postgreSQL_select_Query)
        users_records = cursor.fetchall()
        text = '\n\n'.join([', '.join(map(str, x)) for x in users_records])
        bot.send_message(message.chat.id, (str(text)))




bot.polling(none_stop=True)
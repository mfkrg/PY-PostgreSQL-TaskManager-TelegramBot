import psycopg2
import telebot
from telegram.ext import updater
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
getnickname = "select nickname from users"

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
        bot.send_message(message.chat.id,"Ого, тебя нет в списке!\nСейчас я занесу тебя в базу данных, не волнуйся\nПодожди пару секунд и отправь команду еще раз.")
        cursor.execute(
            f'''INSERT INTO users (first_name, nickname) VALUES ('{current_user_first_name}', '{current_user_nickname}');''')

    else:
        print(res)
        print("already")
        bot.send_message(message.chat.id, "Сейчас ты в базе данных.")


@bot.message_handler(commands=['addtask'])
def add_task(message):
    bot.send_message(message.chat.id, "Хорошо, дай название новой задаче")
    @bot.message_handler(content_types=["text"])
    def adding(message1):
        current_user_nickname = message.from_user.username
        bot.send_message(message.chat.id, """Вы успешно создали новую задачу с названием: '<b><u>"""+message1.text+ "</u></b>'", parse_mode='html')
        cursor.execute(f"INSERT INTO tasks(author, task_name, state) VALUES ('{current_user_nickname}','{message1.text}', 'В ПРОЦЕССЕ')")


@bot.message_handler(commands=['deletetask'])
def delete_task(message):
    bot.send_message(message.chat.id, "Выбери задачу под удаление")
    @bot.message_handler(content_types=["text"])
    def delite_func(message_delete):
        current_user_nickname = message_delete.from_user.username
        cursor.execute(f"DELETE FROM tasks WHERE task_name = '{message_delete.text}'")
        bot.send_message(message_delete.chat.id, """Вы успешно удалили задачу <u><b>""" + message_delete.text +"</b></u>", parse_mode='html')


@bot.message_handler(commands=['complete'])
def complete_task(message):
    bot.send_message(message.chat.id, "Напиши название задачи, статус которой хочешь изменить.")
    @bot.message_handler(content_types=["text"])
    def complete(message_comp):
        cursor.execute(f"SELECT state FROM tasks WHERE task_name = '{message_comp.text}'")
        task_status = cursor.fetchone()[0]
        if task_status == "В ПРОЦЕССЕ":
            cursor.execute(f"UPDATE tasks SET state = 'ГОТОВО' WHERE task_name = '{message_comp.text}'")
            bot.send_message(message_comp.chat.id, "Статус вашей задачи был обновлен на 'ГОТОВО'")
        else:
            cursor.execute(f"UPDATE tasks SET state = 'В ПРОЦЕССЕ' WHERE task_name = '{message_comp.text}'")
            bot.send_message(message_comp.chat.id, "Статус вашей задачи был обновлен на 'В ПРОЦЕССЕ'")



@bot.message_handler(commands=['tasks'])
def get_user_text(message):
    current_user_nickname = message.from_user.username
    cursor.execute(f"SELECT task_name, state FROM tasks WHERE author = '{current_user_nickname}'")
    users_records = cursor.fetchall()
    text = '\n\n'.join(['       '.join(map(str, x)) for x in users_records])
    bot.send_message(message.chat.id, (str(text)))


bot.polling(none_stop=True)

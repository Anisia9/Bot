"""Модуль поддерживает функционал бота"""
import telebot
from telebot import types
from datetime import datetime
from google_sheets import add_to_sheet, create_sheet_connection

bot = telebot.TeleBot("7805032570:AAEosVyvcI7B0KrU4O4lluHYvQQG2WrD8Mg")

sheet = create_sheet_connection("credentials.json", "budget")
user_base = {}

@bot.message_handler(commands=["start", "info"])
def start_handler(message):
    """Выполнение команд start и info"""
    bot.send_message(message.chat.id, f"Привет, <u>{message.from_user.first_name}</u>", parse_mode="html")
    bot.send_message(message.chat.id, "Я — персональный помощник <b>Анисьи</b> для управления финансами через Telegram", parse_mode="html")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Доход", callback_data="income"))
    keyboard.add(types.InlineKeyboardButton("Расход", callback_data="expense"))
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """ Обработка нажатия на кнопку """
    user_input = call.message.chat.id
    if call.data == "income":
        user_base [user_input] = "Доход"
        bot.send_message(call.message.chat.id, "Введите сумму дохода (формат ввода 123):")
    elif call.data == "expense":
        user_base [user_input] = "Расход"
        bot.send_message(call.message.chat.id, "Введите сумму расхода (формат ввода -123):")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_message(message):
    user_input = message.chat.id # Что ответил пользователь
    current_state  = user_base[user_input]

    try:

        number = float(message.text) # Преобразуем текст в число

        if number == 0: # Проверяем не равно ли оно 0
            bot.send_message(user_input, "Вы ввели 0")
            return
       #Проверяем верное ли ввел данные пользователь
        if  current_state  == "Доход" and number < 0:
            bot.send_message(user_input, "Доход должен быть положительный")
            return
        elif current_state == "Расход" and number > 0:
            bot.send_message(user_input, "Расход должен быть отрицательный")
            return

         current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")#Получаем данные о времени ввода
        add_to_sheet(sheet, [current_date,  current_state , number]) #Добавляем данные в таблицу
        bot.send_message(user_input, f"{ current_state } на сумму {number} добавлен в таблицу.")
        del user_base[user_input]#Отчищаем выбор пользователя

    except:
        bot.send_message(user_input, "Ошибка: введите корректное число.")

bot.infinity_polling()




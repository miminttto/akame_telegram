import telebot
from telebot import types
import requests
import time
import random
import datetime

bot = telebot.TeleBot('8351445452:AAEUwAJMPYaam8VTUVgyZVGCplnj6Sey7Ok')

user_last_messages = {}

# Добавляем больше вариантов для поцелуев
kiss_actions = ["поцеловал(а)", "чмокнул(а)", "нежно поцеловал(а)"]

actions = [
    "убил(а)", "ликвидировал(а)", "уничтожил(а)",
    "прикончил(а)", "отправил(а) на тот свет", "лишил(а) жизни"
]

hugs = ["обнял(а)", "прижался(ась) к", "обнял(а) крепко", "обнял(а) нежно"]

# Добавляем гифки для поцелуев
kiss_gifs = [
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NXFvODJzOG85aXh0eXl0aG9ia3Q4NWh1bTdsbzY4ejMwNWE4cmc1cCZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/jR22gdcPiOLaE/giphy.gif",  # Аниме поцелуй
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2R0cTlsaTl2bWxzNHc0OXhxY3JoZm51enlhZ3Vmempkd2tlMmVnbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zkppEMFvRX5FC/giphy.gif",  # Милый поцелуй
]

# Альтернативные рабочие гифки для объятий
hug_gifs = [
    "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",  # Аниме объятия
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGZ5Z3locDlrOTR4ZjJmc2dxdGIxMHc3dGx4ZnViY29xdHRjeDNrMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/u9BxQbM5bxvwY/giphy.gif",  # Аниме парочка
]

glav = types.InlineKeyboardMarkup(row_width=1)

new1 = types.InlineKeyboardMarkup(row_width=1)
new2 = types.InlineKeyboardButton("Новинка", callback_data='new3')

help1 = types.InlineKeyboardMarkup(row_width=1)
help2 = types.InlineKeyboardButton("Помощь", callback_data='help3')

glav.add(help2, new2)

# Функция для экранирования Markdown символов
def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

# Функция для логирования
def log_command(user_id, username, command, target=None, chat_type="private"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] Юзер: @{username}, Команда: {command}, Чат: {chat_type}"
    if target:
        log_message += f", Цель: {target}"

    print(log_message)

    with open("bot_logs.txt", "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

#КНОПКИ
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'help3':
        log_command(call.from_user.id, call.from_user.username or call.from_user.first_name, "help_button")
        bot.send_message(call.message.chat.id, 'Тут можно узнать команды и их использование\n\nakame:kill [юзернейм] - убить человека\nakame:new - новые команды\nakame:hug [юзернейм] - обнять человека\nakame:kiss [юзернейм] - поцеловать человека\n\n🔥Создатель @treplebeska\nДанный бот приватный придобавлении на другой севрер или группу будет выключен!')
    elif call.data == 'new3':
        log_command(call.from_user.id, call.from_user.username or call.from_user.first_name, "new_commands_button")
        bot.send_message(call.message.chat.id, 'Новинка!!!\n\nПоследнее обновление 02.10.2025\n\nДобавлены команды:\nakame:kill\nakame:hug\nakame:kiss\n\nГлобальные обновления:\nДобавлены гифки к командам akame:hug и akame:kiss')

@bot.message_handler(content_types=['text'])
def handle_all_messages(message):
    user_id = message.from_user.id
    text = message.text.strip()
    username = message.from_user.username or message.from_user.first_name

    # Определяем тип чата
    chat_type = "group" if message.chat.type in ["group", "supergroup"] else "private"

    user_last_messages[user_id] = text

    # Обработка команд в группах и личных сообщениях
    if text.lower().startswith('akame:help'):
        log_command(user_id, username, "akame:help", chat_type=chat_type)
        bot.send_message(message.chat.id, 'Тут можно узнать команды и их использование\n\nakame:kill [юзернейм] - убить человека\nakame:new - новые команды\nakame:hug [юзернейм] - обнять человека\nakame:kiss [юзернейм] - поцеловать человека\n\n🔥Создатель @treplebeska\nДанный бот приватный придобавлении на другой севрер или группу будет выключен!')

    # ИСПРАВЛЕННЫЙ КОД ДЛЯ AKAME:KISS
    if text.lower().startswith('akame:kiss'):
        try:
            target = message.text[11:].strip()

            if not target:
                bot.reply_to(message, "❌ Укажи цель: `akame:kiss [имя]`")
                return

            kisser = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

            kiss_action = random.choice(kiss_actions)
            gif_url = random.choice(kiss_gifs)

            # Исправляем сообщение - убираем Markdown разметку для гифки
            kiss_message = f"💋 {kisser} {kiss_action} {target}!"

            log_command(user_id, username, "akame:kiss", target, chat_type)

            # Пытаемся отправить гифку, если ошибка - отправляем только текст
            try:
                bot.send_animation(message.chat.id, gif_url, caption=kiss_message)
            except Exception as gif_error:
                print(f"Ошибка отправки гифки: {gif_error}")
                bot.reply_to(message, kiss_message)

        except Exception as e:
            log_command(user_id, username, "akame:kiss_error", str(e), chat_type)
            bot.reply_to(message, f"❌ Ошибка: {str(e)}")

    if text.lower().startswith('akame:kill '):
        try:
            target = message.text[11:].strip()

            if not target:
                bot.reply_to(message, "❌ Укажи цель: `akame:kill [имя]`")
                return

            killer = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

            action = random.choice(actions)

            # Экранируем имена для Markdown
            killer_escaped = escape_markdown(killer)
            target_escaped = escape_markdown(target)

            kill_message = f"⚔️ **{killer_escaped}** {action} **{target_escaped}**!"

            log_command(user_id, username, "akame:kill", target, chat_type)
            bot.reply_to(message, kill_message, parse_mode='Markdown')

        except Exception as e:
            log_command(user_id, username, "akame:kill_error", str(e), chat_type)
            bot.reply_to(message, f"❌ Ошибка: {str(e)}")

    if text.startswith('/start'):
        bot.send_message(message.chat.id, 'Привет я Акаме.\nЯ создана чтобы добавить развлечения в телеграмм группу или сервер развлечения!', reply_markup=glav)

    if text.lower().startswith('akame:new'):
        log_command(user_id, username, "akame:new", chat_type=chat_type)
        bot.send_message(message.chat.id, 'Новинка!!!\n\nПоследнее обновление 02.10.2025\n\nДобавлены команды:\nakame:kill\nakame:hug\nakame:kiss\n\nГлобальные обновления:\nДобавлены гифки к командам akame:hug и akame:kiss')

    if text.lower().startswith('akame:hug'):
        try:
            target = message.text[10:].strip()

            if not target:
                bot.reply_to(message, "❌ Укажи цель: `akame:hug [имя]`")
                return

            huger = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

            hug = random.choice(hugs)
            gif_url = random.choice(hug_gifs)  # Случайная гифка из списка

            hug_message = f"🤗 {huger} {hug} {target}!"

            log_command(user_id, username, "akame:hug", target, chat_type)

            # Пытаемся отправить гифку, если ошибка - отправляем только текст
            try:
                bot.send_animation(message.chat.id, gif_url, caption=hug_message)
            except Exception as gif_error:
                print(f"Ошибка отправки гифки: {gif_error}")
                bot.reply_to(message, hug_message)

        except Exception as e:
            log_command(user_id, username, "akame:hug_error", str(e), chat_type)
            bot.reply_to(message, f"❌ Ошибка: {str(e)}")

    # Обработка команд с упоминанием бота в группах
    if chat_type in ["group", "supergroup"] and f"@{bot.get_me().username}" in text.lower():
        bot_text = text.replace(f"@{bot.get_me().username}", "").strip()

        if bot_text.lower().startswith('kill '):
            try:
                target = bot_text[5:].strip()

                if not target:
                    bot.reply_to(message, "❌ Укажи цель: `kill [имя]`")
                    return

                killer = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

                action = random.choice(actions)

                # Экранируем имена для Markdown
                killer_escaped = escape_markdown(killer)
                target_escaped = escape_markdown(target)

                kill_message = f"⚔️ **{killer_escaped}** {action} **{target_escaped}**!"

                log_command(user_id, username, "akame:kill", target, chat_type)
                bot.reply_to(message, kill_message, parse_mode='Markdown')

            except Exception as e:
                log_command(user_id, username, "akame:kill_error", str(e), chat_type)
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")

        elif bot_text.lower().startswith('hug '):
            try:
                target = bot_text[4:].strip()

                if not target:
                    bot.reply_to(message, "❌ Укажи цель: `hug [имя]`")
                    return

                huger = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

                hug = random.choice(hugs)
                gif_url = random.choice(hug_gifs)  # Случайная гифка из списка

                hug_message = f"🤗 {huger} {hug} {target}!"

                log_command(user_id, username, "akame:hug", target, chat_type)

                # Пытаемся отправить гифку, если ошибка - отправляем только текст
                try:
                    bot.send_animation(message.chat.id, gif_url, caption=hug_message)
                except Exception as gif_error:
                    print(f"Ошибка отправки гифки: {gif_error}")
                    bot.reply_to(message, hug_message)

            except Exception as e:
                log_command(user_id, username, "akame:hug_error", str(e), chat_type)
                bot.reply_to(message, f"❌ Ошибка: {str(e)}")

        elif bot_text.lower().startswith('help'):
            log_command(user_id, username, "akame:help", chat_type=chat_type)
            bot.reply_to(message, 'Тут можно узнать команды и их использование\n\nakame:kill [юзернейм] - убить человека\nakame:new - новые команды\nakame:hug [юзернейм] - обнять человека\nakame:kiss [юзернейм] - поцеловать человека\n\n🔥Создатель @treplebeska')

bot.polling(none_stop=True)
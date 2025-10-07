import telebot
from telebot import types
import random
import datetime
import time
import logging
import threading

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AkameBot')

bot = telebot.TeleBot('8353863888:AAF255dYhhiihQR_-A_x9_rSJJZcJaTJhHs')

# RP действия
slap_actions = ["шлёпнул(а)", "дал(а) подзатыльник", "отхлестал(а)"]
kiss_actions = ["поцеловал(а)", "чмокнул(а)", "нежно поцеловал(а)"]
kill_actions = ["убил(а)", "ликвидировал(а)", "уничтожил(а)", "прикончил(а)"]
hug_actions = ["обнял(а)", "прижал(а) к груди", "обнял(а) крепко"]
myr_actions = ["помур-р-р-рчал(а)"]

# Список ID модераторов (замени на реальные ID)
MODERATOR_IDS = [
    123456789,  # замени на ID первого модератора
    987654321,  # замени на ID второго модератора
    # добавь больше ID по необходимости
]

# ID создателя (замени на свой реальный ID)
CREATOR_ID = 6695319414

# Хранилище замученных пользователей {user_id: unmute_time}
muted_users = {}

# Гифки
kiss_gifs = [
    "https://media.giphy.com/media/jR22gdcPiOLaE/giphy.gif",
    "https://media3.giphy.com/media/zkppEMFvRX5FC/giphy.gif",
]

hug_gifs = [
    "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
    "https://media4.giphy.com/media/u9BxQbM5bxvwY/giphy.gif",
]

myr_gifs = [
    ""
]

slap_gifs = [
    "https://media.giphy.com/media/Zau0yrl17uzdK/giphy.gif",  
    "https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif",  
]

# Клавиатуры
glav = types.InlineKeyboardMarkup()
help_btn = types.InlineKeyboardButton("Помощь", callback_data='help')
new_btn = types.InlineKeyboardButton("Новинка", callback_data='new')
glav.add(help_btn, new_btn)

# Функция проверки прав
def is_moderator(user_id):
    """Проверяет, является ли пользователь модератором"""
    return user_id in MODERATOR_IDS or user_id == CREATOR_ID

def is_creator(user_id):
    """Проверяет, является ли пользователь создателем"""
    return user_id == CREATOR_ID

def get_time_from_string(time_str):
    """Конвертирует строку времени в секунды"""
    if not time_str[:-1].isdigit():
        return None

    time_number = int(time_str[:-1])
    time_unit = time_str[-1].lower()

    if time_unit == 's':  # секунды
        return time_number
    elif time_unit == 'm':  # минуты
        return time_number * 60
    elif time_unit == 'h':  # часы
        return time_number * 3600
    elif time_unit == 'd':  # дни
        return time_number * 86400
    elif time_unit == 'w':  # недели
        return time_number * 604800
    else:
        return None

def get_display_time(time_str):
    """Возвращает время в читаемом формате"""
    time_number = int(time_str[:-1])
    time_unit = time_str[-1].lower()

    if time_unit == 's':
        return f"{time_number} секунд"
    elif time_unit == 'm':
        return f"{time_number} минут"
    elif time_unit == 'h':
        return f"{time_number} часов"
    elif time_unit == 'd':
        return f"{time_number} дней"
    elif time_unit == 'w':
        return f"{time_number} недель"
    return "неизвестное время"

def log_command(user_id, username, command, target=None, result="успешно"):
    """Логирование команд"""
    logger.info(f"Команда: {command} | Пользователь: {username} (ID: {user_id}) | Цель: {target} | Результат: {result}")

def delete_message_after_delay(chat_id, message_id, delay=15):
    """Удаляет сообщение через указанное количество секунд"""
    def delete():
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, message_id)
            logger.debug(f"Сообщение {message_id} удалено через {delay} секунд")
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения {message_id}: {e}")

    thread = threading.Thread(target=delete)
    thread.daemon = True
    thread.start()

def send_message_with_auto_delete(chat_id, text, parse_mode=None, reply_to_message_id=None, delay=15):
    """Отправляет сообщение и автоматически удаляет его через указанное время"""
    try:
        sent_message = bot.send_message(chat_id, text, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id)
        delete_message_after_delay(chat_id, sent_message.message_id, delay)
        return sent_message
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        return None

def reply_with_auto_delete(message, text, parse_mode=None, delay=15):
    """Отвечает на сообщение и автоматически удаляет ответ через указанное время"""
    try:
        sent_message = bot.reply_to(message, text, parse_mode=parse_mode)
        delete_message_after_delay(message.chat.id, sent_message.message_id, delay)
        return sent_message
    except Exception as e:
        logger.error(f"Ошибка при ответе на сообщение: {e}")
        return None

def send_animation_with_auto_delete(chat_id, animation, caption=None, delay=15):
    """Отправляет анимацию и автоматически удаляет её через указанное время"""
    try:
        sent_message = bot.send_animation(chat_id, animation, caption=caption)
        delete_message_after_delay(chat_id, sent_message.message_id, delay)
        return sent_message
    except Exception as e:
        logger.error(f"Ошибка при отправке анимации: {e}")
        return None

def get_user_id_by_username(chat_id, username):
    """Получает ID пользователя по юзернейму в чате"""
    try:
        # Получаем всех администраторов чата
        admins = bot.get_chat_administrators(chat_id)

        # Ищем среди администраторов
        for admin in admins:
            if admin.user.username and admin.user.username.lower() == username.lower():
                return admin.user.id

        # Если не нашли среди администраторов, пытаемся найти среди участников
        # ВНИМАНИЕ: Этот метод может не работать в больших чатах
        # В реальном боте лучше использовать другие методы поиска
        logger.warning(f"Пользователь @{username} не найден среди администраторов. Поиск по юзернейму может быть ограничен.")
        return None

    except Exception as e:
        logger.error(f"Ошибка при поиске пользователя @{username}: {e}")
        return None

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'help':
        logger.info(f"Callback: help | Пользователь: {call.from_user.username} (ID: {call.from_user.id})")
        bot.send_message(call.message.chat.id, 
        '''🎮 *СПРАВКА ПО КОМАНДАМ* 🎮

Здесь вы можете узнать все доступные команды и их использование!

╔═══════════════════════╗
║              🎯КОМАНДЫ БОТА              ║
╚═══════════════════════╝
• 🔫 `a:kill [юзернейм]` — устранить пользователя
• 🆕 `a:new` — список последних обновлений
• 🤗 `a:hug [юзернейм]` — обнять пользователя
• 💋 `a:kiss [юзернейм]` — поцеловать пользователя
• 😻 `a:myr [юзернейм]` — помурчать на пользователя
• 👋 `a:slap [юзернейм]` — шлепнуть пользователя

╔═══════════════════════╗
║           ⚡МОДЕРСКИЕ КОМАНДЫ           ║
╚═══════════════════════╝
• 🔇 `!mute @юзернейм время причина` — замутить по юзернейму
• 🔇 `!mute время причина` — замутить (ответом на сообщение)
• 🔊 `!unmute` — размутить (ответом на сообщение)
• 📋 `a:staffcmd` — список модерских команд

*Время:*
s - секунда | m - минута | h - час
d - день   | w - неделя

*Примеры:*
`!mute @username 5m спам`
Ответь на сообщение и напиши `!mute 5m спам`

╔═══════════════════════╗
║                  👨‍💻 СОЗДАТЕЛЬ                   ║
╚═══════════════════════╝

🔥 @treplebeska''', parse_mode='Markdown')

    elif call.data == 'new':
        logger.info(f"Callback: new | Пользователь: {call.from_user.username} (ID: {call.from_user.id})")
        bot.send_message(call.message.chat.id, 
        '''🏴‍☠️ НОВИНКА!!!

🗓 Последнее обновление 02.10.2025

🦾 Добавлены команды:

a:kill
a:hug
a:kiss
a:slap
a:myr
!mute (через ответ и по юзернейму)
!unmute (через ответ)
a:staffcmd

🎬 Глобальные обновления:

• Добавлена система логирования
• Добавлен мут по юзернейму
• Теперь вместо `akame:` можно писать `a:`
• Добавлен НАСТОЯЩИЙ мут через ответ на сообщения!''')

@bot.message_handler(commands=['start'])
def start(message):
    logger.info(f"Команда: /start | Пользователь: {message.from_user.username} (ID: {message.from_user.id}) | Чат: {message.chat.id}")
    bot.send_message(message.chat.id, 'Привет я Акаме.\nЯ создана чтобы добавить развлечения в телеграмм группу или сервер развлечения!\n\n(дᴀнный боᴛ нᴀходиᴛьᴄя ʙ ᴩᴀзᴩᴀбоᴛᴋᴇ, ᴨо϶ᴛоʍу ʍоᴦуᴛ быᴛь бᴀᴦи и чᴀᴄᴛо ʙыᴋᴧючᴇн.)', reply_markup=glav)

# РП КОМАНДЫ (без автоудаления)
# kill команда
@bot.message_handler(func=lambda message: message.text.startswith('a:kill'))
def kill_rp(message):
    try:
        target = message.text.replace('a:kill', '').strip()
        if not target:
            log_command(message.from_user.id, message.from_user.username, 'a:kill', result='ошибка: не указана цель')
            bot.reply_to(message, '❌ Укажи кого убить: `a:kill [имя]`')
            return

        killer = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        action = random.choice(kill_actions)

        log_command(message.from_user.id, message.from_user.username, 'a:kill', target)
        bot.reply_to(message, f'⚔️ {killer} {action} {target}!')

    except Exception as e:
        logger.error(f"Ошибка в a:kill: {e} | Пользователь: {message.from_user.username} (ID: {message.from_user.id})")
        bot.reply_to(message, f'❌ Ошибка: {e}')

# hug команда
@bot.message_handler(func=lambda message: message.text.startswith('a:hug'))
def hug_rp(message):
    try:
        target = message.text.replace('a:hug', '').strip()
        if not target:
            log_command(message.from_user.id, message.from_user.username, 'a:hug', result='ошибка: не указана цель')
            bot.reply_to(message, '❌ Укажи кого обнять: `a:hug [имя]`')
            return

        hugger = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        action = random.choice(hug_actions)
        gif = random.choice(hug_gifs)

        log_command(message.from_user.id, message.from_user.username, 'a:hug', target)
        bot.send_animation(message.chat.id, gif, caption=f'🤗 {hugger} {action} {target}!')

    except Exception as e:
        logger.error(f"Ошибка в a:hug: {e} | Пользователь: {message.from_user.username} (ID: {message.from_user.id})")
        bot.reply_to(message, f'❌ Ошибка: {e}')

# kiss команда
@bot.message_handler(func=lambda message: message.text.startswith('a:kiss'))
def kiss_rp(message):
    try:
        target = message.text.replace('a:kiss', '').strip()
        if not target:
            log_command(message.from_user.id, message.from_user.username, 'a:kiss', result='ошибка: не указана цель')
            bot.reply_to(message, '❌ Укажи кого поцеловать: `a:kiss [имя]`')
            return

        kisser = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        action = random.choice(kiss_actions)
        gif = random.choice(kiss_gifs)

        log_command(message.from_user.id, message.from_user.username, 'a:kiss', target)
        bot.send_animation(message.chat.id, gif, caption=f'💋 {kisser} {action} {target}!')

    except Exception as e:
        logger.error(f"Ошибка в a:kiss: {e} | Пользователь: {message.from_user.username} (ID: {message.from_user.id})")
        bot.reply_to(message, f'❌ Ошибка: {e}')

# myr команда
@bot.message_handler(func=lambda message: message.text.startswith('a:myr'))
def myr_rp(message):
    try:
        target = message.text.replace('a:myr', '').strip()
        if not target:
            log_command(message.from_user.id, message.from_user.username, 'a:myr', result='ошибка: не указана цель')
            bot.reply_to(message, '❌ Укажи кому помурчать:3: `a:myr [имя]`')
            return

        myrer = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        action = random.choice(myr_actions)
        gif = random.choice(myr_gifs)

        log_command(message.from_user.id, message.from_user.username, 'a:myr', target)
        if gif:
            bot.send_animation(message.chat.id, gif, caption=f'😻 {myrer} {action} {target} :3')
        else:
            bot.reply_to(message, f'😻 {myrer} {action} {target} :3')

    except Exception as e:
        logger.error(f"Ошибка в a:myr: {e} | Пользователь: {message.from_user.username} (ID: {message.from_user.id})")
        bot.reply_to(message, f'❌ Ошибка: {e}')

# slap команда
@bot.message_handler(func=lambda message: message.text.startswith('a:slap'))
def slap_rp(message):
    try:
        target = message.text.replace('a:slap', '').strip()
        if not target:
            log_command(message.from_user.id, message.from_user.username, 'a:slap', result='ошибка: не указана цель')
            bot.reply_to(message, '❌ Укажи кого шлепнуть: `a:slap [имя]`')
            return

        slapper = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        action = random.choice(slap_actions)
        gif = random.choice(slap_gifs)

        log_command(message.from_user.id, message.from_user.username, 'a:slap', target)
        bot.send_animation(message.chat.id, gif, caption=f'👋 {slapper} {action} {target}!')

    except Exception as e:
        logger.error(f"Ошибка в a:slap: {e} | Пользователь: {message.from_user.username} (ID: {message.from_user.id})")
        bot.reply_to(message, f'❌ Ошибка: {e}')

# КОМАНДА STAFFCMD - список модерских команд
@bot.message_handler(func=lambda message: message.text.startswith('a:staffcmd'))
def staffcmd(message):
    try:
        # Проверяем права пользователя
        user_id = message.from_user.id
        if not is_moderator(user_id):
            log_command(message.from_user.id, message.from_user.username, 'a:staffcmd', result='отказ в доступе')
            reply_with_auto_delete(message, '❌ У вас нет прав для использования этой команды!')
            return

        log_command(message.from_user.id, message.from_user.username, 'a:staffcmd')
        staff_commands = """🛡 *МОДЕРСКИЕ КОМАНДЫ*

🔇 *Мут (два способа):*
• `!mute @юзернейм время причина` - замутить по юзернейму
• `!mute время причина` - замутить (ответом на сообщение)
• `!unmute` - размутить (ответом на сообщение)

👮 *Управление модераторами:*
• `!addmod ID` - добавить модератора
• `!delmod ID` - удалить модератора  
• `!modlist` - список модераторов

*Примеры использования мута:*
1. `!mute @username 5m спам`
2. Ответь на сообщение и напиши `!mute 5m спам`

*Время:*
s - секунды, m - минуты, h - часы, d - дни, w - недели"""

        reply_with_auto_delete(message, staff_commands, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Ошибка в a:staffcmd: {e} | Пользователь: {message.from_user.username} (ID: {message.from_user.id})")
        reply_with_auto_delete(message, f'❌ Ошибка: {str(e)}')

# 🔥 ИСПРАВЛЕННАЯ КОМАНДА MUTE ПО ЮЗЕРНЕЙМУ
@bot.message_handler(func=lambda message: message.text.startswith('!mute') and not message.reply_to_message)
def mute_username_command(message):
    try:
        # Проверяем, что команда в группе
        if message.chat.type not in ['group', 'supergroup']:
            reply_with_auto_delete(message, '❌ Эта команда работает только в группах!')
            return

        # Проверяем права пользователя
        user_id = message.from_user.id
        if not is_moderator(user_id):
            log_command(message.from_user.id, message.from_user.username, '!mute @username', result='отказ в доступе')
            reply_with_auto_delete(message, '❌ У вас нет прав для использования этой команды!')
            return

        # Проверяем, что бот является администратором
        chat_member = bot.get_chat_member(message.chat.id, bot.get_me().id)
        if not chat_member.status == 'administrator':
            reply_with_auto_delete(message, '❌ Бот должен быть администратором для мута пользователей!')
            return

        parts = message.text.split()
        if len(parts) < 4:
            reply_with_auto_delete(message, '❌ Формат: `!mute @юзернейм время причина`\n\n*Пример:*\n`!mute @username 5m спам`')
            return

        username = parts[1]
        time_str = parts[2]
        reason = ' '.join(parts[3:])

        # Проверяем формат времени
        mute_seconds = get_time_from_string(time_str)
        if mute_seconds is None:
            reply_with_auto_delete(message, '❌ Неправильный формат времени!\n*Примеры:*\n`30s` - 30 секунд\n`5m` - 5 минут\n`1h` - 1 час\n`2d` - 2 дня\n`1w` - 1 неделя')
            return

        # Убираем @ из юзернейма если есть
        if username.startswith('@'):
            username = username[1:]

        moderator = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        time_display = get_display_time(time_str)

        # 🔥 ИСПРАВЛЕННАЯ СИСТЕМА: Получаем ID пользователя по юзернейму
        target_user_id = get_user_id_by_username(message.chat.id, username)

        if not target_user_id:
            reply_with_auto_delete(message, f'❌ Не удалось найти пользователя @{username} в этом чате. Убедитесь, что пользователь является участником чата.')
            return

        target_username_full = f"@{username}"

        # 🔥 ВАЖНО: Проверяем, является ли целевой пользователь администратором
        try:
            target_chat_member = bot.get_chat_member(message.chat.id, target_user_id)
            if target_chat_member.status in ['administrator', 'creator']:
                reply_with_auto_delete(message, f'❌ Не могу замутить {target_username_full} - пользователь является администратором чата!')
                return
        except Exception as admin_check_error:
            logger.error(f"Ошибка при проверке прав пользователя: {admin_check_error}")
            reply_with_auto_delete(message, f'❌ Ошибка при проверке прав пользователя: {str(admin_check_error)}')
            return

        # 🔥 НАСТОЯЩИЙ МУТ ЧЕРЕЗ TELEGRAM API
        try:
            until_date = int(time.time()) + mute_seconds

            # Ограничиваем права пользователя
            bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=target_user_id,
                until_date=until_date,
                permissions=types.ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False
                )
            )

            # Сохраняем в список замученных
            muted_users[target_user_id] = until_date

            # Формируем сообщение об УСПЕШНОМ муте
            mute_message = f"""🔇 *ПОЛЬЗОВАТЕЛЬ ЗАМУЧЕН*

👤 *Наказанный:* {target_username_full}
🛡 *Модератор:* {moderator}
⏰ *Время:* {time_display}
📝 *Причина:* {reason}

✅ *Пользователь замучен на {time_display}!*"""

            log_command(message.from_user.id, message.from_user.username, '!mute @username', f"@{username}", "успешно")
            reply_with_auto_delete(message, mute_message, parse_mode='Markdown')

        except Exception as api_error:
            logger.error(f"Ошибка API в !mute @username: {api_error} | Модератор: {message.from_user.username} (ID: {message.from_user.id})")
            reply_with_auto_delete(message, f'❌ Ошибка при муте через Telegram API: {str(api_error)}')

    except Exception as e:
        logger.error(f"Ошибка в !mute @username: {e} | Пользователь: {message.from_user.username} (ID: {message.from_user.id})")
        reply_with_auto_delete(message, f'❌ Ошибка при выполнении команды: {str(e)}')

# 🔥 СТАРАЯ КОМАНДА MUTE ЧЕРЕЗ ОТВЕТ НА СООБЩЕНИЕ (сохранена)
@bot.message_handler(func=lambda message: message.text.startswith('!mute') and message.reply_to_message)
def mute_reply_command(message):
    try:
        # Проверяем, что команда в группе
        if message.chat.type not in ['group', 'supergroup']:
            reply_with_auto_delete(message, '❌ Эта команда работает только в группах!')
            return

        # Проверяем права пользователя
        user_id = message.from_user.id
        if not is_moderator(user_id):
            log_command(message.from_user.id, message.from_user.username, '!mute reply', result='отказ в доступе')
            reply_with_auto_delete(message, '❌ У вас нет прав для использования этой команды!')
            return

        # Проверяем, что бот является администратором
        chat_member = bot.get_chat_member(message.chat.id, bot.get_me().id)
        if not chat_member.status == 'administrator':
            reply_with_auto_delete(message, '❌ Бот должен быть администратором для мута пользователей!')
            return

        parts = message.text.split()
        if len(parts) < 3:
            reply_with_auto_delete(message, '❌ Формат: `!mute время причина` (в ответ на сообщение пользователя)\n\n*Пример:*\n`!mute 5m спам`')
            return

        time_str = parts[1]
        reason = ' '.join(parts[2:])

        # Проверяем формат времени
        mute_seconds = get_time_from_string(time_str)
        if mute_seconds is None:
            reply_with_auto_delete(message, '❌ Неправильный формат времени!\n*Примеры:*\n`30s` - 30 секунд\n`5m` - 5 минут\n`1h` - 1 час\n`2d` - 2 дня\n`1w` - 1 неделя')
            return

        # Получаем информацию о пользователе и модераторе
        target_user_id = message.reply_to_message.from_user.id
        target_username = f"@{message.reply_to_message.from_user.username}" if message.reply_to_message.from_user.username else message.reply_to_message.from_user.first_name
        moderator = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        time_display = get_display_time(time_str)

        # 🔥 ВАЖНО: Проверяем, является ли целевой пользователь администратором
        try:
            target_chat_member = bot.get_chat_member(message.chat.id, target_user_id)
            if target_chat_member.status in ['administrator', 'creator']:
                reply_with_auto_delete(message, f'❌ Не могу замутить {target_username} - пользователь является администратором чата!')
                return
        except Exception as admin_check_error:
            reply_with_auto_delete(message, f'❌ Ошибка при проверке прав пользователя: {str(admin_check_error)}')
            return

        # 🔥 НАСТОЯЩИЙ МУТ ЧЕРЕЗ TELEGRAM API
        try:
            # ВАЖНО: Используем Unix timestamp для временного мута
            until_date = int(time.time()) + mute_seconds

            # Ограничиваем права пользователя
            bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=target_user_id,
                until_date=until_date,
                permissions=types.ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False
                )
            )

            # Сохраняем в список замученных
            muted_users[target_user_id] = until_date

            # Формируем сообщение об УСПЕШНОМ муте
            mute_message = f"""🔇 *ПОЛЬЗОВАТЕЛЬ ЗАМУЧЕН*

👤 *Наказанный:* {target_username}
🛡 *Модератор:* {moderator}
⏰ *Время:* {time_display}
📝 *Причина:* {reason}

✅ *Пользователь замучен на {time_display}!*"""

            log_command(message.from_user.id, message.from_user.username, '!mute reply', target_username, "успешно")
            reply_with_auto_delete(message, mute_message, parse_mode='Markdown')

        except Exception as api_error:
            logger.error(f"Ошибка API в !mute reply: {api_error} | Модератор: {message.from_user.username} (ID: {message.from_user.id})")
            reply_with_auto_delete(message, f'❌ Ошибка при муте через Telegram API: {str(api_error)}')

    except Exception as e:
        logger.error(f"Ошибка в !mute reply: {e} | Пользователь: {message.from_user.username} (ID: {message.from_user.id})")
        reply_with_auto_delete(message, f'❌ Ошибка при выполнении команды: {str(e)}')

# 🔥 НАСТОЯЩАЯ КОМАНДА UNMUTE ЧЕРЕЗ ОТВЕТ НА СООБЩЕНИЕ
@bot.message_handler(func=lambda message: message.text.startswith('!unmute') and message.reply_to_message)
def unmute_reply_command(message):
    try:
        # Проверяем, что команда в группе
        if message.chat.type not in ['group', 'supergroup']:
            reply_with_auto_delete(message, '❌ Эта команда работает только в группах!')
            return

        # Проверяем права пользователя
        user_id = message.from_user.id
        if not is_moderator(user_id):
            log_command(message.from_user.id, message.from_user.username, '!unmute', result='отказ в доступе')
            reply_with_auto_delete(message, '❌ У вас нет прав для использования этой команды!')
            return

        # Получаем информацию о пользователе и модераторе
        target_user_id = message.reply_to_message.from_user.id
        target_username = f"@{message.reply_to_message.from_user.username}" if message.reply_to_message.from_user.username else message.reply_to_message.from_user.first_name
        moderator = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

        # 🔥 НАСТОЯЩИЙ РАЗМУТ ЧЕРЕЗ TELEGRAM API
        try:
            # Восстанавливаем все права пользователя (устанавливаем until_date на текущее время + 1 секунда)
            bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=target_user_id,
                until_date=int(time.time()) + 1,
                permissions=types.ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False
                )
            )

            # Удаляем из списка замученных
            if target_user_id in muted_users:
                del muted_users[target_user_id]

            # Формируем сообщение об УСПЕШНОМ размуте
            unmute_message = f"""🔊 *ПОЛЬЗОВАТЕЛЬ РАЗМУЧЕН*

👤 *Пользователь:* {target_username}
🛡 *Модератор:* {moderator}

✅ *Пользователь размучен!*"""

            log_command(message.from_user.id, message.from_user.username, '!unmute', target_username, "успешно")
            reply_with_auto_delete(message, unmute_message, parse_mode='Markdown')

        except Exception as api_error:
            logger.error(f"Ошибка API в !unmute: {api_error} | Модератор: {message.from_user.username} (ID: {message.from_user.id})")
            reply_with_auto_delete(message, f'❌ Ошибка при размуте через Telegram API: {str(api_error)}')

    except Exception as e:
        logger.error(f"Ошибка в !unmute: {e} | Пользователь: {message.from_user.username} (ID: {message.from_user.id})")
        reply_with_auto_delete(message, f'❌ Ошибка при выполнении команды: {str(e)}')

# КОМАНДА ДЛЯ ДОБАВЛЕНИЯ МОДЕРАТОРОВ (только для создателя)
@bot.message_handler(func=lambda message: message.text.startswith('!addmod'))
def add_moderator(message):
    try:
        user_id = message.from_user.id

        # Проверяем, что это создатель
        if not is_creator(user_id):
            log_command(message.from_user.id, message.from_user.username, '!addmod', result='отказ в доступе')
            reply_with_auto_delete(message, '❌ Эта команда только для создателя!')
            return

        parts = message.text.split()
        if len(parts) != 2:
            reply_with_auto_delete(message, '❌ Используй: `!addmod ID_пользователя`')
            return

        new_mod_id = int(parts[1])

        # Добавляем ID в список модераторов
        if new_mod_id not in MODERATOR_IDS:
            MODERATOR_IDS.append(new_mod_id)
            log_command(message.from_user.id, message.from_user.username, '!addmod', f"ID: {new_mod_id}", "успешно")
            reply_with_auto_delete(message, f'✅ Пользователь {new_mod_id} добавлен в модераторы!')
        else:
            log_command(message.from_user.id, message.from_user.username, '!addmod', f"ID: {new_mod_id}", "уже модератор")
            reply_with_auto_delete(message, f'❌ Этот пользователь уже является модератором!')

    except ValueError:
        log_command(message.from_user.id, message.from_user.username, '!addmod', result='ошибка формата ID')
        reply_with_auto_delete(message, '❌ Неправильный формат ID!')
    except Exception as e:
        logger.error(f"Ошибка в !addmod: {e} | Создатель: {message.from_user.username} (ID: {message.from_user.id})")
        reply_with_auto_delete(message, f'❌ Ошибка: {str(e)}')

# КОМАНДА ДЛЯ УДАЛЕНИЯ МОДЕРАТОРОВ (только для создателя)
@bot.message_handler(func=lambda message: message.text.startswith('!delmod'))
def delete_moderator(message):
    try:
        user_id = message.from_user.id

        # Проверяем, что это создатель
        if not is_creator(user_id):
            log_command(message.from_user.id, message.from_user.username, '!delmod', result='отказ в доступе')
            reply_with_auto_delete(message, '❌ Эта команда только для создателя!')
            return

        parts = message.text.split()
        if len(parts) != 2:
            reply_with_auto_delete(message, '❌ Используй: `!delmod ID_пользователя`')
            return

        del_mod_id = int(parts[1])

        # Удаляем ID из списка модераторов
        if del_mod_id in MODERATOR_IDS and del_mod_id != CREATOR_ID:
            MODERATOR_IDS.remove(del_mod_id)
            log_command(message.from_user.id, message.from_user.username, '!delmod', f"ID: {del_mod_id}", "успешно")
            reply_with_auto_delete(message, f'✅ Пользователь {del_mod_id} удален из модераторов!')
        elif del_mod_id == CREATOR_ID:
            log_command(message.from_user.id, message.from_user.username, '!delmod', f"ID: {del_mod_id}", "попытка удалить создателя")
            reply_with_auto_delete(message, '❌ Нельзя удалить создателя!')
        else:
            log_command(message.from_user.id, message.from_user.username, '!delmod', f"ID: {del_mod_id}", "не модератор")
            reply_with_auto_delete(message, f'❌ Этот пользователь не является модератором!')

    except ValueError:
        log_command(message.from_user.id, message.from_user.username, '!delmod', result='ошибка формата ID')
        reply_with_auto_delete(message, '❌ Неправильный формат ID!')
    except Exception as e:
        logger.error(f"Ошибка в !delmod: {e} | Создатель: {message.from_user.username} (ID: {message.from_user.id})")
        reply_with_auto_delete(message, f'❌ Ошибка: {str(e)}')

# КОМАНДА ДЛЯ ПРОСМОТРА МОДЕРАТОРОВ (только для создателя)
@bot.message_handler(func=lambda message: message.text.startswith('!modlist'))
def moderator_list(message):
    try:
        user_id = message.from_user.id

        # Проверяем, что это создатель
        if not is_creator(user_id):
            log_command(message.from_user.id, message.from_user.username, '!modlist', result='отказ в доступе')
            reply_with_auto_delete(message, '❌ Эта команда только для создателя!')
            return

        mod_list = "\n".join([f"• {mod_id}" for mod_id in MODERATOR_IDS])
        log_command(message.from_user.id, message.from_user.username, '!modlist')
        reply_with_auto_delete(message, f'📋 *Список модераторов:*\n{mod_list}\n\n*Создатель:* {CREATOR_ID}', parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Ошибка в !modlist: {e} | Создатель: {message.from_user.username} (ID: {message.from_user.id})")
        reply_with_auto_delete(message, f'❌ Ошибка: {str(e)}')

# ОБЩИЕ КОМАНДЫ
@bot.message_handler(func=lambda message: message.text.lower() == 'a:help')
def help_cmd(message):
    log_command(message.from_user.id, message.from_user.username, 'a:help')
    send_message_with_auto_delete(message.chat.id, '''🎮 *СПРАВКА ПО КОМАНДАМ* 🎮

Здесь вы можете узнать все доступные команды и их использование!

╔═══════════════════════╗
║              🎯КОМАНДЫ БОТА              ║
╚═══════════════════════╝
• 🔫 `a:kill [юзернейм]` — устранить пользователя
• 🆕 `a:new` — список последних обновлений
• 🤗 `a:hug [юзернейм]` — обнять пользователя
• 💋 `a:kiss [юзернейм]` — поцеловать пользователя
• 😻 `a:myr [юзернейм]` — помурчать на пользователя
• 👋 `a:slap [юзернейм]` — шлепнуть пользователя

╔═══════════════════════╗
║           ⚡МОДЕРСКИЕ КОМАНДЫ           ║
╚═══════════════════════╝
• 🔇 `!mute @юзернейм время причина` — замутить по юзернейму
• 🔇 `!mute время причина` — замутить (ответом на сообщение)
• 🔊 `!unmute` — размутить (ответом на сообщение)
• 📋 `a:staffcmd` — список модерских команд

*Время:*
s - секунда | m - минута | h - час
d - день   | w - неделя

*Примеры:*
`!mute @username 5m спам`
Ответь на сообщение и напиши `!mute 5m спам`

╔═══════════════════════╗
║                  👨‍💻 СОЗДАТЕЛЬ                   ║
╚═══════════════════════╝

🔥 @treplebeska''', parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'a:new')
def new_cmd(message):
    log_command(message.from_user.id, message.from_user.username, 'a:new')
    send_message_with_auto_delete(message.chat.id, 
    '''🏴‍☠️ НОВИНКА!!!

🗓 Последнее обновление 02.10.2025

🦾 Добавлены команды:

a:kill
a:hug
a:kiss
a:slap
a:myr
!mute (через ответ и по юзернейму)
!unmute (через ответ)
a:staffcmd

🎬 Глобальные обновления:

• Добавлена система логирования
• Добавлен мут по юзернейму
• Теперь вместо `akame:` можно писать `a:`
• Добавлен НАСТОЯЩИЙ мут через ответ на сообщения!''')

# Логирование всех сообщений (опционально)
@bot.message_handler(func=lambda message: True)
def log_all_messages(message):
    """Логирует все сообщения для отладки"""
    logger.debug(f"Сообщение: {message.text} | Пользователь: {message.from_user.username} (ID: {message.from_user.id}) | Чат: {message.chat.id}")

logger.info("=" * 50)
logger.info("Бот Акаме запущен!")
logger.info(f"Создатель: {CREATOR_ID}")
logger.info(f"Модераторы: {MODERATOR_IDS}")
logger.info(f"Всего команд: 12")
logger.info("Доступные команды:")
logger.info("РП команды: a:kill, a:hug, a:kiss, a:myr, a:slap")
logger.info("Общие команды: a:help, a:new, /start")
logger.info("Модерские команды: !mute (@юзернейм/ответ), !unmute, a:staffcmd")
logger.info("Команды создателя: !addmod, !delmod, !modlist")
logger.info("=" * 50)

print("Бот запущен!")
print(f"Создатель: {CREATOR_ID}")
print(f"Модераторы: {MODERATOR_IDS}")
print("Логи сохраняются в файл: bot.log")
print("Автоудаление сообщений включено (15 секунд для всех команд кроме РП)")
bot.polling(none_stop=True)

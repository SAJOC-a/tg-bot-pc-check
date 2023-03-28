import os
import time
import threading
import telebot
import psutil

TOKEN = "" # Токен TG бота (@BotFather)
OWNER_ID = 1532847216 # ID админа, необходим для доступа к боту
ALERT_THRESHOLD = 85 # Аварийный процент загрузки, при котором автоматический высылается предупреждение
ALERT_INTERVAL = 60 # Секунды задержки между авто. проверкой состояния

bot = telebot.TeleBot(TOKEN)

def is_owner(message):
    return message.from_user.id == OWNER_ID

@bot.message_handler(commands=['start'], func=is_owner)
def start(message):
    bot.reply_to(message, "Привет! Я бот, который отслеживает состояние вашего ПК.")

@bot.message_handler(commands=['status'], func=is_owner)
def get_status(message):
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    mem_percent = memory.percent
    bot.reply_to(message, f"CPU: {cpu_percent}%\nОперативная память: {mem_percent}%")

def monitor_status():
    while True:
        memory = psutil.virtual_memory()
        mem_percent = memory.percent
        cpu_percent = psutil.cpu_percent()

        if cpu_percent > ALERT_THRESHOLD or mem_percent > ALERT_THRESHOLD:
            bot.send_message(chat_id=OWNER_ID, text=f"⚠️ Внимание! Высокая нагрузка:\nCPU: {cpu_percent}%\nОперативная память: {mem_percent}%")

        time.sleep(ALERT_INTERVAL)

if __name__ == '__main__':
    monitor_thread = threading.Thread(target=monitor_status)
    monitor_thread.start()
    bot.polling(none_stop=True)

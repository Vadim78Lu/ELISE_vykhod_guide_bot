import os
import telebot
import openai
import yaml

# Загрузка YAML-файла с приветствием
with open("elise_приветствие.yaml", "r", encoding="utf-8") as f:
    welcome_data = yaml.safe_load(f)

WELCOME_TEXT = welcome_data["текст"]

# Настройки API
TELEGRAM_TOKEN = os.environ.get("Telegram_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OpenAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# Обработка входящих сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if text in ["старт", "/start", "начать", "привет", "hello"]:
        bot.reply_to(message, WELCOME_TEXT)
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response['choices'][0]['message']['content']
        bot.reply_to(message, reply)

bot.polling()

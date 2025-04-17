import os
import telebot
import openai

TELEGRAM_TOKEN = os.environ.get("Telegram_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OpenAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.text}]
    )
    reply = response['choices'][0]['message']['content']
    bot.reply_to(message, reply)

bot.polling()

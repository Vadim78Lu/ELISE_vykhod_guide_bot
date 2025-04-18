import os
import telebot
import openai
import yaml

# Загрузка YAML по коду шага
def load_step_yaml(step_code):
    with open(f"{step_code}.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Загрузка приветствия ELISE из отдельного YAML
with open("elise_приветствие.yaml", "r", encoding="utf-8") as f:
    welcome_data = yaml.safe_load(f)
WELCOME_TEXT = welcome_data["текст"]

# Память клиента — временно в словаре
client_step = {}

# Настройки API
TELEGRAM_TOKEN = os.environ.get("Telegram_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OpenAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text.strip().lower()

    # Старт — полное приветствие и установка первого шага
    if text in ["старт", "/start", "начать", "привет", "hello"]:
        client_step[user_id] = "01_вступление"
        bot.reply_to(message, WELCOME_TEXT)
        return

    # Команда "задание" — достаём упражнение из YAML по текущему шагу
    if text == "задание":
        step = client_step.get(user_id, "01_вступление")
        try:
            data = load_step_yaml(step)
            exercise = data.get("задание", {}).get("упражнение", "Упражнение пока не задано.")
            bot.reply_to(message, f"📝 Твоё задание:\n{exercise}")
        except FileNotFoundError:
            bot.reply_to(message, "Файл с заданием пока не найден.")
        return

    # Команда "дальше" — переход на следующий шаг
    if text == "дальше":
        current = client_step.get(user_id, "01_вступление")
        next_step = "02_осознание" if current == "01_вступление" else "03_правила_ошибки"
        client_step[user_id] = next_step

        try:
            data = load_step_yaml(next_step)
            кратко = data.get("цель", "Следующий шаг.")
            bot.reply_to(message, f"🧭 Новый шаг: {next_step}\n{кратко}")
        except FileNotFoundError:
            bot.reply_to(message, "Файл следующего шага не найден.")
        return

    # Все остальные сообщения — GPT отвечает
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.text}]
    )
    reply = response['choices'][0]['message']['content']
    bot.reply_to(message, reply)

bot.polling()

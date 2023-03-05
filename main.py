import openai
import telebot 


BOT_TOKEN='Твой токен бота'
OPENAI_TOKEN = "тоен openai"


# Устанавливаем ключ API для OpenAI
openai.api_key = OPENAI_TOKEN

# Определяем функцию для запроса ответа от OpenAI
def get_response(prompt: str, context: str) -> str:
    """
    Функция для запроса ответа от OpenAI.

    Args:
        prompt (str): Текст от пользователя для передачи в модель.
        context (str): Текущий контекст для передачи в модель.

    Returns:
        str: Ответ от модели.

    """
    # Запрос ответа от OpenAI
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Продолжи общение: {context}Пользователь: {prompt}\n",
        temperature=0,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.2,
        presence_penalty=0.0,
        stop=None
    )
    # Возврат ответа
    return response.choices[0].text.lstrip()

# Определяем функцию для получения текущего контекста из файла
def get_context(file_name) -> str:
    """
    Функция для получения текущего контекста из файла.

    Returns:
        str: Текущий контекст.
    """
    # Чтение текущего контекста из файла
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

# Определяем функцию для сохранения контекста в файл
def save_context(file_name, context: str) -> None:
    """
    Функция для сохранения контекста в файл.

    Args:
        context (str): Контекст для сохранения.
    """
    # Запись контекста в файл
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(context)

# Определяем функцию для сброса контекста
def reset_context(file_name):
    """
    Функция для сброса текущего контекста.

    Args:
        file_name (str): Имя файла с текущим контекстом.
    """
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(" ")

# Создание объекта бота Telegram
bot = telebot.TeleBot(BOT_TOKEN)

# Определяем обработчик команды "reset" для сброса контекста
@bot.message_handler(commands=['reset'])
def get_weather(message):
    reset_context(f"{message.chat.id}.txt")
    bot.send_message(message.chat.id, "Контекст очищен")


# Определяем обработчик сообщений от пользователя
@bot.message_handler(content_types=['text'])
def echo(message) -> None:
    """
    Функция-обработчик для ответа на сообщения от пользователей.

    Args:
        message (telebot.types.Message): Сообщение от пользователя.
    """
    # Сохранение сообщения пользователя в контексте
    save_context(f"{message.chat.id}.txt", f"Пользователь: {message.text}\n")
    # Получение ответа от модели OpenAI на основе контекста и сообщения пользователя
    ans = get_response(message.text, get_context(f"{message.chat.id}.txt"))
    # Отправка ответа пользователю
    bot.send_message(message.chat.id, text=ans)
    # Сохранение ответа в контексте
    save_context(f"{message.chat.id}.txt", f"{ans}\n")


if __name__ == '__main__':
    # Запуск бота в режиме ожидания новых сообщений
    bot.polling(none_stop=True)
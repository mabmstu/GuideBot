from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(token='495453959:AAH26CmZCbrHcGv0N60y4sw6cTE_OpUtsGI') # Токен API к Telegram
dispatcher = updater.dispatcher

# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
def textMessage(bot, update):
    response = 'Получил Ваше сообщение: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)
    
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# Начинаем поиск обновлений
updater.start_polling(poll_interval = 0, timeout = 360,bootstrap_retries = 5,clean=True)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle(stop_signals=(SIGINT))

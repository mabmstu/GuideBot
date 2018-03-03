from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests, bs4

updater = Updater(token='495453959:AAH26CmZCbrHcGv0N60y4sw6cTE_OpUtsGI') # Токен API к Telegram
dispatcher = updater.dispatcher

# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
def textMessage(bot, update):
    response = 'Устал получать ваши сообщения: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)
def pogodka(bot,update):
    s=requests.get('https://sinoptik.com.ru/погода-москва')
    b=bs4.BeautifulSoup(s.text, "html.parser")
    p3=b.select('.temperature .p3')
    pogoda1=p3[0].getText()
    p4=b.select('.temperature .p4')
    pogoda2=p4[0].getText()
    p5=b.select('.temperature .p5')
    pogoda3=p5[0].getText()
    p6=b.select('.temperature .p6')
    pogoda4=p6[0].getText()
    response = 'Утром :' + pogoda1 + ' ' + pogoda2 + ',' + 'Днём :' + pogoda3 + ' ' + pogoda4
    bot.send_message(chat_id=update.message.chat_id, text=response)
    #p=b.select('.rSide .description')
    #pogoda=p[0].getText()
    #print(pogoda.strip())
    
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
#text_message_handler = MessageHandler(Filters.text, textMessage)
pogoda_message_handler = MessageHandler(Filters.text, pogodka)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
#dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(pogoda_message_handler)

# Начинаем поиск обновлений
updater.start_polling()

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()

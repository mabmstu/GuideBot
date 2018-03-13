import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import sqlite3


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Да", callback_data='1'),
                 InlineKeyboardButton("Нет", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Здравствуйте! Сейчас вы находитесь в Уфе. Хотите ознакомиться с достопримечательностями этого города?', reply_markup=reply_markup)
    

def button1(bot, update):
    query = update.callback_query
    if query.data == "2":
         bot.edit_message_text(text="До свидания! Хорошего настроения!",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    if query.data == "1":
        bot.edit_message_text(text="Отлично!",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
class Ufa:        
    updater = Updater('495453959:AAH26CmZCbrHcGv0N60y4sw6cTE_OpUtsGI')
    
    def __init__(updater):
        updater.dispatcher.add_handler(CommandHandler('Ufa', Ufa1))
        updater.dispatcher.add_handler(CallbackQueryHandler(button2))
    
    def db_connection():
        conn = sqlite3.connect("Cities.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ufa")
        return cursor
        
    def Ufa1(bot, update):
        print(update)
        cursor = db_connection() 
        data = cursor.fetchall()
        keyboard = []
        for i in range(52):
            keyboard.append([InlineKeyboardButton(data[i][1], callback_data=str(i))])
        #keyboard.append([InlineKeyboardButton("Далее..", callback_data= str(10))]) 
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Что Вам наиболее интересно?', reply_markup=reply_markup)
        
        
    def button2(bot, update):
        cursor = db_connection()
        data = cursor.fetchall()
        query = update.callback_query
        #print(bot.getUpdates())
        for i in range(52):
            if query.data == str(i):
                 bot.edit_message_text(text="Адрес:"+ data[i][2]+"\n"+data[i][3],
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id)


    
def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

    
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('495453959:AAH26CmZCbrHcGv0N60y4sw6cTE_OpUtsGI')
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button1))
    Ufa
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()

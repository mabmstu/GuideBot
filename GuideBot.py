import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import sqlite3
import telegram


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class Bott:
   
    def __init__(self,token):
        self.updater = Updater(token = token)
        self.i = 0
        self.begin = 0
        self.end = 10
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.btn_handler))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))
        self.updater.dispatcher.add_error_handler(self.error)
        
        

    def start_handler(self):
        self.updater.start_polling()
        self.updater.idle()
        
    def start(self, bot ,update):
        self.bot = bot
        self.update = update
        self.begin = 0
        self.end = 10
        self.update.message.reply_text("Hello!")
        self.keyboard = [[InlineKeyboardButton("Да", callback_data='Да'),
                     InlineKeyboardButton("Нет", callback_data='Нет')]]
        self.reply_markup = InlineKeyboardMarkup(self.keyboard)
        update.message.reply_text('Здравствуйте! Сейчас вы находитесь в Уфе.'
        'Хотите ознакомиться с достопримечательностями этого города?', reply_markup = self.reply_markup)
            

    def help(self,bot,update):
        self.update = update
        self.bot = bot
        print(type(update.message))
        self.update.message.reply_text("Use /start to test this bot.")

    def error(self, bot, update, error):
        logger.warning('Update "%s" caused error "%s"', update, error)
        
    def db_connection(self):
        conn = sqlite3.connect("Cities.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ufa")
        return cursor      
            
    def Ufa(self,bot,update):
        print('Ufa')
        
        
    def updateKeyboard(self, begin, end):
        self.keyboard = []
        if(self.begin < self.end):
            for i in range(self.begin, self.end):
                self.keyboard.append([InlineKeyboardButton(self.data[i][1], callback_data = str(i))])
            self.keyboard.append([InlineKeyboardButton("Далее", callback_data = 'more')])
        else:
            self.keyboard.append([InlineKeyboardButton("Заново", callback_data = 'Заново')])
            self.keyboard.append([InlineKeyboardButton("Нет", callback_data = 'Нет')])

        
    def btn_handler(self,bot,update):      
        query = update.callback_query       
        if query.data == "Нет":
        	self.bot.edit_message_text(text="До свидания! Хорошего настроения!",
                              chat_id = query.message.chat_id,
                              message_id = query.message.message_id)
        elif query.data == "Да":
            bot.edit_message_text(text="Отлично!",
                              chat_id = query.message.chat_id,
                              message_id = query.message.message_id)
            self.cursor = self.db_connection()
            self.data = self.cursor.fetchall()
            self.updateKeyboard(self.begin,self.end)
            reply_markup = InlineKeyboardMarkup(self.keyboard)  
            self.update.message.reply_text('Что Вам наиболее интересно?)',
                                  reply_markup = reply_markup)
           for i in range(self.begin, self.end):
                if self.query.data == str(i):
                    bot.edit_message_text(text=self.data[i][1]+"\n"+"Адрес:"+ self.data[i][2]+"\n"+self.data[i][3],
                                    chat_id = query.message.chat_id,
                                    message_id = query.message.message_id)
 

        elif query.data == 'more':
            self.begin += 10
            self.end += 10
            if self.end > len(self.data):
                self.end = len(self.data)
            self.updateKeyboard(self.begin,self.end)
            reply_markup = InlineKeyboardMarkup(self.keyboard)
            self.bot.edit_message_text(text="...",
                             chat_id = query.message.chat_id,
                              message_id = query.message.message_id)
            if(self.begin < self.end):
                self.update.message.reply_text('Что Вам наиболее интересно?)',
                                  reply_markup = reply_markup)
            else:
                self.update.message.reply_text('Достопримечательности кончились. Показать заново?',
                                  reply_markup = reply_markup)
        elif query.data == 'Заново':
            self.begin = 0
            self.end = 10
            self.bot.edit_message_text(text="...",
                             chat_id = query.message.chat_id,
                              message_id = query.message.message_id)
            self.updateKeyboard(self.begin,self.end)
            reply_markup = InlineKeyboardMarkup(self.keyboard)
            if(self.begin < self.end):
                self.update.message.reply_text('Что Вам наиболее интересно? Для продолжения нажмите на кнопку "Далее" и введите что-нибудь(стикер, текст..)',
                                  reply_markup = reply_markup)
        #else:


    
def main():
    # Create the Updater and pass it your bot's token.
    bott = Bott('495453959:AAH26CmZCbrHcGv0N60y4sw6cTE_OpUtsGI')
    bott.start_handler()
   
if __name__ == '__main__':
    main()

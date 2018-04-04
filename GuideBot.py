import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
import sqlite3
import telegram
      

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

Users_Data = {}
Users_Begins = {}
Users_Ends = {}
Marshrs = {}

Cities = ['Екатеринбург', 'Нижний Новгород', 'Краснодар', 'Красноярск',
          'Новосибирск', 'Санкт-Петербург',  'Самара', 'Сочи',  'Уфа']

class Bott:
   
    def __init__(self,token):
        self.updater = Updater(token = token)
        self.i = 0
        self.begin = 0
        self.end = 10
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.btn_handler))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.all, self.msg_handler))
        self.updater.dispatcher.add_error_handler(self.error)
        

    def start_handler(self):
        self.updater.start_polling()
        self.updater.idle()
        
    def start(self, bot ,update):
        self.bot = bot
        self.update = update
        self.marshr = 0
        self.begin = 0
        self.end = 10
        self.update.message.reply_text("Hello!")

        self.keyboard = []
        for city in Cities:
            self.keyboard.append([InlineKeyboardButton(city, callback_data=city)])
            
        self.keyboard.append([InlineKeyboardButton("Не хочу", callback_data='Нет')])
       
        self.reply_markup = InlineKeyboardMarkup(self.keyboard)
        update.message.reply_text( 'Здравствуйте! Выберите город, чтоб ознакомиться с достопримечательностями'
                        , reply_markup = self.reply_markup)
           

    def help(self,bot,update):
        self.update = update
        self.bot = bot
        print(type(update.message))
        self.update.message.reply_text("Use /start to test this bot.")

    def error(self, bot, update, error):
        logger.warning('Update "%s" caused error "%s"', update, error)
        
    def db_connection(self, city):
        conn = sqlite3.connect("Overall.db") 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sight WHERE city = '{}'".format(city))
        return cursor      
            
        
    def updateKeyboard(self, begin, end):
        self.keyboard = []
        if(self.begin < self.end):
            for i in range(self.begin, self.end):
                self.keyboard.append([InlineKeyboardButton(self.data[i][0], callback_data = str(i))])
            self.keyboard.append([InlineKeyboardButton("Далее", callback_data = 'more')])
            if self.begin > 0:
                self.keyboard.append([InlineKeyboardButton("Назад", callback_data = 'назад')])
        else:
            self.keyboard.append([InlineKeyboardButton("Заново", callback_data = 'Заново')])
            self.keyboard.append([InlineKeyboardButton("Нет", callback_data = 'Нет')])



    def msg_handler(self, bot, update):
        message = update.message

        
    def btn_handler(self,bot,update):      
        query = update.callback_query
        id = query.message.chat_id
        m_id = query.message.message_id
        if query.data == "Нет":
            bot.edit_message_text(text="До свидания! Хорошего настроения!",
                              chat_id = id,
                              message_id = m_id)
        elif query.data in Cities:
            bot.delete_message(chat_id = id, message_id = m_id)
            self.cursor = self.db_connection(query.data)
            
            Users_Data[id] = self.cursor.fetchall()
            Users_Begins[id] = 0
            Users_Ends[id] = 10
            print("\nNew user " + str(id) + " pressed: " + query.data)
            
            self.data = Users_Data.get(id)
            self.begin = Users_Begins.get(id)
            self.end = Users_Ends.get(id)
            
            self.updateKeyboard(self.begin,self.end)
            reply_markup = InlineKeyboardMarkup(self.keyboard)  
            bot.send_message(chat_id = id, message_id = m_id, text ='Что Вам наиболее интересно?',
                                  reply_markup = reply_markup, parse_mode = 'Markdown')
        elif query.data == 'more':
            self.data = Users_Data.get(id)
            self.begin = Users_Begins.get(id)
            self.end = Users_Ends.get(id)
            
            self.begin += 10
            self.end += 10
            if self.end > len(self.data):
                self.end = len(self.data)

            Users_Begins[id] = self.begin
            Users_Ends[id] = self.end
                
            bot.delete_message(chat_id = id, message_id = m_id)
            self.updateKeyboard(self.begin,self.end)
            reply_markup = InlineKeyboardMarkup(self.keyboard)
            if(self.begin < self.end):
                bot.send_message(chat_id = id, message_id = m_id, text ='Что Вам наиболее интересно?',
                                  reply_markup = reply_markup , parse_mode = 'Markdown')
            else:
                bot.send_message(chat_id = id, message_id = m_id, text ='Достопримечательности закончились. Показать заново?',
                                  reply_markup = reply_markup, parse_mode = 'Markdown')
        elif query.data == 'назад':
            self.data = Users_Data.get(id)
            self.begin = Users_Begins.get(id)
            self.end = Users_Ends.get(id)
            
            if self.end == len(self.data):
                self.end -= len(self.data) % 10
                self.begin -= 10
            else:
                self.begin -= 10
                self.end -= 10

            Users_Begins[id] = self.begin
            Users_Ends[id] = self.end
                
            bot.delete_message(chat_id = id, message_id = m_id)
            self.updateKeyboard(self.begin,self.end)
            reply_markup = InlineKeyboardMarkup(self.keyboard)
            if(self.begin < self.end):
                bot.send_message(chat_id = id, message_id = m_id, text ='Что Вам наиболее интересно?',
                                  reply_markup = reply_markup , parse_mode = 'Markdown')
        elif query.data == 'Заново':
            self.data = Users_Data.get(id)
            self.begin = Users_Begins.get(id)
            self.end = Users_Ends.get(id)
            
            self.begin = 0
            self.end = 10

            Users_Begins[id] = self.begin
            Users_Ends[id] = self.end
            
            bot.delete_message(chat_id = id, message_id = m_id)
            self.updateKeyboard(self.begin,self.end)
            reply_markup = InlineKeyboardMarkup(self.keyboard)
            if(self.begin < self.end):
                bot.send_message(chat_id = id, message_id = m_id, text ='Что Вам наиболее интересно?',
                                  reply_markup = reply_markup, parse_mode = 'Markdown')
        elif query.data == 'back':
            self.data = Users_Data.get(id)
            self.begin = Users_Begins.get(id)
            self.end = Users_Ends.get(id)
            
            bot.delete_message(chat_id = id, message_id = m_id)
            self.updateKeyboard(self.begin,self.end)
            reply_markup = InlineKeyboardMarkup(self.keyboard)  
            bot.send_message(chat_id = id, message_id = m_id, text ='Что Вам наиболее интересно?',
                                  reply_markup = reply_markup, parse_mode = 'Markdown')
        elif query.data == 'delphoto':
            bot.delete_message(chat_id = id, message_id = m_id)
        elif query.data == 'Маршрут':
            self.data = Users_Data.get(id)
            self.begin = Users_Begins.get(id)
            self.end = Users_Ends.get(id)
            self.marshr = Marshrs.get(id)
            long = self.data[self.marshr][6]
            lat = self.data[self.marshr][5]
            bot.send_location(chat_id=id,message_id= m_id,
                                  longitude = long, latitude=lat)        
        else:
            for i in range(self.begin, self.end):
                if query.data == str(i):
                    self.data = Users_Data.get(id)
                    self.begin = Users_Begins.get(id)
                    self.end = Users_Ends.get(id)
                    
                    self.marshr = i
                    Marshrs[id] = i
                    bot.delete_message(chat_id = id, message_id = m_id)
                    keyb = [[InlineKeyboardButton('Закрыть', callback_data = 'delphoto')]]
                    reply_markup = InlineKeyboardMarkup(keyb)
                    bot.send_photo(chat_id = id, photo = self.data[i][7],
                                   reply_markup = reply_markup)
                    
                    self.keyb = [[InlineKeyboardButton('Показать на карте', callback_data = 'Маршрут')],
                                 [InlineKeyboardButton('Назад', callback_data = 'back')]]
                    reply_markup = InlineKeyboardMarkup(self.keyb)
                    bot.send_message(chat_id = id, message_id = m_id,
                                  text =self.data[i][0]+"\n"+"Адрес: "+ self.data[i][1]+"\n"+self.data[i][3]+"\n"
                                     +"Расписание: "+ self.data[i][4],
                                  reply_markup = reply_markup, parse_mode = 'Markdown') 
                    
            
                    
                    
 

    # Create the Updater and pass it your bot's token.
bott = Bott('495453959:AAH26CmZCbrHcGv0N60y4sw6cTE_OpUtsGI')
bott.start_handler()


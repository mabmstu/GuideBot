from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, StringCommandHandler
import requests
import collections
from lxml import html
import requests
from lxml import etree
import random


"""
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
    p=b.select('.rSide .description')
    pogoda=p[0].getText()
    response = 'Утром :' + pogoda1 + ' ' + pogoda2 + '\n' + 'Днём :' + pogoda3 + ' ' + pogoda4 + '\n' + pogoda.strip()
    bot.send_message(chat_id=update.message.chat_id, text=response)
    
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
pogoda_message_handler = CommandHandler('weather', pogodka)
text_message_handler = MessageHandler(Filters.text, textMessage)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(pogoda_message_handler)
dispatcher.add_handler(text_message_handler)

# Начинаем поиск обновлений
updater.start_polling()

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
"""

class Message(object):
    def __init__(self, text, **options):
        self.text = text
        self.options = options


class Markdown(Message):
    def __init__(self, text, **options):
        super(Markup, self).__init__(text, parse_mode="Markdown", **options)


class HTML(Message):
    def __init__(self, text, **options):
        super(HTML, self).__init__(text, parse_mode="HTML", **options)


class DialogBot(object):

    def __init__(self, token, generator):
        self.updater = Updater(token=token)  # заводим апдейтера
        handler = MessageHandler(Filters.text | Filters.command, self.handle_message)
        self.updater.dispatcher.add_handler(handler)  # ставим обработчик всех текстовых сообщений
        self.handlers = collections.defaultdict(generator)  # заводим мапу "id чата -> генератор"

    def start(self):
        self.updater.start_polling()

    def handle_message(self, bot, update):
        print("Received", update.message)
        chat_id = update.message.chat_id
        if update.message.text == "/start":
            # если передана команда /start, начинаем всё с начала -- для
            # этого удаляем состояние текущего чатика, если оно есть
            self.handlers.pop(chat_id, None)
        if chat_id in self.handlers:
            # если диалог уже начат, то надо использовать .send(), чтобы
            # передать в генератор ответ пользователя
            try:
                answer = self.handlers[chat_id].send(update.message)
            except StopIteration:
                # если при этом генератор закончился -- что делать, начинаем общение с начала
                del self.handlers[chat_id]
                # (повторно вызванный, этот метод будет думать, что пользователь с нами впервые)
                return self.handle_message(bot, update)
        else:
            # диалог только начинается. defaultdict запустит новый генератор для этого
            # чатика, а мы должны будем извлечь первое сообщение с помощью .next()
            # (.send() срабатывает только после первого yield)
            answer = next(self.handlers[chat_id])
        # отправляем полученный ответ пользователю
        print("Answer: %r" % answer)
        self._send_answer(bot, chat_id, answer)

    def _send_answer(self, bot, chat_id, answer):
        if isinstance(answer, str):
            answer = Message(answer)
        bot.sendMessage(chat_id=chat_id, text=answer.text, **answer.options)

def dialog():
    answer = yield "Здравствуйте! Как Вас зовут?"
    # убираем ведущие знаки пунктуации, оставляем только 
    # первую компоненту имени, пишем её с заглавной буквы
    name = answer.text.rstrip(".!").split()[0].capitalize()
    answer = yield "Приятно познакомиться, %s.В каком городе Вы сейчас находитесь?" %name
    likes_python = yield from ask_yes_or_no("Хотели бы Вы ознакомиться с достопримечательностями этого города?")
    if likes_python:
        #answer = yield from discuss_good_python(name)
        answer = yield from Ufa(name)
    else:
        answer = yield from discuss_bad_python(name)


def ask_yes_or_no(question):
    answer = yield question
    while not ("да" in answer.text.lower() or "нет" in answer.text.lower()):
        answer = yield HTML("Так <b>да</b> или <b>нет</b>?")
    return "да" in answer.text.lower()


def discuss_good_python(name):
    #answer = yield 
    pages = []
    index_page = requests.get('https://kudago.com/ufa/attractions/')
    tree_index = html.fromstring(index_page.content)

    div = tree_index.xpath('//div[@class="clear-filters-container"]')
    div_res = div[0].attrib['data-obj-count']

    answer = yield "Давайте посмотрим, что у нас тут есть...\n" + "Найдено " + div_res + " досторимечательности"
    return answer

def Ufa(name):
    pages = []
    index_page = requests.get('https://kudago.com/ufa/attractions/')
    tree_index = html.fromstring(index_page.content)

    div = tree_index.xpath('//div[@class="clear-filters-container"]')
    div_res = div[0].attrib['data-obj-count']

    print('Найдено', div_res ,'досторимечательности')
    page_count = int(div_res) // 30 + 1
    pages.append(requests.get('https://kudago.com/ufa/attractions/'))
    pages.append(requests.get('https://kudago.com/ufa/attractions/?page=2'))
    tree = []
    names = []
    adress = []
    brief_description = []

    for i in range(page_count):
        tree.append(html.fromstring(pages[i].content))
        names.append(tree[i].xpath('//a[@class="post-title-link"]//span/text()'))
        adress.append(tree[i].xpath('//span[@class="post-detail-address-link"]//span/text()'))
        brief_description.append(tree[i].xpath('//div[@class="post-description"]/text()'))

    n = 30
    for i in range(page_count):
        if i == 1:
            n = int(div_res)-30
        for j in range(n):
            answer =  "Наименование: " + names[i][j] + '\nАдрес: '+ adress[i][j] +"Краткое описание: " + brief_description[i][j].strip() + "\n"
    return answer
"""
       likes_article = yield from ask_yes_or_no("Ага. А как вам, кстати, статья на Хабре? Понравилась?")
    if likes_article:
        answer = yield "Чудно!"
    else:
        answer = yield "Жалко."
    """


def discuss_bad_python(name):
    likes_article = yield from ask_yes_or_no(
        "Окей. Как насчет интересного факта? Просто скажите да или нет")
    if likes_article:
        city_page = requests.get('https://fishki.net/1588575-15-faktov-ob-ufe-i-ufimcah-kotorye-nuzhno-znat-gostjam.html/')
        tree_city = html.fromstring(city_page.content)
        descriotion = tree_city.xpath('//div[@class="content__text"]//p[@itemprop="description"]/text()')
        #for i in descriotion:
        answer = yield descriotion[10][4:]
    else:
        answer = yield "Жаль, что я ничем не смог помочь. Приятно было пообщаться."
    return answer

#def Ufa():

if __name__ == "__main__":
    dialog_bot = DialogBot('495453959:AAH26CmZCbrHcGv0N60y4sw6cTE_OpUtsGI', dialog)
    dialog_bot.start()

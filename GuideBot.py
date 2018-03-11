from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, StringCommandHandler
import requests
import collections

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
import collections

from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

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
    answer = yield "Здравствуйте! Меня забыли наградить именем, а как зовут вас?"
    # убираем ведущие знаки пунктуации, оставляем только 
    # первую компоненту имени, пишем её с заглавной буквы
    name = answer.text.rstrip(".!").split()[0].capitalize()
    likes_python = yield from ask_yes_or_no("Приятно познакомиться, %s. Вам нравится Питон?" % name)
    if likes_python:
        answer = yield from discuss_good_python(name)
    else:
        answer = yield from discuss_bad_python(name)


def ask_yes_or_no(question):
        """Спросить вопрос и дождаться ответа, содержащего «да» или «нет».

    Возвращает:
        bool
    """
    answer = yield question
    while not ("да" in answer.text.lower() or "нет" in answer.text.lower()):
        answer = yield HTML("Так <b>да</b> или <b>нет</b>?")
    return "да" in answer.text.lower()


def discuss_good_python(name):
    answer = yield "Мы с вами, %s, поразительно похожи! Что вам нравится в нём больше всего?" % name
    likes_article = yield from ask_yes_or_no("Ага. А как вам, кстати, статья на Хабре? Понравилась?")
    if likes_article:
        answer = yield "Чудно!"
    else:
        answer = yield "Жалко."
    return answer


def discuss_bad_python(name):
    answer = yield "Ай-яй-яй. %s, фу таким быть! Что именно вам так не нравится?" % name
    likes_article = yield from ask_yes_or_no(
        "Ваша позиция имеет право на существование. Статья "
        "на Хабре вам, надо полагать, тоже не понравилась?")
    if likes_article:
        answer = yield "Ну и ладно."
    else:
        answer = yield "Что «нет»? «Нет, не понравилась» или «нет, понравилась»?"
        answer = yield "Спокойно, это у меня юмор такой."
    return answer


if __name__ == "__main__":
    dialog_bot = DialogBot('495453959:AAH26CmZCbrHcGv0N60y4sw6cTE_OpUtsGI', dialog)s
    dialog_bot.start()

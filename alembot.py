import logging
import os
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_HTTP_API_TOKEN = '760305111:AAHOFviE_4JYOe6WP1gL1ASX7ObsqdYncaI'

FIRST, SECOND = range(2)

index_file = []

files = []

def start(bot, update):
    index_file.clear()
    keyboard = [[InlineKeyboardButton("Алматы", callback_data='Алматы'),
                 InlineKeyboardButton("Астана", callback_data='Астана')],

                [InlineKeyboardButton("Шымкент", callback_data='Шымкент'), 
                InlineKeyboardButton("Алматинская область", callback_data = 'Алматинская_область')],

                [InlineKeyboardButton("Мангистауская область", callback_data= 'Мангистауская_область'), 
                InlineKeyboardButton("Атырауская область", callback_data = 'Атырауская_область')],

                [InlineKeyboardButton("Акмолинская область", callback_data='Акмолинская_область'), 
                InlineKeyboardButton("Актюбинская область", callback_data = 'Актюбинская_область')],

                [InlineKeyboardButton("Республика Казахстан", callback_data='Республика_Казахстан'), 
                InlineKeyboardButton("Жамбылская область", callback_data = 'Жамбылская_область')],

                [InlineKeyboardButton("Павлодарская область", callback_data='Павлодарская_область'), 
                InlineKeyboardButton("Кызылординская область", callback_data = 'Кызылординская_область')],
                ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=update.message.chat_id, text="Please choose:", reply_markup=reply_markup)
    return FIRST


def button(bot, update):
    query = update.callback_query

    query.edit_message_text(text="Selected option: {}".format(query.data))
    index_file.append(query.data)

def start_location(bot, update):
    query = update.callback_query
    index_file.append(query.data)

    keyboard_location = [[InlineKeyboardButton("Все проблемы", callback_data='все_проблемы'),
                InlineKeyboardButton("Безопасность", callback_data='безопасность')],

                [InlineKeyboardButton("Бизнес", callback_data='бизнес'), 
                InlineKeyboardButton("Образование", callback_data='образование')],

                [InlineKeyboardButton("Экоголия", callback_data='экоголия'), 
                InlineKeyboardButton("ЖКХ", callback_data='ЖКХ')],

                [InlineKeyboardButton("Земельные отношения", callback_data='земельные_отношения'), 
                InlineKeyboardButton("Государственное управление", callback_data='государственное_управление')],

                [InlineKeyboardButton("Инфрастуктура", callback_data='инфрастуктура'), 
                InlineKeyboardButton("Коррупция", callback_data='коррупция')],
                ]

    reply_markup_location = InlineKeyboardMarkup(keyboard_location)

    bot.send_message(chat_id=query.message.chat_id, text="Please choose:", reply_markup=reply_markup_location)
    return SECOND
    return ConversationHandler.END

updater = Updater(TELEGRAM_HTTP_API_TOKEN)

def send_me(bot, update):
    query = update.callback_query
    index_file.append(query.data)

    bot.sendMessage(chat_id=query.message.chat_id, text='Send me your message:')

send_me_handler = CommandHandler('send_me', send_me)
updater.dispatcher.add_handler(send_me_handler)

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def save_message(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Write and I'll save!")
    print(index_file)
    print('aaaa')
    saved_text = update.message.text
    print(update.message.from_user.username)
    filename = "Alem/"+index_file[0]+"/"+index_file[1]+"/file-%s.json" %update.message.from_user.username
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, "a+", encoding='utf8')
    # with open(filename, "a+") as f:
    files.append({
    'message': saved_text,
    'timestamp': str(update.message.date)
   })
    print(files)
    print('aaaa')
    f.write(json.dumps(files, ensure_ascii=False))
    # f.write(saved_text)
    f.write("\n")
    f.close()
    bot.sendMessage(chat_id=update.message.chat_id, text="We got you!")


save_message_handler = MessageHandler(Filters.text, save_message)
updater.dispatcher.add_handler(save_message_handler)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST: [CallbackQueryHandler(start_location)],
        SECOND: [CallbackQueryHandler(send_me)],
    },
    fallbacks=[CommandHandler('start_location', start_location)]
)
updater.dispatcher.add_handler(conv_handler)

updater.start_polling()

updater.idle()

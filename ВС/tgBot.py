import telebot

def init():
    global bot
    global chat_id
    global mes

    token = '6904111754:AAEyyp3bF8DEI7mzwdDRQNOp0ypUsnqZaCU'
    bot = telebot.TeleBot(token)
    chat_id = None
    mes = None

def get_keyboard(name_buttons = [], params = {'type': 'Replay',\
                                              'resize_keyboard': True,\
                                              'one_time_keyboard': False}):
    if len(name_buttons) == 0:
        return
    
    if params['type'] == 'Replay':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=params['resize_keyboard'],\
                                                   one_time_keyboard=params['one_time_keyboard'])
        for row in name_buttons:
            buttons = []
            for name in row:
                buttons.append(telebot.types.KeyboardButton(name))
            markup.row(*buttons)
    else:
        markup = telebot.types.InlineKeyboardMarkup()

        for row in name_buttons:
            buttons = []
            for name in row:
                buttons.append(telebot.types.InlineKeyboardButton(name, callback_data=str(name)))
            markup.row(*buttons)

    return markup
    

def tg_print(text, markup = None):
    global bot
    global chat_id

    bot.send_message(chat_id, str(text), reply_markup=markup)

def tg_callback():
    global bot
    global mes
    mes = None
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        global mes
        if call.data:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            mes = call.data

    while mes == None:
        pass

    return mes

def tg_rules(text, rules):
    global bot
    global chat_id
    global g_rules
    g_rules = rules

    @bot.message_handler(func=lambda message: message.text == text)
    def send_rules(message):
        global g_rules
        tg_print(g_rules)

def tg_input(text, markup = None):
    global bot
    global mes
    mes = None

    tg_print(text, markup)

    @bot.message_handler(content_types=["text"])
    def text(message):
        global mes
        mes = message.text

    while mes == None:
        pass

    return mes

def tg_polling():
    global bot
    bot.polling()

import asyncio
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

def vk_init():
    global bot
    global chat
    global mes

    token = "vk1.a.erwSxT7oodrUdd-BGz9tglbdG2ignuOYjvmnkMqgD52pD929Hth09pUO5n0AG8vbfProU8vvwi4Vvpa_47Eo27KJls0AoSF6m8WClJcOt1yhvk2VUgphj-unfa9m8dJrpKVUZzvNoK0SS4ZV9Ag14sIRq9tC0kgXcmYP8P6L3LfwYmRp1l2rO7aA6AW42gbuDqS9wYZRLIQjKSppHn5WWA"
    bot = Bot(token=token)
    chat = None
    mes = None

def vk_polling():
    global bot

    bot.run_forever()

def get_keyboard(name_buttons = [], params = {'inline': False,\
                                              'one_time': False,\
                                              'color': 'secondary'}):
    if len(name_buttons) == 0:
        return

    params['inline'] = params.get('inline', False)
    if params['inline']:
        params['one_time'] = False
    else:
        params['one_time'] = params.get('one_time', False)

    match params.get('color', 'secondary'):
        case 'primary':
            params['color'] = KeyboardButtonColor.PRIMARY
        case 'negative':
            params['color'] = KeyboardButtonColor.NEGATIVE
        case 'positive':
            params['color'] = KeyboardButtonColor.POSITIVE
        case _:
            params['color'] = KeyboardButtonColor.SECONDARY

    keyboard = Keyboard(inline=params['inline'], one_time=params['one_time'])
    for row in name_buttons:
        keyboard.row()
        for name in row:
            keyboard.add(Text(str(name)), color=params['color'])

    return keyboard.get_json()

async def vk_print(text, keyboard = None):
    global chat

    await chat.answer(str(text), keyboard=keyboard)

async def vk_input(text, keyboard = None):
    global bot
    global mes
    global flag
    mes = None
    flag = asyncio.Event()

    await vk_print(text, keyboard)

    @bot.on.message()
    async def get_mes(message: Message):
        global mes
        global flag
        mes = message.text
        flag.set()

    await flag.wait()

    return mes

def vk_rules(name_button, rules):
    global bot
    global g_rules
    g_rules = rules

    @bot.on.message(text=name_button):
    async def send_rules(message: Message):
        global g_rules
        await vk_print(g_rules)

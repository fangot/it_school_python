import asyncio
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

def init():
    global bot
    global chat
    global mes
    
    token = "vk1.a.PUiC-4StYYoY5JP5TGaChjukg396SdYJUdRHU8hubaFSQ-qGAeV1nrUm9IJlHSDzc__auvSBwA-r_YNZzeUK7P_JdyNy47Nw9G5-M1ktwrW5vAmZTf-CNTnFbxImZ19hFK6AWanBL9e3Ntwear1Ip8N7Rx-DhR63q4f0GrkYywYoFBlzbbl82gb3neKRX6ekztEAW1kV4huGi8285f2YIw"
    bot = Bot(token=token)
    chat = None
    mes = None

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
    global flag
    global mes
    mes = None
    flag = asyncio.Event()

    await vk_print(text, keyboard)

    @bot.on.message()
    async def txt(message: Message):
        global mes
        global flag
        mes = message.text
        flag.set()

    await flag.wait()

    return mes

def vk_rules(text, rules):
    global bot
    global g_rules
    g_rules = rules

    @bot.on.message(text=text)
    async def send_rules(message: Message):
        global g_rules
        await vk_print(g_rules)

def vk_polling():
    global bot
    bot.run_forever()

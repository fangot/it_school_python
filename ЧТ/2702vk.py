import vkBot
from random import sample
from vkbottle.bot import Message

vkBot.init()

async def checkLenghNumber(old = False):
    keyboard = vkBot.get_keyboard([[4, 5, 6, 7], [8, 9, 10]], {'inline': True})
    if not old:
        old = await vkBot.vk_input("Сколько знаков будет у загаданного числа (от 4 до 10): ", keyboard)
    
    result = old
    check = True
    try:
        if int(old) < 4:
            result = await vkBot.vk_input("Слишком мало знаков, выбери от 4 до 10: ", keyboard)
            check = False
        elif int(old) > 10:
            result = await vkBot.vk_input("Слишком много знаков, выбери от 4 до 10: ", keyboard)
            check = False
    except ValueError:
        result = await vkBot.vk_input("Это не число. Выбери число от 4 до 10: ", keyboard)
        check = False

    if not check:
        return await checkLenghNumber(result)
    else:
        return result

async def getAnswer(old = False):
    global lenghNumber
    if not old:
        old = await vkBot.vk_input("Введи свой вариант числа (" + str(lenghNumber) + "): ")
    
    result = old
    check = True
    try:
        int(old)
        if len(old) != lenghNumber:
            result = await vkBot.vk_input("Число должно иметь длинну " + str(lenghNumber) + ". Попробуй еще раз: ")
            check = False
        elif not checkRepeat(old):
            result = await vkBot.vk_input("В числе не должно быть повторов цифр. Попробуй еще раз: ")
            check = False
    except ValueError:
        result = await vkBot.vk_input("Это не число. Введи число (" + str(lenghNumber) + "): ")
        check = False

    if not check:
        return await getAnswer(result)
    else:
        return result

def checkRepeat(num):
    i = 0
    for n in num:
        i += 1
        if num.find(n, i) >= 0:
            return False
    return True

async def bullsAndCows(num):
    global secret
    
    bulls = 0
    cows = 0
    i = 0

    for n in num:
        if n == secret[i]:
            bulls += 1
        elif secret.find(n) >= 0:
            cows += 1
        i += 1
    await vkBot.vk_print("Быков: " + str(bulls) + ", Коров: " + str(cows))

@vkBot.bot.on.message(text=['Начать'])
async def start(message: Message):
    global lenghNumber
    global secret

    vkBot.chat = message

    keyboard = vkBot.get_keyboard([['Правила']])
    await vkBot.vk_print("Добро пожаловать в игру Быки и Коровы!", keyboard)

    rules = '''Правила игры:
1. Бот загадывает число с количеством знаков от 4 до 10;
2. Загаданное число не имеет повторов цифр;
3. У игрока есть ограниченное число попыток, чтобы угадать загаданное число;
4. После каждой попытки бот сообщает количество Быков и Коров в предложенном числе относительно загаданного;
5. Быки - это цифры в числе, которые совпадают по значению и расположению;
6. Коровы - это цифры в числе, которые совпадают по значению, но не совпадают по расположению.
'''
    vkBot.vk_rules("Правила", rules)
    
    while True:
        lenghNumber = int(await checkLenghNumber())
        secret = "".join(sample("0123456789", lenghNumber))
        await vkBot.vk_print("Я загадал число!")

        attempt = 1
        while attempt - 1 < lenghNumber * 2:
            await vkBot.vk_print("Попытка " + str(attempt) + " из " + str(lenghNumber * 2))
            answer = await getAnswer()
            await bullsAndCows(answer)

            if answer == secret:
                await vkBot.vk_print("УРА! Ты угадал число " + str(secret))
                break
            attempt += 1
        else:
            await vkBot.vk_print("Увы, попытки кончились. Повезет в следующий раз")

        keyboard = vkBot.get_keyboard([['Да', 'Нет']], {'inline': True, 'color': 'primary'})
        retry = await vkBot.vk_input("Сыграть еще раз?", keyboard)
        if retry == "Нет":
            keyboard = vkBot.get_keyboard([['Начать', 'Правила']])
            await vkBot.vk_print("До встречи! Нажми \"Начать\" когда захочешь сыграть еще раз!", keyboard)
            break

vkBot.vk_polling()

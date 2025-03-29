#t.me/ITSchool72Python_bot
#6904111754:AAEyyp3bF8DEI7mzwdDRQNOp0ypUsnqZaCU
#https://replit.com/

import vkBot
from random import sample
from vkbottle.bot import Message

vkBot.init()

async def getLenghtNumber():
    keyboard = vkBot.get_keyboard([[3, 4, 5, 6], [7, 8, 9, 10]], {'inline': True, 'one_time': True})
    result = await vkBot.vk_input("Какой длины загадать число? (3 - 10): ", keyboard)

    try:
        if int(result) < 3:
            await vkBot.vk_print("Слишком короткое!")
            return await getLenghtNumber()
        elif int(result) > 10:
            await vkBot.vk_print("Слишком длинное!")
            return await getLenghtNumber()
    except ValueError:
        await vkBot.vk_print("Это не число!")
        return await getLenghtNumber()
        
    return int(result)

def isUniqueNums(num):
    i = 0
    for n in num:
        i += 1
        if num.find(n, i) >= 0:
            return False
    return True

async def getAnswer():
    global lenghtNumber
    result = await vkBot.vk_input("Твой вариант числа (" + str(lenghtNumber) + ")? ")

    try:
        int(result)
        if len(result) != lenghtNumber:
            await vkBot.vk_print("Длинна загаданного числа отличается от этого!")
            return await getAnswer()
        elif not isUniqueNums(result):
            await vkBot.vk_print("Число должно содержать только уникальные цифры!")
            return await getAnswer()
    except ValueError:
        await vkBot.vk_print("Это не число!")
        return await getAnswer()
        
    return result

async def checkBullsAndCows(answer):
    global secret
    bulls = 0
    cows = 0

    i = 0
    for n in answer:
        if n == secret[i]:
            bulls += 1
        elif secret.find(n) >= 0:
            cows += 1
        i += 1

    await vkBot.vk_print("Быков: " + str(bulls) + ", Коров: " + str(cows))

@vkBot.bot.on.message(text=['Начать'])
async def start(message: Message):
    global lenghtNumber
    global secret
    vkBot.chat = message

    keyboard = vkBot.get_keyboard([["Правила игры"]])
    await vkBot.vk_print("Добро пожаловать в игру Быки и Коровы!", keyboard)

    rules = '''Правила игры:
1. Бот загадывает число с количеством знаков от 3 до 10;
2. Загаданное число не имеет повторов цифр;
3. У игрока есть ограниченное число попыток, чтобы угадать загаданное число;
4. После каждой попытки бот сообщает количество Быков и Коров в предложенном числе относительно загаданного;
5. Быки - это цифры в числе, которые совпадают по значению и расположению;
6. Коровы - это цифры в числе, которые совпадают по значению, но не совпадают по расположению.
'''
    vkBot.vk_rules("Правила игры", rules)
    
    while True:
        lenghtNumber = await getLenghtNumber()

        secret = "".join(sample("0123456789", lenghtNumber))

        i = 0
        while i < lenghtNumber * 2:
            i += 1
            await vkBot.vk_print("Попытка " + str(i) + " из " + str(lenghtNumber * 2))
            answer = await getAnswer()
            await checkBullsAndCows(answer)

            if answer == secret:
                await vkBot.vk_print("УРА! Ты угадал число " + str(secret))
                break
        else:
            await vkBot.vk_print("К сожалению все попытки закончились. Повезет в следующий раз!")

        keyboard = vkBot.get_keyboard([['Да', 'Нет']], {'inline': True,\
                                                        'one_time': True,\
                                                        'color': 'primary'})
        repeat = await vkBot.vk_input("Сыграть еще раз?", keyboard)
        if repeat == "Нет":
            keyboard = vkBot.get_keyboard([['Начать', 'Правила игры']])
            await vkBot.vk_print("До встречи! Нажми \"Начать\" когда захочешь сыграть еще раз!", keyboard)
            break

vkBot.vk_polling()

#t.me/ITSchool72Python_bot
#6904111754:AAEyyp3bF8DEI7mzwdDRQNOp0ypUsnqZaCU
#https://replit.com/

import tgBot
from random import sample

tgBot.init()

def getLenghtNumber():
    keyboard = tgBot.get_keyboard([[3, 4, 5, 6, 7, 8, 9, 10]], {'type': 'Inline'})
    tgBot.tg_print("Какой длины загадать число? (3 - 10): ", keyboard)
    result = tgBot.tg_callback()

    try:
        if int(result) < 3:
            tgBot.tg_print("Слишком короткое!")
            return getLenghtNumber()
        elif int(result) > 10:
            tgBot.tg_print("Слишком длинное!")
            return getLenghtNumber()
    except ValueError:
        tgBot.tg_print("Это не число!")
        return getLenghtNumber()
        
    return int(result)

def isUniqueNums(num):
    i = 0
    for n in num:
        i += 1
        if num.find(n, i) >= 0:
            return False
    return True

def getAnswer():
    global lenghtNumber
    result = tgBot.tg_input("Твой вариант числа (" + str(lenghtNumber) + ")? ")

    try:
        int(result)
        if len(result) != lenghtNumber:
            tgBot.tg_print("Длинна загаданного числа отличается от этого!")
            return getAnswer()
        elif not isUniqueNums(result):
            tgBot.tg_print("Число должно содержать только уникальные цифры!")
            return getAnswer()
    except ValueError:
        tgBot.tg_print("Это не число!")
        return getAnswer()
        
    return result

def checkBullsAndCows(answer):
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

    tgBot.tg_print("Быков: " + str(bulls) + ", Коров: " + str(cows))

@tgBot.bot.message_handler(commands=['start'])
@tgBot.bot.message_handler(func=lambda message: message.text == 'Начать игру!')
def start(message):
    global lenghtNumber
    global secret
    tgBot.chat_id = message.chat.id

    keyboard = tgBot.get_keyboard([["Правила игры"]])
    tgBot.tg_print("Добро пожаловать в игру Быки и Коровы!", keyboard)

    rules = '''Правила игры:
1. Бот загадывает число с количеством знаков от 3 до 10;
2. Загаданное число не имеет повторов цифр;
3. У игрока есть ограниченное число попыток, чтобы угадать загаданное число;
4. После каждой попытки бот сообщает количество Быков и Коров в предложенном числе относительно загаданного;
5. Быки - это цифры в числе, которые совпадают по значению и расположению;
6. Коровы - это цифры в числе, которые совпадают по значению, но не совпадают по расположению.
'''
    tgBot.tg_rules("Правила игры", rules)
    
    while True:
        lenghtNumber = getLenghtNumber()

        secret = "".join(sample("0123456789", lenghtNumber))

        i = 0
        while i < lenghtNumber * 2:
            i += 1
            tgBot.tg_print("Попытка " + str(i) + " из " + str(lenghtNumber * 2))
            answer = getAnswer()
            checkBullsAndCows(answer)

            if answer == secret:
                tgBot.tg_print("УРА! Ты угадал число " + str(secret))
                break
        else:
            tgBot.tg_print("К сожалению все попытки закончились. Повезет в следующий раз!")

        keyboard = tgBot.get_keyboard([["Да", "Нет"]], {'type': 'Inline'})
        tgBot.tg_print("Сыграть еще раз?", keyboard)
        repeat = tgBot.tg_callback()
        if repeat == "Нет":
            keyboard = tgBot.get_keyboard([["Начать игру!", "Правила игры"]])
            tgBot.tg_print("До встречи! Нажми \"Начать игру!\" когда захочешь сыграть еще раз!", keyboard)
            break

tgBot.tg_polling()

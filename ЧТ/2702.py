#t.me/ITSchool72Python_bot
#6904111754:AAEyyp3bF8DEI7mzwdDRQNOp0ypUsnqZaCU

from random import sample
import tgBot

tgBot.init()

def checkLenghNumber(old = False):
    keyboard = tgBot.get_keyboard([[4, 5, 6, 7, 8, 9, 10]], {'type': 'Inline'})
    if not old:
        tgBot.tg_print("Сколько знаков будет у загаданного числа (от 4 до 10): ", keyboard)
        old = tgBot.tg_callback()
    
    result = old
    check = True
    try:
        if int(old) < 4:
            tgBot.tg_print("Слишком мало знаков, выбери от 4 до 10: ", keyboard)
            result = tgBot.tg_callback()
            check = False
        elif int(old) > 10:
            tgBot.tg_print("Слишком много знаков, выбери от 4 до 10: ", keyboard)
            result = tgBot.tg_callback()
            check = False
    except ValueError:
        tgBot.tg_print("Это не число. Выбери число от 4 до 10: ", keyboard)
        result = tgBot.tg_callback()
        check = False

    if not check:
        return checkLenghNumber(result)
    else:
        return result

def getAnswer(old = False):
    global lenghNumber
    if not old:
        old = tgBot.tg_input("Введи свой вариант числа (" + str(lenghNumber) + "): ")
    
    result = old
    check = True
    try:
        int(old)
        if len(old) != lenghNumber:
            result = tgBot.tg_input("Число должно иметь длинну " + str(lenghNumber) + ". Попробуй еще раз: ")
            check = False
        elif not checkRepeat(old):
            result = tgBot.tg_input("В числе не должно быть повторов цифр. Попробуй еще раз: ")
            check = False
    except ValueError:
        result = tgBot.tg_input("Это не число. Введи число (" + str(lenghNumber) + "): ")
        check = False

    if not check:
        return getAnswer(result)
    else:
        return result

def checkRepeat(num):
    i = 0
    for n in num:
        i += 1
        if num.find(n, i) >= 0:
            return False
    return True

def bullsAndCows(num):
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
    tgBot.tg_print("Быков: " + str(bulls) + ", Коров: " + str(cows))

@tgBot.bot.message_handler(commands=['start'])
@tgBot.bot.message_handler(func=lambda message: message.text == "Начать игру!")
def start(message):
    tgBot.chat_id = message.chat.id
    global lenghNumber
    global secret

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
        lenghNumber = int(checkLenghNumber())
        secret = "".join(sample("0123456789", lenghNumber))
        tgBot.tg_print("Я загадал число!")

        attempt = 1
        while attempt - 1 < lenghNumber * 2:
            tgBot.tg_print("Попытка " + str(attempt) + " из " + str(lenghNumber * 2))
            answer = getAnswer()
            bullsAndCows(answer)

            if answer == secret:
                tgBot.tg_print("УРА! Ты угадал число " + str(secret))
                break
            attempt += 1
        else:
            tgBot.tg_print("Увы, попытки кончились. Повезет в следующий раз")

        keyboard = tgBot.get_keyboard([["Да", "Нет"]], {'type': 'Inline'})
        tgBot.tg_print("Сыграть еще раз?", keyboard)
        retry = tgBot.tg_callback()
        if retry == "Нет":
            keyboard = tgBot.get_keyboard([["Начать игру!", "Правила игры"]])
            tgBot.tg_print("До встречи! Нажми \"Начать игру!\" когда захочешь сыграть еще раз!", keyboard)
            break

tgBot.tg_polling()

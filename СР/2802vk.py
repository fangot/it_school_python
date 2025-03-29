from random import sample
import tgBot

tgBot.tg_init()

def getNumLenght():
    keyboard = tgBot.get_keyboard([[3, 4, 5, 6, 7, 8, 9, 10]], {'type': 'Inline'})
    tgBot.tg_print("Какой длинны загадывать число (3 - 10)? ", keyboard)
    result = tgBot.tg_callback()

    try:
        if int(result) < 3:
            tgBot.tg_print("Слишком короткое число!")
            return getNumLenght()
        elif int(result) > 10:
            tgBot.tg_print("Слишком длинное число!")
            return getNumLenght()
    except ValueError:
        tgBot.tg_print("Это не число!")
        return getNumLenght()
    return int(result)

def getAnswer():
    global numLenght
    
    result = tgBot.tg_input("Твой вариант числа (" + str(numLenght) + "): ")

    try:
        int(result)
        if len(result) != numLenght:
            tgBot.tg_print("Длинна числа отличается от загаданной!")
            return getAnswer()
        elif not checkRepeat(result):
            tgBot.tg_print("В числе не должно быть повторов!")
            return getAnswer()
    except ValueError:
        tgBot.tg_print("Это не число!")
        return getAnswer()
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

@tgBot.bot.message_handler(commands=["start"])
@tgBot.bot.message_handler(func=lambda message: message.text == "Начать игру!")
def start(message):
    global numLenght
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
        numLenght = getNumLenght()

        secret = "".join(sample("0123456789", numLenght))

        step = 1
        while step <= numLenght * 2:
            tgBot.tg_print("Попытка " + str(step) + " из " + str(numLenght * 2))
            answer = getAnswer()
            bullsAndCows(answer)

            if answer == secret:
                tgBot.tg_print("УРА! Ты угадал число " + str(secret))
                break
            step += 1
        else:
            tgBot.tg_print("К сожалению все попытки закончились. Повезет в следующий раз!")

        keyboard = tgBot.get_keyboard([["Да", "Нет"]], {'type': 'Inline'})
        tgBot.tg_print("Хотите сыграть еще?", keyboard)
        repeat = tgBot.tg_callback()
        if repeat == "Нет":
            keyboard = tgBot.get_keyboard([["Начать игру!", "Правила игры"]])
            tgBot.tg_print("До встречи! Нажми \"Начать игру!\", когда захочешь сыграть еще раз", keyboard)
            break

tgBot.tg_polling()

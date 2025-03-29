from random import sample

def checkLenghNumber(old = False):
    if not old:
        old = input("Сколько знаков будет у загаданного числа (от 4 до 10): ")
    
    result = old
    check = True
    try:
        if int(old) < 4:
            result = input("Слишком мало знаков, выбери от 4 до 10: ")
            check = False
        elif int(old) > 10:
            result = input("Слишком много знаков, выбери от 4 до 10: ")
            check = False
    except ValueError:
        result = input("Это не число. Выбери число от 4 до 10: ")
        check = False

    if not check:
        return checkLenghNumber(result)
    else:
        return int(result)

def checkSuggestedNumber(old = False):
    if not old:
        old = input("Введи вариант числа (" + str(lenghNumber) + "): ")
    result = old
    check = True
    try:
        int(old)
        if len(old) != lenghNumber:
            result = input("Неверное количество знаков. Введи число (" + str(lenghNumber) + "): ")
            check = False
        elif not isUniqueNums(old):
            result = input("В числе должны быть только уникальные цифры. Введи число (" + str(lenghNumber) + "): ")
            check = False
    except ValueError:
        result = input("Это не число. Введи число (" + str(lenghNumber) + "): ")
        check = False

    if not check:
        return checkSuggestedNumber(result)
    else:
        return result

def isUniqueNums(num):
    i = 0
    for n in num:
        i += 1
        if num.find(n, i) >= 0:
            return False
    return True

def bullsAndCows(suggest):
    i = 0
    bulls = 0
    cows = 0
    for n in secret:
        if n == suggest[i]:
            bulls += 1
        elif suggest.find(n) >= 0:
            cows += 1
        i += 1
    print("Быков: " + str(bulls) + ", Коров: " + str(cows) + "\n")

    if bulls == lenghNumber:
        return True
    return False

while True:
    lenghNumber = checkLenghNumber()
    secret = "".join(sample("0123456789", lenghNumber))

    print("Я загадал число (" + str(lenghNumber) + ")\n")

    i = 0
    while i < lenghNumber:
        i += 1
        print("Попытка " + str(i) + " из " + str(lenghNumber))
        suggest = checkSuggestedNumber()
        if bullsAndCows(suggest):
            print("УРА!! Ты угадал число " + secret)
            break
    else:
        print("Увы, попытки закончились. Повезет в следующий раз!")
    retry = input("\nСыграть еще раз? (1 - Да): ")

    if retry != "1":
        break
    print("\n")



    

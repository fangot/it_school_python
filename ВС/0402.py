def divide(a, b):
    try:
        return float(a) / float(b)
    except ZeroDivisionError:
        return "Не дели на ноль!"
    except TypeError:
        return "Делить можно только числа!"

def inputData():
    a = input("Введи делимое: ")
    b = input("Введи делитель: ")
    print(divide(a, b))
    inputData()

inputData()

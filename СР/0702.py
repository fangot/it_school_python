def divide(a, b):
    try:
        return float(a) / float(b)
    except ZeroDivisionError:
        return "Не дели на ноль!"
    except ValueError:
        return "Дели только числа!"

def calculator():
    a = input("Введи делимое: ")
    b = input("Введи делитель: ")
    d = divide(a, b)

    print(d)
    calculator()

calculator()

def input_data():
    a = input("Введи делимое: ")
    b = input("Введи делитель: ")
    res = divide(a, b)

    print(f"Результат: {res}\n\n")
    input_data()

def divide(a, b):
    try:
        a = float(a.replace(",", "."))
        b = float(b.replace(",", "."))
        return a / b
    except ValueError:
        return "Ошибка! Делить можно только числа"
    except ZeroDivisionError:
        return "Ошибка! Делить на ноль нельзя"

input_data()

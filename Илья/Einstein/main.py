import itertools

color = ("Красный", "Зелёный", "Белый", "Жёлтый", "Синий")
drink = ("Кофе", "Чай", "Молоко", "Сок", "Вода")
name = ("Иван", "Сергей", "Анна", "Пётр", "Алиса")
pet = ("Собака", "Кошка", "Рыбки", "Попугай", "Лиса")
hobbi = ("Велоспорт", "Футбол", "Шахматы", "Музыка", "Хоккей")

def isRightCondition(a, b):
    if a is not None and b is not None:
        return a == b
    return True

def isLeftHouse(a, b):
    if a is not None and b is not None:
        return a + 1 == b
    return True

def isCenterHouse(a):
    if a is not None:
        return a == 2
    return True

def isFirstHouse(a):
    if a is not None:
        return a == 0
    return True
    
def isHeighbour(a, b):
    if a is not None and b is not None:
        return abs(a - b) == 1
    return True

def check(c = [], d = [], n = [], p = [], h = []):
    def index(a):
        if a in c:
            return c.index(a)
        if a in d:
            return d.index(a)
        if a in n:
            return n.index(a)
        if a in p:
            return p.index(a)
        if a in h:
            return h.index(a)

    return isRightCondition(index("Иван"), index("Красный")) and\
           isRightCondition(index("Сергей"), index("Собака")) and\
           isRightCondition(index("Зелёный"), index("Кофе")) and\
           isRightCondition(index("Анна"), index("Чай")) and\
           isLeftHouse(index("Белый"), index("Зелёный")) and\
           isRightCondition(index("Велоспорт"), index("Рыбки")) and\
           isRightCondition(index("Жёлтый"), index("Футбол")) and\
           isCenterHouse(index("Молоко")) and\
           isFirstHouse(index("Пётр")) and\
           isHeighbour(index("Шахматы"), index("Кошка")) and\
           isHeighbour(index("Попугай"), index("Футбол")) and\
           isRightCondition(index("Музыка"), index("Сок")) and\
           isRightCondition(index("Алиса"), index("Хоккей")) and\
           isHeighbour(index("Пётр"), index("Синий"))

def main():
    colors = list(itertools.permutations(color))
    drinks = list(itertools.permutations(drink))
    names = list(itertools.permutations(name))
    pets = list(itertools.permutations(pet))
    hobbies = list(itertools.permutations(hobbi))
    i = 0

    for c in colors:
        if not check(c):
            i += 1
            continue
        for d in drinks:
            if not check(c, d):
                i += 1
                continue
            for n in names:
                if not check(c, d, n):
                    i += 1
                    continue
                for p in pets:
                    if not check(c, d, n, p):
                        i += 1
                        continue
                    for h in hobbies:
                        if not check(c, d, n, p, h):
                            i += 1
                            continue
                        print(i + 1)
                        return [c, d, n, p, h]

for row in main():
    print(row)
           

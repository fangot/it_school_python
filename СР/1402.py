import itertools

color = ("Красный", "Зеленый", "Синий", "Желтый", "Белый")
nation = ("Белорус", "Украинец", "Грузин", "Испанец", "Китаец")
garden = ("Малина", "Смородина", "Крыжовник", "Клубника", "Виноград")
pet = ("Собака", "Кошка", "Рыбки", "Попугай", "Хомячок")
chocolate = ("Twix", "Snickers", "Mars", "Bounty", "Kitkat")

def rightCondition(a, b):
    if a != None and b != None:
        return a == b
    return True

def rightHouse(a, b):
    if a != None and b != None:
        return a - b == 1
    return True

def centralHouse(a):
    if a != None:
        return a == 2
    return True

def firstHouse(a):
    if a != None:
        return a == 0
    return True

def neighbour(a, b):
    if a != None and b != None:
        return abs(a - b) == 1
    return True

def check(c = [], n = [], g = [], p = [], h = []):
    def index(string):
        if string in c:
            return c.index(string)
        if string in n:
            return n.index(string)
        if string in g:
            return g.index(string)
        if string in p:
            return p.index(string)
        if string in h:
            return h.index(string)

    return rightCondition(index("Украинец"), index("Красный")) and \
           rightCondition(index("Собака"), index("Белорус")) and \
           rightCondition(index("Зеленый"), index("Малина")) and \
           rightCondition(index("Грузин"), index("Виноград")) and \
           rightHouse(index("Зеленый"), index("Белый")) and \
           rightCondition(index("Twix"), index("Кошка")) and \
           rightCondition(index("Желтый"), index("Snickers")) and \
           centralHouse(index("Крыжовник")) and \
           firstHouse(index("Испанец")) and \
           neighbour(index("Mars"), index("Попугай")) and \
           neighbour(index("Хомячок"), index("Snickers")) and \
           rightCondition(index("Kitkat"), index("Клубника")) and \
           rightCondition(index("Китаец"), index("Bounty")) and \
           neighbour(index("Испанец"), index("Синий"))

def main():
    colorArr = list(itertools.permutations(color))
    nationArr = list(itertools.permutations(nation))
    gardenArr = list(itertools.permutations(garden))
    petArr = list(itertools.permutations(pet))
    chocolateArr = list(itertools.permutations(chocolate))
    i = 0

    for c in colorArr:
        if not check(c):
            i += 1
            continue
        for n in nationArr:
            if not check(c, n):
                i += 1
                continue
            for g in gardenArr:
                if not check(c, n, g):
                    i += 1
                    continue
                for p in petArr:
                    if not check(c, n, g, p):
                        i += 1
                        continue
                    for h in chocolateArr:
                        if not check(c, n, g, p, h):
                            i += 1
                            continue
                        print(i + 1)
                        return [c, n, g, p, h]
    

for row in main():
    print(row)

import itertools

color = ("Белый", "Желтый", "Зеленый", "Синий", "Красный")
nation = ("Украинец", "Испанец", "Грузин", "Китаец", "Белорус")
garden = ("Малина", "Смородина", "Виноград", "Крыжовник", "Клубника")
pet = ("Собака", "Рыбки", "Кошка", "Хомячок", "Попугай")
chocolate = ("Mars", "Snickers", "Twix", "Bounty", "Kitkat")


def isRightCondition(a, b):
    return a == b

def isRightPosition(a, b):
    return a - b == 1

def isCentralHouse(a):
    return a == 2

def isFirstHouse(a):
    return a == 0

def isNeighbour(a, b):
    return abs(a - b) == 1

def check(c = [], n = [], g = [], p = [], h = []):
    result = True
    if h:
        result = result and \
                 isNeighbour(h.index("Mars"), p.index("Попугай")) and \
                 isNeighbour(p.index("Хомячок"), h.index("Snickers")) and \
                 isRightCondition(h.index("Kitkat"), g.index("Клубника")) and \
                 isRightCondition(n.index("Китаец"), h.index("Bounty")) and \
                 isRightCondition(h.index("Twix"), p.index("Кошка")) and \
                 isRightCondition(c.index("Желтый"), h.index("Snickers"))
    if p:
        result = result and \
                 isRightCondition(p.index("Собака"), n.index("Белорус"))
    if g:
        result = result and \
                 isCentralHouse(g.index("Крыжовник")) and \
                 isRightCondition(c.index("Зеленый"), g.index("Малина")) and \
                 isRightCondition(n.index("Грузин"), g.index("Виноград"))
    if n:
        result = result and \
                 isFirstHouse(n.index("Испанец")) and \
                 isNeighbour(n.index("Испанец"), c.index("Синий")) and \
                 isRightCondition(n.index("Украинец"), c.index("Красный"))
    if c:
        result = result and \
                 isRightPosition(c.index("Зеленый"), c.index("Белый"))

    return result

def main():
    colorArr = list(itertools.permutations(color))
    nationArr = list(itertools.permutations(nation))
    gardenArr = list(itertools.permutations(garden))
    petArr = list(itertools.permutations(pet))
    chocolateArr = list(itertools.permutations(chocolate))

    for c in colorArr:
        if not check(c):
            continue
        for n in nationArr:
            if not check(c, n):
                continue
            for g in gardenArr:
                if not check(c, n, g):
                    continue
                for p in petArr:
                    if not check(c, n, g, p):
                        continue
                    for h in chocolateArr:
                        if not check(c, n, g, p, h):
                            continue
                        return [c, n, g, p, h]


for row in main():
    print(row)


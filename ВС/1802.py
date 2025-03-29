import itertools

color = ("Синий", "Желтый", "Белый", "Зеленый", "Красный")
nation = ("Украинец", "Японец", "Норвежец", "Испанец", "Англичанен")
pet = ("Зебра", "Улитки", "Лиса", "Собака", "Лошадь")
drink = ("Вода", "Чай", "Сок", "Кофе", "Молоко")
coin = ("Monero", "Bitcoin", "IOTA", "Etherium", "Stellar")

def isRightHouse(a, b):
    if a != None and b != None:
        return a - b == 1
    return True

def isFirstHouse(a):
    if a != None:
        return a == 0
    return True

def isCentralHouse(a):
    if a != None:
        return a == 2
    return True

def isNeighbour(a, b):
    if a != None and b != None:
        return abs(a - b) == 1
    return True

def isRightCondition(a, b):
    if a != None and b != None:
        return a == b
    return True

def check(c = [], n = [], p = [], d = [], o = []):
    def index(a):
        if a in c:
            return c.index(a)
        if a in n:
            return n.index(a)
        if a in p:
            return p.index(a)
        if a in d:
            return d.index(a)
        if a in o:
            return o.index(a)

    return isRightCondition(index("Англичанен"), index("Красный")) and \
           isRightCondition(index("Испанец"), index("Собака")) and \
           isRightCondition(index("Зеленый"), index("Кофе")) and \
           isRightCondition(index("Украинец"), index("Чай")) and \
           isRightHouse(index("Зеленый"), index("Белый")) and \
           isRightCondition(index("Bitcoin"), index("Улитки")) and \
           isRightCondition(index("Желтый"), index("Etherium")) and \
           isCentralHouse(index("Молоко")) and \
           isFirstHouse(index("Норвежец")) and \
           isNeighbour(index("Stellar"), index("Лиса")) and \
           isNeighbour(index("Лошадь"), index("Etherium")) and \
           isRightCondition(index("IOTA"), index("Сок")) and \
           isRightCondition(index("Японец"), index("Monero")) and \
           isNeighbour(index("Норвежец"), index("Синий"))

def main():
    colorArr = list(itertools.permutations(color))
    nationArr = list(itertools.permutations(nation))
    petArr = list(itertools.permutations(pet))
    drinkArr = list(itertools.permutations(drink))
    coinArr = list(itertools.permutations(coin))
    i = 0

    for c in colorArr:
        if not check(c):
            i += 1
            continue
        for n in nationArr:
            if not check(c, n):
                i += 1
                continue
            for p in petArr:
                if not check(c, n, p):
                    i += 1
                    continue
                for d in drinkArr:
                    if not check(c, n, p, d):
                        i += 1
                        continue
                    for o in coinArr:
                        if not check(c, n, p, d, o):
                            i += 1
                            continue
                        print(i + 1)
                        return [c, n, p, d, o]

for row in main():
    print(row)

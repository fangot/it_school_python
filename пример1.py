import itertools

color = ("Желтый", "Белый", "Синий", "Зеленый", "Красный")
nathion = ("Украинец", "Японец", "Норвежец", "Испанец", "Англичанен")
pet = ("Зебра", "Улитки", "Лиса", "Собака", "Лошадь")
drink = ("Вода", "Чай", "Сок", "Кофе", "Молоко")
coin = ("Bitcoin", "IOTA", "Etherium", "Stellar", "Monero")

def isOnRight(a, b):
    if a != None and b != None:
        return a - b == 1
    return True

def isFirstHouse(a):
    if a != None:
        return a == 0
    return True

def isCetralHouse(a):
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

def check(o = [], d = [], p = [], n = [], c = []):
    def index(a):
        if a in o:
            return o.index(a)
        if a in d:
            return d.index(a)
        if a in p:
            return p.index(a)
        if a in n:
            return n.index(a)
        if a in c:
            return c.index(a)
    
    return isOnRight(index("Зеленый"), index("Белый")) and \
           isRightCondition(index("Англичанен"), index("Красный")) and \
           isNeighbour(index("Норвежец"), index("Синий")) and \
           isRightCondition(index("Зеленый"), index("Кофе")) and \
           isRightCondition(index("Желтый"), index("Etherium"))and \
           isFirstHouse(index("Норвежец")) and \
           isRightCondition(index("Испанец"), index("Собака")) and \
           isRightCondition(index("Японец"), index("Monero")) and \
           isRightCondition(index("Украинец"), index("Чай"))and \
           isRightCondition(index("Bitcoin"), index("Улитки")) and \
           isNeighbour(index("Stellar"), index("Лиса")) and \
           isNeighbour(index("Лошадь"), index("Etherium"))and \
           isRightCondition(index("IOTA"), index("Сок")) and \
           isCetralHouse(index("Молоко"))

def main():
    colorArr = list(itertools.permutations(color))
    nathionArr = list(itertools.permutations(nathion))
    petArr = list(itertools.permutations(pet))
    drinkArr = list(itertools.permutations(drink))
    coinArr = list(itertools.permutations(coin))
    i = 0
    
    for o in coinArr:
        if not check(o):
            i += 1
            continue
        for d in drinkArr:
            if not check(o, d):
                i += 1
                continue
            for p in petArr:
                if not check(o, d, p):
                    i += 1
                    continue
                for n in nathionArr:
                    if not check(o, d, p, n):
                        i += 1
                        continue
                    for c in colorArr:
                        if not check(o, d, p, n, c):
                            i += 1
                            continue
                        print(i)
                        return [c, n, p, d, o]

for row in main():
    print(row)

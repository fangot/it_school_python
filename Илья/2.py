asd = 123

#1. НЕ 4asd, asd4
#2. ТОЛЬКО a-Z,0-9, -, _
#3. С маленькой буквы! НЕ Asd, aSD
#4. Осмысленное название переменных. user_name (имя существительное)
#5. Константы капсом: CONSTANT, USER_NAME

def sum(a, b):
    c = a + b
    return c

c = sum(1, 3)
#4

#1. НЕ 4asd, asd4
#2. ТОЛЬКО a-Z,0-9, -, _
#3. С маленькой буквы! НЕ Asd, aSD
#4. Осмысленное название функции (глагол, причастие/деепричастие)
#is, on, in, get, set


if a > 0:
    print("1")
elif a < 0:
    print("-1")
else:
    print("0")


arr = [1, 2, 3, 4, 5]

for i in arr:
    print(i)

dic = {"a": 1, "b": 2}
for key, val in dic:
    print()

for i in range(5): #0,1,2,3,4
    pass

for i in range(2, 7): #2,3,4,5,6
    pass

for i in range(1, 10, 2): #1,3,5,7,9
    pass


while c > 0:
    print()

while True:
    if c < 0:
        break

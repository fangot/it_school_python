Integer (int) 1 0 2 2132 -23 9223372036854775807
Float (float) 0.1 4357394875.643857634
0.1 + 0.2 = 0.30000000000000004

String (str) "3's'df"
'df"s"d'

'''
sdfsdf
sdf
sdf
sdf
sdf
sdf
sdf
sdf
'''

"\n"
"\t"

Boolean (bool) True / False

and
True  and True  = True
True  and False = False
False and True  = False
False and False = False

or
True  or True  = True
True  or False = True
False or True  = True
False or False = False

not
not True  = False
not False = True

Array:

- list a = [1, "sdfsd", True, 12.3, [123], 1, 1]
a[0] -> 1
a[3] -> 12.3
- tuple a = (1, "sdfsd", True, 213.12)
a[2] -> True
- set a = {1, 2, 3, "sdfs"}
- dict a = {"user": "NAME", "password": "234ds42", "user2": "NAME"}
a["user"] = "NAME"


None


#int, float

a = 1 + 2 #(int + int = int), (float + int = float)
a = 1 - 2 = 1 + (-2)
a = 1 * 2
a = 1 / 2 = 0.5 #= float
a = 1 // 2 = 0 #= int
a = 1 % 2 = 1 #= int
a = 2 ** 2 #float ** (int, float) = float, int ** (int, float) = int
a: int = 1 / 0 = NaN != NaN
a: float = 1 / 0 = inf


#str

a = "A" + "2" = "A2"
a = "A_1" * 4 = "A_1A_1A_1A_1"
a = "Python"
a[0] = "P"
a[-1] = "n"
a[1:3] = "yt"
a[0:6:2] = "Pto"
a[::2] = "Pto"
len(a) = 6 #int
len("") = 0
h = "Hello World"
b = "2losd\nfsdf"
b in h = False #bool

h.upper() = "HELLO WORLD"
h.lower() = "hello world"

s = "     He llo  "
s.strip() = "He llo"

j = h.split(" ") = ["Hello", "World"]
"*".join(j) = "Hello*World"

h.replace("l", "2") = "He22o Wor2d"
h.find("l") = 2


#bool

1 == 2 = False
1 != 2 = True
2 < 2 = False
1 > 2 = False
1 <= 2 = True
1 >= 2 = False

1 < 4 < 3 = False
0 > 1 < 10 = False
len(a) > 1 and a[2] == "fsd"

1 == 1.0 = True
"a" < "b" = True
"abc -> ABC"
"Z" < "я"

#Truly, Fallsy

#Fallsy:
0 -> False
0.0 -> False
"" -> False
None -> False
False -> False
[], (), {} -> False

a is None



#List

a = [1, "a", True, "b"]
a[0] = 1
a[-1] = "b"
b = a[1:3] = ["a", True]
a + b = [1, "a", True, "b", "a", True]
[1] * 3 = [1, 1, 1]

a1 = [0, 21, -1, 3, 11]

"a" in a = True
len(a) = 4
min(a1) = -1
max(a1) = 21

a.append(4)
#a = [1, "a", True, "b", 4]

a.remove(1)
#a = ["a", True, "b", 4]

p = a.pop()
#a = ["a", True, "b"]
#p = 4

a.index("b") = 2
a.count("b") = 1

a.clear()
#a = []

#КОПИРОВАНИЕ МАССИВОВ
b = a.copy()


a1.sort()
#[-1, 0, 3, 11, 21]

a1.reverse()
#[11, 3, -1, 21, 0]



#Tuple

t = (1, 2, 3)
t1, t2, t3 = t
#t1 = 1, t2 = 2, t3 = 3



#Set

a = {1, 2, 3}
b = {4, 5, 2}
d = set()

c = a | b
#{1, 2, 3, 4, 5}
c = a.union(b)

c = a & b
c = a.intersection(b)
#{2}


c = a - b
c = a.difference(b)
#{1, 3}

a.add(9)
#a = {1, 2, 3, 9}

a.remove(1)
#a = {2, 3, 9}

a.discard(11)
#a = {2, 3, 9}


#Dict
d = {}
a = {"a": 1, "b": 2, "c": 3}

a["a"]
#= 1

a.get("q", 0)
#= 0


a["q"] = 11
#{"a": 1, "b": 2, "c": 3, "q": 11}

del a["a"]
#{"b": 2, "c": 3, "q": 11}


"a" in a
#False


keys = a.keys()
#["b", "c", "q"]

vals = a.values()
#[2, 3, 11]

len(a)
#3

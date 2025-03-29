def arr(n):
    result = []
    for i in range(n):
        result.append(i + 1)
    return result

def sum(n):
    result = 0
    for i in range(n):
        result += i + 1
    return result

def loop(n):
    summ = sum(n)

    if (summ % 3 != 0):
        return "NO"
            
    third = int(summ / 3)
            
    if third < n:
        return "NO"
    
    array = arr(n)
    shift = 1
    for k in range(n):
        array = array[-shift:] + array[:-shift]
                
        result1 = 0
        result2 = 0
        for i in array:
            if (result1 < third):
                result1 += i
            elif (result2 < third):
                if result2 == 0:
                    j = i
                result2 += i
            if (result1 > third or result2 > third):
                break
            if (result1 == third and result2 == third):
                break
        if (result1 == third and result2 == third):
            result = [["1/3", third], [array[0], j - 1], [j, i], [i + 1, array[-1]]]
            break
    else:
        return "NO"
            
    return str(result)

n = 3
while n <= 1000:
    res = loop(n)
    if (res != "NO"):
        print("n = " + str(n) + ": " + res)
    n += 1

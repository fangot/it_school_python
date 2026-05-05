for i in range(5):
    if i < 3:
        continue

    print(i)

    if i == 5:
        break
else:
    print("Не было i = 5")

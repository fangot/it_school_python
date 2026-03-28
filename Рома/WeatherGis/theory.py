#Работы с файлами

#with open('test.txt', 'w', encoding = 'utf-8') as f:
#    print('123\n', file = f)
#    print('346\n', file = f)


#Работа с путями

from pathlib import Path

p = Path('ddd/tttt/test2.txt')
#print(p.parent)

if p.exists():
    print("Существует")
else:
    p.write_text('Создали новый файл', encoding='utf-8')

if p.is_dir():
    print("Это папка")
if p.is_file():
    print("Это файл")

Path('werwer/ddd/123').mkdir(parents=True, exist_ok=True)
#Работы с файлами

#with open('test.txt', 'a', encoding = 'utf-8') as f:
#    print('123\n', file = f)
#    print('346\n', file = f)


#Работа с путями

import json
from pathlib import Path

#p = Path('README.md')
#print(p.parent)

#if p.exists():
#    print("Существует")
#else:
#    p.write_text('Создали новый файл', encoding='utf-8')

#if p.is_dir():
#    print("Это папка")
#if p.is_file():
#    print("Это файл")

#Path('werwer/ddd/123').mkdir(parents=True, exist_ok=True)
#content = p.read_text(encoding='utf-8')

#for file in Path('.').rglob('*.py'):
#    print(file)


#ПЕРЕМЕЩЕНИЕ
import shutil

#shutil.copy2('README.md', '1.md')
#shutil.copytree('src', 'copy')

#shutil.move('README.md', 'db/README.md')
#shutil.rmtree('.')


#ПОИСК
import glob
import os

#py = glob.glob('../*.py', recursive=True)
#print(py)

#for root, dirs, files in os.walk('.'):
#    for file in files:
#        if file.endswith('.py'):
#            print(os.path.join(root, file))



#АРХИВЫ ZIP
from zipfile import ZipFile, ZIP_DEFLATED

#with ZipFile('arh.zip', 'w', ZIP_DEFLATED) as zf:
#    zf.write('README.md', 'RENAME.md')

#with ZipFile('arh.zip', 'r') as zf:
#    files = zf.namelist()
#    print(files)

#    content = zf.read('RENAME.md').decode('utf-8')
#    print(content)

#    zf.extractall('.')
#    zf.extract('RENAME.md', '.')


#ЗАПРОСЫ
import requests

#try:
#    response = requests.get('https://google.com', timeout=10)
#    response.raise_for_status()
#    data = response.json()

#except requests.exceptions.Timeout:
#    print("Время ожидания истекло")
#except requests.exceptions.HTTPError as e:
#    print(e)

#requests.exceptions.ConnectionError
#requests.exceptions.RequestException


#БАЗЫ ДАННЫХ
#SQL
import sqlite3

db = sqlite3.connect("example.db")
cur = db.cursor()

#cur.execute("""
#    CREATE TABLE IF NOT EXISTS students (
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        name TEXT NOT NULL,
#        age INTEGER,
#        facultet TEXT
#    )
#""")

#cur.execute(
#    "INSERT INTO students (name, age, facultet) VALUES (?, ?, ?)",
#    ("Роман", 18, "ФизФак")
#)

#students = [
#    ("Иван", 20, "ФилФак"),
#    ("Сергей", 19, "ЖурФак"),
#    ("Анна", 17, "МатФак")
#]
#cur.executemany(
#    "INSERT INTO students (name, age, facultet) VALUES (?, ?, ?)",
#    students
#)

#cur.execute(
#    "SELECT * FROM students"
#)
#rows = cur.fetchall()
#for row in rows:
#    print(row)

#cur.execute("""
#    SELECT name, facultet
#    FROM students
#    WHERE age > 18
#""")
#rows = cur.fetchall()
#for row in rows:
#    print(row)

#cur.execute("""
#    UPDATE students
#    SET age = ?
#    WHERE name = ?
#""",
#(1800, "Анна")
#)
#db.commit()

#cur.execute(
#    "DELETE FROM students WHERE id > ?",
#    (0,)
#)
#db.commit()


#cur.execute(
#    "SELECT * FROM students WHERE facultet LIKE ? ORDER BY name DESC LIMIT 2",
#    ("%Фак",)
#)
#rows = cur.fetchall()
#for row in rows:
#    print(row)


#db.close()
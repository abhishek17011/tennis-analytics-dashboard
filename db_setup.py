
import sqlite3
import random

conn = sqlite3.connect("tennis.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Rankings(
player_id TEXT,
name TEXT,
country TEXT,
gender TEXT,
year INTEGER,
week INTEGER,
rank INTEGER,
points INTEGER,
stage TEXT
)""")

cur.execute("DELETE FROM Rankings")

players = [
("Novak Djokovic","Serbia","Men"),
("Carlos Alcaraz","Spain","Men"),
("Jannik Sinner","Italy","Men"),
("Iga Swiatek","Poland","Women"),
("Aryna Sabalenka","Belarus","Women"),
("Coco Gauff","USA","Women")
]

stages = ["Early", "Mid", "Peak"]

data = []
for year in [2023, 2024]:
    for week in range(1, 11):
        rank = 1
        for p in players:
            data.append((
                p[0][:3]+str(week)+str(year),
                p[0],
                p[1],
                p[2],
                year,
                week,
                rank,
                random.randint(4000,12000),
                random.choice(stages)
            ))
            rank += 1

cur.executemany("INSERT INTO Rankings VALUES (?,?,?,?,?,?,?,?,?)", data)

conn.commit()
conn.close()
print("Advanced database created successfully")

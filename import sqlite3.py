import sqlite3

def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL COLLATE NOCASE,
            has_legs INTEGER DEFAULT 1
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appendages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id INTEGER,
            type TEXT NOT NULL,
            numm INTEGER NOT NULL,
            FOREIGN KEY (animal_id) REFERENCES animals(id)
        )
    ''')

def animaldef(cursor):
    animals_data = [
        ('Собака', 1),
        ('Кошка', 1),
        ('Лошадь', 1),
        ('Птица', 0),
        ('Змея', 0),
        ('Рыба', 0),
        ('Человек', 1)
    ]
    cursor.executemany("INSERT OR IGNORE INTO animals (name, has_legs) VALUES (?, ?)", animals_data)

    kon_data = [
        (1, 'лапы', 4),
        (2, 'лапы', 4),
        (3, 'копыта', 4),
        (4, 'крылья', 2),
        (5, None, 0),
        (6, 'плавники', 0),
        (7, 'ноги', 2)
    ]
    cursor.executemany("INSERT OR IGNORE INTO appendages (animal_id, type, numm) VALUES (?, ?, ?)", kon_data)


def infodef(cursor, animal_name):
    cursor.execute("""
        SELECT
            a.name,
            ap.type,
            ap.numm
        FROM animals a
        LEFT JOIN appendages ap ON a.id = ap.animal_id
        WHERE a.name = ?
    """, (animal_name,))
    return cursor.fetchone()


def main():
    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()

    try:
        create_tables(cursor)
        animaldef(cursor)

        while True:
            animal_name = input("Введите название животного (или 'q' для выхода): ")
            if animal_name.lower() == 'q':
                break
            appendage_info = infodef(cursor, animal_name)
            if appendage_info:
                animal_name, type_an, numscon = appendage_info
                print(f"У {animal_name}:")
                if type_an:
                    print(f"{type_an}: {numscon}")
                else:
                    print("Нет конечностей.")
            else:
                print(f"Животное '{animal_name}' не найдено.")
        conn.commit()
    except:
        print(f"Ошибка работы с базой данных")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
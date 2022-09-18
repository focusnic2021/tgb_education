import sqlite3

def create_db_objects(sql, message):
    try:
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print(message,' - ok')
        return 0
    except Exception as ex:
        print('Error:', ex)
        return -1
    # ...def create_db_objects


def main():
    message = "создание таблицы пользователей"
    sql = """CREATE TABLE users (
                id INTEGER PRIMARY KEY NOT NULL,
                first_name VARCHAR (20),
                last_name  VARCHAR (20),
                real_first_name  VARCHAR (20) DEFAULT '',
                real_second_name VARCHAR (20) DEFAULT '',
                real_last_name   VARCHAR (20) DEFAULT '',
                dt_insert DATETIME NOT NULL,
                dt_update DATETIME NULL
                );"""
    result = create_db_objects(sql, message)

    if result == 0:
        message = "создание в таблице USERS индекса по столбцу first_name(Никнейм)"
        query = """CREATE INDEX idx_first_name ON users (
        first_name ASC
        );"""
        result = create_db_objects(query, message)

    if result == 0:
        message = "создание в таблице USERS индекса по столбцу real_first_name(Полное имя)"
        query = """CREATE INDEX idx_real_name ON users (
        real_first_name,real_second_name,real_last_name  ASC
        );"""
        result = create_db_objects(query, message)

    if result == 0:
        print("Все запросы выполнены успешно")
    # ... def main()


if __name__ == '__main__':
    main()
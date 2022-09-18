import sqlite3


def db_new_user(data):
    """Вставляет запись о новом пользователе - если его нще не знаем. Либо возвращет информацию о уже знакомом пользователе"""
    # попытка вставить запись о новом пользователе:
    # return db_insert_user(data)
    (result_code, result_text) = db_insert_user(data)
    if result_code == 0:
        return (result_code, result_text)
    elif result_code == -2:
        # user_id is exist - select him real_first_name, real_second_name, real_last_name
        return db_exist_user(data[0])
    # ...db_new_user


def db_insert_user(data):
    try:
        connect = sqlite3.connect('students.db')
        cursor = connect.cursor()
        sql = "INSERT INTO users(id, first_name, last_name, dt_insert) " \
              "VALUES(?,?,?,?);"
        print(f"db_insert_user: {sql=}")
        cursor.execute(sql, data)
        connect.commit()
        connect.close()
        return (0, data[1]+' '+data[2])
    except sqlite3.IntegrityError as ie_ex:  # except Exception as ex:
        print('Insert Error:', ie_ex)
        connect.close()
        return (-2, ie_ex)
    except sqlite3.DatabaseError as db_ex:
        print('DatabaseError:', db_ex)
        connect.close()
        return (-4, db_ex)
    # ...db_insert_user

def db_exist_user(user_id):
    connect = sqlite3.connect('students.db')
    cursor = connect.cursor()
    # попытка выборки Существующего_Известного_Пользователя:
    sql = f"SELECT first_name, last_name, real_first_name, real_second_name, real_last_name " \
          f"FROM users WHERE id = {user_id}"
    print(f"db_exist_user: {sql = }")
    cursor.execute(sql)
    exist_user = cursor.fetchone()
    print(f"db_exist_user: {exist_user = }")
    connect.close()
    if len((exist_user[2]).strip()) == 0:
        # нет РЕАЛЬНОГО имени - вернуть ФИКТИВНЫЕ first_name + last_name:
        if len((exist_user[1]).strip()) == 0:
            # нет ФИКТИВНОЙ фамилии:
            if len((exist_user[0]).strip()) == 0:
                # нет ни ФИКТИВНОГО имени, ни ФИКТИВНОЙ фамилии:
                return(-100, f'{user_id=}')
            else:
                # нет ФИКТИВНОГО имени - вернуть хотя бы ФИКТИВНУЮ фамилию:
                return (0, exist_user[0])
        else:
            return (0, exist_user[0]+' '+exist_user[1])
    else:
        # return real_first_name + real_second_name + real_last_name:
        return (0, (exist_user[2]+' '+exist_user[3]+' '+exist_user[4]).strip())
    # ...db_exist_user
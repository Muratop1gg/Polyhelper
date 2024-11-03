import sqlite3
from config import *


db = sqlite3.connect(f"{mainSource}{dbName}", check_same_thread=False)

cur = db.cursor()


cur.execute( # Creating a table in database if not exist
    f"""CREATE TABLE IF NOT EXISTS {db_table_name}(
        {list(db_keys.keys())[0]} {list(db_keys.values())[0]},
        {list(db_keys.keys())[1]} {list(db_keys.values())[1]},
        {list(db_keys.keys())[2]} {list(db_keys.values())[2]},
        {list(db_keys.keys())[3]} {list(db_keys.values())[3]},
        {list(db_keys.keys())[4]} {list(db_keys.values())[4]},
        {list(db_keys.keys())[5]} {list(db_keys.values())[5]},
        {list(db_keys.keys())[6]} {list(db_keys.values())[6]},
        {list(db_keys.keys())[7]} {list(db_keys.values())[7]},
        {list(db_keys.keys())[8]} {list(db_keys.values())[8]},
        {list(db_keys.keys())[9]} {list(db_keys.values())[9]},
        {list(db_keys.keys())[10]} {list(db_keys.values())[10]}
    )"""
)


def db_update_element_by_chat_id(chat_id : int, var_name : str, content: any) -> bool:
    try:
        if content is str:
            cur.execute(f"""UPDATE {db_table_name} SET {var_name} = \"{content}\" WHERE (chatID = {chat_id}) """)
            db.commit()
        elif content is bool:
            if content:
                cur.execute(f"""UPDATE {db_table_name} SET {var_name} = TRUE WHERE (chatID = {chat_id}) """)
                db.commit()
            else:
                cur.execute(f"""UPDATE {db_table_name} SET {var_name} = FALSE WHERE (chatID = {chat_id}) """)
                db.commit()
        else:
            cur.execute(f"""UPDATE {db_table_name} SET {var_name} = {content} WHERE (chatID = {chat_id}) """)
            db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def db_insert_element(element_name : str, element_value : any) -> bool:
    try:
        cur.execute(f"INSERT INTO {db_table_name} ({element_name}) VALUES({element_value})")
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def db_get_element_by_chat_id(chat_id : int, var_name : str) -> any:
    try:
        out = cur.execute(f"SELECT {var_name} FROM {db_table_name} WHERE (chatID = {chat_id})").fetchone()[0]
        return out
    except Exception as e:
        print(e)
        return None


def db_count_by_element(element_name : str, element_value : any) -> int:
    return cur.execute(f"SELECT COUNT(*) FROM {db_table_name} WHERE {element_name} = {element_value}").fetchone()[0]
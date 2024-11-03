import sqlite3
from config import *


db = sqlite3.connect(f"{mainSource}{dbName}", check_same_thread=False)
cur = db.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        id INTEGER PRIMARY KEY,
        chatID INTEGER,
        msgID INTEGER,
        geomsgID INTEGER,
        groupID TEXT,
        schMODE BOOL,
        schDELTA INTEGER,
        groupEDIT BOOL,
        teacherEDIT BOOL,
        teacherNAME TEXT
    )"""
)


def db_update_element_by_chat_id(chat_id : int, var_name : str, content: any) -> bool:
    try:
        if content is str:
            cur.execute(f"""UPDATE users SET {var_name} = \"{content}\" WHERE (chatID = {chat_id}) """)
            db.commit()
        elif content is bool:
            if content:
                cur.execute(f"""UPDATE users SET {var_name} = TRUE WHERE (chatID = {chat_id}) """)
                db.commit()
            else:
                cur.execute(f"""UPDATE users SET {var_name} = FALSE WHERE (chatID = {chat_id}) """)
                db.commit()
        else:
            cur.execute(f"""UPDATE users SET {var_name} = {content} WHERE (chatID = {chat_id}) """)
            db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def db_insert_element(element_name : str, element_value : any) -> bool:
    try:
        cur.execute(f"INSERT INTO users ({element_name}) VALUES({element_value})")
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


def db_get_element_by_chat_id(chat_id : int, var_name : str) -> any:
    try:
        out = cur.execute(f"SELECT {var_name} FROM users WHERE (chatID = {chat_id})").fetchone()[0]
        return out
    except Exception as e:
        print(e)
        return None


def db_count_by_element(element_name : str, element_value : any) -> int:
    return cur.execute(f"SELECT COUNT(*) FROM users WHERE {element_name} = {element_value}").fetchone()[0]
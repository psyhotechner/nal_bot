import sqlite3
from typing import List, Tuple
from config import db_file

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def add_user(self, tg_id_user: int, last_name: str, first_name: str, second_name: str, registr_date: str, specialty: str) -> None:
        self.cursor.execute('''
        INSERT INTO users(tg_id_user, last_name, first_name, second_name, registr_date, specialty)
        VALUES(?, ?, ?, ?, ?, ?)
        ''', (tg_id_user, last_name, first_name, second_name, registr_date, specialty))
        self.conn.commit()

    def get_users(self) -> List[Tuple[int, str, str, str, str, str]]:
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

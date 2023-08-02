import sqlite3


class Database:
    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.con.rollback()
        else:
            self.con.commit()
        self.con.close()

    # def add_item(self, item):
    #     if 'author' in item.__dict__.keys():
    #         query_create_db = "CREATE TABLE IF NOT EXISTS Notes(id INTEGER PRIMARY KEY, Name VARCHAR, Author VARCHAR, Text VARCHAR)"
    #         self.con.execute(query_create_db)
    #         #self.con.commit()
    #         author = item.author
    #         text = item.text
    #         name = item.name
    #         index = self.get_index('Notes')
    #         if index[0][0] is None:
    #             index = 0
    #         else:
    #             index = index[0][0] + 1
    #
    #         query_insert_note = f"INSERT INTO Notes(id, name, author, text) VALUES(?, ?, ?, ?)"
    #         self.con.execute(query_insert_note, (index, name, author, text))
    #         print(query_insert_note)
    #     else:
    #         query_create_db = "CREATE TABLE IF NOT EXISTS Cards(id INTEGER PRIMARY KEY, 'Name', 'Company', 'Address')"
    #         self.con.execute(query_create_db)
    #         name = item.name
    #         company = item.company
    #         address = item.address
    #         index = self.get_index('Cards')
    #         if index[0][0] is None:
    #             index = 0
    #         else:
    #             index = index[0][0] + 1
    #
    #         query_insert_card = f"INSERT INTO Cards(id, name, company, address) VALUES(?, ?, ?, ?)"
    #         self.con.execute(query_insert_card, (index, name, company, address))
    #         print(query_insert_card)

    def get_index(self, table: str) -> list:
        if self.table_exists(table):
            query = f"SELECT MAX(id) FROM {table}"
            results = self.con.execute(query).fetchall()[0][0]
            # print(type(results))
            if results:
                return results
            return 0
        return 0

    # def get_notes(self):
    #     query = f"SELECT name, author, text FROM Notes"
    #     results = self.con.execute(query).fetchall()
    #     return results

    # def get_cards(self):
    #     query = f"SELECT name, company, address FROM Cards"
    #     results = self.con.execute(query).fetchall()
    #     return results

    # def remove_note(self, name: str):
    #     query = f"DELETE FROM Notes WHERE name = '{name}'"
    #     self.con.execute(query)

    # def remove_card(self, name: str):
    #     pass

    def table_exists(self, table_name):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name = '{table_name}'"
        result = self.con.execute(query).fetchall()
        return result

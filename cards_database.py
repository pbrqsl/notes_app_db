from database import Database
import json


class CardsDatabase(Database):
    def __init__(self, path):
        super().__init__(path)
        create_query = "CREATE TABLE IF NOT EXISTS Cards(id INTEGER PRIMARY KEY, Name VARCHAR, Company VARCHAR, Address VARCHAR)"
        self.con.execute(create_query)
        self.con.commit()

    def get_cards(self):
        if self.table_exists("Cards"):
            query = f"SELECT id, Name, Company, Address FROM Cards"
            results = self.con.execute(query).fetchall()
            result_dir = {}
            for result in results:
                result_dir[result[0]] = {
                    "Name": result[1],
                    "Company": result[2],
                    "Address": result[3],
                }
            result_dir = json.dumps(result_dir)
            result_json = json.loads(result_dir)
            return result_json
        return None

    def add_card(self, note):
        index = self.get_index("Cards")
        print(index)
        query = f"INSERT INTO Cards(id, Name, Company, Address) VALUES({index+1}, '{note['Name']}', '{note['Company']}', '{note['Address']}');"
        self.con.execute(query)
        self.con.commit()

    def remove_card(self, name):
        query = f"DELETE FROM Cards WHERE name = '{name}'"
        self.con.execute(query)
        self.con.commit()

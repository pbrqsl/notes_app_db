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
            return self.sql_results_to_json(results)
        return None

    def add_card(self, note):
        index = self.get_index("Cards")
        query = (f"INSERT INTO Cards(id, Name, Company, Address) "
                 f"VALUES({index+1}, '{note['Name']}', '{note['Company']}', '{note['Address']}');")
        self.con.execute(query)
        self.con.commit()

    def remove_card(self, name):
        query = f"DELETE FROM Cards WHERE name = '{name}'"
        self.con.execute(query)
        self.con.commit()

    def update_card(self, card_id, name, company, address):
        query = (
            f"UPDATE Cards SET Name = '{name}', "
            f"  Company = '{company}', "
            f"  Address = '{address}' "
            f"  WHERE id = '{card_id}'"
        )
        self.con.execute(query)
        self.con.commit()

    def get_card_by_name(self, name: str):
        query = f"SELECT id, Name, Company, Address FROM Cards WHERE Name = '{name}'"
        results = self.con.execute(query).fetchall()
        return self.sql_results_to_json(results)

    def get_card_by_id(self, name: str):
        query = f"SELECT id, Name, Company, Address FROM Cards WHERE id = '{name}'"
        results = self.con.execute(query).fetchall()
        return self.sql_results_to_json(results)

    def sql_results_to_json(self, sql_results):
        result_dir = {}
        for result in sql_results:
            result_dir[result[0]] = {
                "Id": result[0],
                "Name": result[1],
                "Company": result[2],
                "Address": result[3],
            }
        result_dir = json.dumps(result_dir)
        result_json = json.loads(result_dir)
        return result_json

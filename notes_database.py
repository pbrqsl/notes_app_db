from database import Database
import json


class NotesDatabase(Database):
    def __init__(self, path):
        super().__init__(path)
        create_query = "CREATE TABLE IF NOT EXISTS Notes(id INTEGER PRIMARY KEY, Name VARCHAR, Author VARCHAR, Text VARCHAR)"
        self.con.execute(create_query)
        self.con.commit()

    def get_notes(self):
        if self.table_exists("Notes"):
            query = f"SELECT id, name, author, text FROM Notes"
            results = self.con.execute(query).fetchall()
            return self.sql_results_to_json(results)
        return None

    def add_note(self, note):
        index = self.get_index("Notes")
        print(index)
        query = f"INSERT INTO Notes(id, Name, Author, Text) VALUES({index+1}, '{note['Name']}', '{note['Author']}', '{note['Text']}');"
        self.con.execute(query)
        self.con.commit()

    def remove_note(self, name):
        query = f"DELETE FROM Notes WHERE name = '{name}'"
        self.con.execute(query)
        self.con.commit()

    def update_note(self, note_id, name, author, text):
        query = (
            f"UPDATE Notes SET Name = '{name}', "
            f"  Author = '{author}', "
            f"  Text = '{text}' "
            f"  WHERE id = '{note_id}'"
        )
        self.con.execute(query)
        self.con.commit()

    def get_note_by_name(self, name: str):
        query = f"SELECT id, Name, Author, Text FROM Notes WHERE Name = '{name}'"
        results = self.con.execute(query).fetchall()
        return self.sql_results_to_json(results)

    def get_note_by_id(self, name: str):
        query = f"SELECT id, Name, Author, Text FROM Notes WHERE id = '{name}'"
        results = self.con.execute(query).fetchall()
        return self.sql_results_to_json(results)

    def sql_results_to_json(self, sql_results):
        result_dir = {}
        for result in sql_results:
            result_dir[result[0]] = {
                "Id": result[0],
                "Name": result[1],
                "Author": result[2],
                "Text": result[3],
            }
        result_dir = json.dumps(result_dir)
        result_json = json.loads(result_dir)
        return result_json


from typing import Callable, List
from notes_database import NotesDatabase
from cards_database import CardsDatabase


class MenuOption:
    def __init__(self, reference: Callable, label: str):
        self.reference = reference
        self.label = label


class Menu:
    def __init__(self, options: List[MenuOption]):
        self.options = options
        self.keep_running = True

    def show(self):
        for key in self.options.keys():
            print(f"{key}. {self.options[key].label}")

    def get_choice(self):
        self.choice_pending = True

        while self.choice_pending:
            try:
                choice = int(input("Enter your choice: "))

                if choice in self.options.keys():
                    self.choice_pending = False
                    return self.options[choice].reference

                print("Wrong choice, please try again!")

            except ValueError:
                print("Something went wrong, please try again.")


class Note:
    def __init__(
        self,
        name: str = "sample_name",
        author: str = "Anonymous",
        text: str = "Some note...",
    ):
        print("Created a note!")

        self.name = name

        self.author = author

        self.text = text

    def show(self):
        print(f"Author: {self.author}, Text: {self.text}")

    def to_json(self):
        note_dir = {"Name": self.name, "Author": self.author, "Text": self.text}
        return note_dir


class Card:
    def __init__(
        self,
        name: str = "John Smith",
        company: str = "Google Inc.",
        address: str = "Palo Alto",
    ):
        print("Created a card!")

        self.name = name
        self.company = company
        self.address = address

    def show(self):
        print(f"Name: {self.name}\nCompany: {self.company}\nAddress: {self.address}")

    def to_json(self):
        card_dir = {"Name": self.name, "Company": self.company, "Address": self.address}
        return card_dir


class NotesSubManager:
    def __init__(self, path):
        self.path = path

    def add_note(self):
        name = input("Enter name: ")

        author = input("Enter author: ")

        text = input("Enter text: ")

        note = Note(author=author, text=text, name=name)

        with NotesDatabase(self.path) as db_notes:
            db_notes.add_note(note.to_json())

    def show_notes(self):
        print("Showing notes: ")

        with NotesDatabase(self.path) as db_notes:
            notes = db_notes.get_notes()
        for note in notes.values():
            print(f"Name: {note['Name']} ")
            print(f"Author: {note['Author']}")
            print(f"Text: {note['Text']}")

        print()

    def remove_note(self):
        name = input("Enter name: ")

        with NotesDatabase(self.path) as db_notes:
            db_notes.remove_note(name)


class CardsSubManager:
    def __init__(self, path):
        self.path = path

    def add_card(self):
        name = input("Enter name: ")

        company = input("Enter company: ")

        address = input("Enter address: ")

        card = Card(name=name, company=company, address=address)

        with CardsDatabase(self.path) as db_cards:
            db_cards.add_card(card.to_json())

    def show_cards(self):
        print("Showing cards:")

        with CardsDatabase(self.path) as db_cards:
            cards = db_cards.get_cards()

        for card in cards.values():
            print(f"Name: {card['Name']} ")
            print(f"Author: {card['Company']}")
            print(f"Text: {card['Address']}")

        print("-------")

    def remove_card(self):
        name = input("Enter name: ")

        with CardsDatabase(self.path) as db_cards:
            db_cards.remove_card(name)


class Manager:
    def __init__(self):
        self.notes_manager = NotesSubManager("app_database.db")
        self.cards_manager = CardsSubManager("app_database.db")
        self.options = {
            1: MenuOption(self.add_note, "Add note"),
            2: MenuOption(self.add_card, "Add card"),
            3: MenuOption(self.show_notes, "Show notes"),
            4: MenuOption(self.show_cards, "Show cards"),
            5: MenuOption(self.remove_note, "Remove note"),
            6: MenuOption(self.remove_card, "Remove card"),
            7: MenuOption(self.exit_manager, "Exit"),
        }
        self.menu: Menu = Menu(self.options)
        self.running = True

    def run(self):
        print("Started Manager!")
        while self.running:
            self.show_menu()
            choice = self.menu.get_choice()
            choice()

    def show_menu(self):
        self.menu.show()

    def show_notes(self):
        self.notes_manager.show_notes()

    def show_cards(self):
        self.cards_manager.show_cards()

    def add_note(self):
        self.notes_manager.add_note()

    def add_card(self):
        self.cards_manager.add_card()

    def remove_note(self):
        self.notes_manager.remove_note()

    def remove_card(self):
        self.cards_manager.remove_card()

    def exit_manager(self):
        self.running = False


def main():
    manager_main = Manager()
    manager_main.run()


if __name__ == "__main__":
    main()

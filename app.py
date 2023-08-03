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
        note_details = self.get_note_details(self)

        note = Note(name=note_details['Name'],
                    author=note_details['Author'],
                    text=note_details['Text']
                    )
        print(note.to_json())

        with NotesDatabase(self.path) as db_notes:
            db_notes.add_note(note.to_json())

    def get_note_details(self):
        name = input("Enter name: ")
        author = input("Enter author: ")
        text = input("Enter text: ")
        note_details_output = {
            'Name': name,
            'Author': author,
            'Text': text,
                               }
        return note_details_output

    def show_notes(self):
        print("Showing notes: ")

        with NotesDatabase(self.path) as db_notes:
            notes = db_notes.get_notes()
        self.display_notes(notes)

    def remove_note(self):
        name = input("Enter name: ")

        with NotesDatabase(self.path) as db_notes:
            db_notes.remove_note(name)

    def update_note(self):
        note_id = input("Enter Note_ID: ")
        print('Current values:')
        with NotesDatabase(self.path) as db_notes:
            notes = db_notes.get_note_by_id(note_id)
        self.display_notes(notes)
        note_details = self.get_note_details()
        print("Enter new values:")

        with NotesDatabase(self.path) as db_notes:
            db_notes.update_note(note_id=note_id,
                                 name=note_details['Name'],
                                 author=note_details['Author'],
                                 text=note_details['Text'])

    def display_notes(self, notes):
        for note in notes.values():
            print(f"Note_ID: {note['Id']} ")
            print(f"Name: {note['Name']} ")
            print(f"Author: {note['Author']}")
            print(f"Text: {note['Text']}")
            print('-------------------------')


class CardsSubManager:
    def __init__(self, path):
        self.path = path

    def add_card(self):
        card_details = self.get_card_details()
        card = Card(name=card_details['Name'],
                    company=card_details['Company'],
                    address=card_details['Address']
                    )
        print(card.to_json())

        with CardsDatabase(self.path) as db_cards:
            db_cards.add_card(card.to_json())

    def get_card_details(self):
        name = input("Enter name: ")
        company = input("Enter company: ")
        address = input("Enter address: ")
        card_details_output = {
            'Name': name,
            'Company': company,
            'Address': address,
                               }
        return card_details_output

    def show_cards(self):
        print("Showing cards:")

        with CardsDatabase(self.path) as db_cards:
            cards = db_cards.get_cards()
        self.display_cards(cards)

    def remove_card(self):
        name = input("Enter name: ")

        with CardsDatabase(self.path) as db_cards:
            db_cards.remove_card(name)

    def update_card(self):
        card_id = input("Enter Card_ID: ")
        print('Current values:')
        with CardsDatabase(self.path) as db_cards:
            cards = db_cards.get_card_by_id(card_id)
        self.display_cards(cards)
        card_details = self.get_card_details()
        print("Enter new values:")

        with CardsDatabase(self.path) as db_cards:
            db_cards.update_card(card_id=card_id,
                                 name=card_details['Name'],
                                 company=card_details['Company'],
                                 address=card_details['Address'])

    def display_cards(self, cards):
        for card in cards.values():
            print(f"Card_ID: {card['Id']} ")
            print(f"Name: {card['Name']} ")
            print(f"Company: {card['Company']}")
            print(f"Address: {card['Address']}")
            print('-------------------------')


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
            7: MenuOption(self.update_note, "Update note"),
            8: MenuOption(self.update_card, "Update card"),
            9: MenuOption(self.exit_manager, "Exit")
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

    def update_note(self):
        self.notes_manager.update_note()

    def update_card(self):
        self.cards_manager.update_card()

    def exit_manager(self):
        self.running = False


def main():
    manager_main = Manager()
    manager_main.run()


if __name__ == "__main__":
    main()

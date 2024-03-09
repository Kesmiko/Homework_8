from Classes import AddressBook, Record
import datetime as strftime
import pickle

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"
        except Exception as e:
            return f"Error: {e}"

    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
    
@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)

    record.add_phone(phone)
    return "Contact added"

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)

    record.add_birthday(birthday)
    return "Birthday added"
        
@input_error
def birthdays(args, book: AddressBook):
    return book.get_upcoming_birthdays()

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return "No such name found"
    record.edit_phone(old_phone, new_phone)
    return "Phone changed"

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)
        
@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "No such name found"
    if record.birthday:
        return str(record.birthday.value.strftime('%d.%m.%Y'))
    else:
        return "Birthday not set"


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return "No such name found"
    return '; '.join(str(phone.value) for phone in record.phones)

@input_error
def show_all(args, book):
    return book

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    commands = ["hello", "add", "change", "phone", "all", "birthdays", "add-birthday", "show-birthday"]
    while True:
        user_input = input(f"Enter a command ({', '.join(commands)}): \n>>> ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))

if __name__ == "__main__":
    main()

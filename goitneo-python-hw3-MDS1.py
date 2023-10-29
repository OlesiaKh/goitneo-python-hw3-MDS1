from datetime import datetime, timedelta

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __eq__(self, other: object) -> bool:
        return self.value == other.value

    def __str__(self):
        return f"Phone: {self.value}"


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format")
        self.value = value


class Record:
    def __init__(self, name: str, phones: list[str] = None, birthday: str = None) -> None:
        if phones is None:
            self.phones = []
        else:
            self.phones = [Phone(p) for p in phones]
        self.name = Name(name)
        self.birthday = None
        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone_number: str) -> None:
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p

    def delete_phone(self, phone: str) -> None:
        phone_to_delete = self.find_phone(phone)
        if phone_to_delete:
            self.phones.remove(phone_to_delete)

    def edit_phone(self, old_phone, new_phone) -> None:
        new_phone = Phone(new_phone)
        phone_to_remove = self.find_phone(old_phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
            self.phones.append(new_phone)

    def __str__(self):
        phones = '; '.join(str(p) for p in self.phones)
        birthday = self.birthday.value if self.birthday else "None"
        return f"Name: {self.name.value}, Phones: {phones}, Birthday: {birthday}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, rec: Record) -> None:
        self.data[rec.name.value] = rec

    def find_record(self, value: str):
        return self.data.get(value)

    def delete_record(self, value: str) -> None:
        self.data.pop(value)

    def get_birthdays_per_week(self):
        now = datetime.today().date()
        end_date = now + timedelta(days=7)
        birthday_week = [rec for rec in self.data.values() if rec.birthday and datetime.strptime(rec.birthday.value, "%d.%m.%Y").date() <= end_date]
        return birthday_week


CONTACTS = AddressBook()


def parse_input(user_input):
    user_input = user_input.split()
    command = user_input[0].lower()
    args = user_input[1:] if len(user_input) > 1 else []
    return command, args


def add_contact(name, phone):
    if name in CONTACTS.data:
        return f"Contact for {name} already exists"
    elif len(phone) != 10:
        return "Please provide a valid 10-digit phone number"
    else:
        CONTACTS.add_record(Record(name, [phone]))
        return f"Contact added: {name}, {phone}"


def change_contact(name, phone):
    contact = CONTACTS.find_record(name)
    if contact:
        contact.edit_phone(contact.phones[0].value, phone)
        return f"Contact updated: {name}, {phone}"
    else:
        return f"No contact found for {name}"


def phone_info(name):
    contact = CONTACTS.find_record(name)
    if contact:
        return f"Phone for {name}: {contact.phones[0]}"
    else:
        return f"No contact found for {name}"


def show_all():
    if not CONTACTS.data:
        return "No contacts found"
    else:
        result = "All contacts:\n"
        for contact in CONTACTS.data.values():
            result += str(contact) + "\n"
        return result


def add_birthday(name, birthday):
    contact = CONTACTS.find_record(name)
    if contact:
        try:
            contact.add_birthday(birthday)
            return f"Birthday added for {name}: {birthday}"
        except ValueError:
            return "Please provide a birthday in format DD.MM.YYYY"
    else:
        return f"No contact found for {name}"


def show_birthday(name):
    contact = CONTACTS.find_record(name)
    if contact:
        if contact.birthday:
            return f"Birthday for {name}: {contact.birthday.value}"
        else:
            return f"No birthday found for {name}"
    else:
        return f"No contact found for {name}"


def birthdays_upcoming():
    upcoming_bdays = CONTACTS.get_birthdays_per_week()
    if upcoming_bdays:
        result = "Upcoming birthdays:\n"
        for contact in upcoming_bdays:
            result += f"{contact.name.value}: {contact.birthday.value}\n"
        return result
    else:
        return "No upcoming birthdays in the next week"


def main():
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            result = add_contact(*args)
            print(result)

        elif command == "change":
            result = change_contact(*args)
            print(result)

        elif command == "phone":
            result = phone_info(*args)
            print(result)

        elif command == "all":
            result = show_all()
            print(result)

        elif command == "add-birthday":
            result = add_birthday(*args)
            print(result)

        elif command == "show-birthday":
            result = show_birthday(*args)
            print(result)

        elif command == "birthdays":
            result = birthdays_upcoming()
            print(result)

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()

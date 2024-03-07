from collections import UserDict
import datetime as dt
from datetime import datetime as dtdt

class Field:
    def __init__(self, value):
        self.value = value
        
    def is_valid(self, value):
        return True
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError
        else:
            self.__value = value
    
    def __str__(self) -> str:
        return str(self.value)
    
class Birthday(Field):
    
    def is_valid(self, value):
        try:
            dtdt.strptime(value, '%d.%m.%Y')
        except ValueError:
            return False
        return True    
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError
        else:
            self.__value = dtdt.strptime(value, '%d.%m.%Y')

class Name(Field):
    def is_valid(self, value):
        return bool(value)

class Phone(Field):
    def is_valid(self, value):
        return value.isdigit() and len(value) == 10

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, phone, new_phone):
        if phone in [p.value for p in self.phones]: 
                self.remove_phone(phone)
                self.add_phone(new_phone)
        else:
            raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(phone) for phone in self.phones)}, birthday: {str(self.birthday)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today_date = dtdt.today().date()
        birthdays = [] 
        for record in self.data.values(): 
            if record.birthday is not None:
                birthday_date = record.birthday.value
                birthday_date = dt.date(today_date.year, birthday_date.month, birthday_date.day)
                week_day = birthday_date.isoweekday() 
                days_between = (birthday_date - today_date).days 
                if 0 <= days_between < 7: 
                    if week_day < 6: 
                        birthdays.append({'name': record.name.value, 'congratulation_date': birthday_date.strftime("%Y.%m.%d")}) 
                    else:
                        if (birthday_date + dt.timedelta(days=1)).weekday() == 0:
                            birthdays.append({'name': record.name.value, 'congratulation_date': (birthday_date + dt.timedelta(days=1)).strftime("%Y.%m.%d")})
                        elif (birthday_date + dt.timedelta(days=2)).weekday() == 0: 
                            birthdays.append({'name': record.name.value, 'congratulation_date': (birthday_date + dt.timedelta(days=2)).strftime("%Y.%m.%d")})
        return birthdays

    def __str__(self) -> str:
        return "\n".join(str(record) for record in self.data.values())


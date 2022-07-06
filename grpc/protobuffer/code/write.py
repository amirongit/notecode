import sys

import specification_pb2


def prompt_for_address(person):
    person.id = int(input('Enter person ID number: '))
    person.name = input('Enter name: ')

    person.email = input('Enter email address: ')

    while True:
        number = input('Enter a phone number (blank to finish): ')
        if number == '':
            break

        phone_number = person.phones.add()
        phone_number.number = number
        type_ = input('What kind of phone is this?! ')
        if type_ == 'mobile':
            phone_number.type = specification_pb2.Person.PhoneType.MOBILE
        if type_ == 'home':
            phone_number.type = specification_pb2.Person.PhoneType.HOME
        if type_ == 'work':
            phone_number.type = specification_pb2.Person.PhoneType.WORK
        else:
            print('Unknown type, setting the default value!')


if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} ADDRESS_BOOK_FILE')
    sys.exit(-1)

address_book = specification_pb2.AddressBook()

try:
    f = open(sys.argv[1], 'rb')
    address_book.ParseFromString(f.read())
    f.close()
except IOError:
    print(f'Could not open {sys.argv[1]}. Creating a new one.')
prompt_for_address(address_book.people.add())
f = open(sys.argv[1], 'wb')
f.write(address_book.SerializeToString())
f.close()

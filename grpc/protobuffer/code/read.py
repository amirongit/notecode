import sys

import specification_pb2


def list_people(address_book):
    for person in address_book.people:
        print(str(person))


if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]}, ADDRESS_BOOK_FILE')
    sys.exit(-1)


address_book = specification_pb2.AddressBook()

f = open(sys.argv[1], 'rb')
address_book.ParseFromString(f.read())
f.close()

list_people(address_book)

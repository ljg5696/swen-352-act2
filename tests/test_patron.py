import unittest
from library.patron import Patron, InvalidNameException

class TestPatron(unittest.TestCase):

    def test_create_patron(self):
        patron = Patron("John", "Doe", 25, "123")
        self.assertEqual(patron.get_fname(), "John")

    def test_create_patron_invalid_first_name(self):
        try:
            Patron("John2", "Doe", 25, "123")
            error = False
        except InvalidNameException:
            error = True
        self.assertEqual(error, True)

    def test_create_patron_invalid_last_name(self):
        try:
            Patron("John", "Doe3", 25, "123")
            error = False
        except InvalidNameException:
            error = True
        self.assertEqual(error, True)

    def test_add_borrowed_book(self):
        patron = Patron("Jane", "Doe", 30, "456")
        patron.add_borrowed_book("Dune")
        self.assertEqual(patron.get_borrowed_books(), ["dune"])

    def test_add_borrowed_book_no_duplicates(self):
        patron = Patron("Jane", "Doe", 30, "456")
        patron.add_borrowed_book("Dune")
        patron.add_borrowed_book("Dune")
        self.assertEqual(patron.get_borrowed_books(), ["dune"])

    def test_return_borrowed_book(self):
        patron = Patron("Jane", "Doe", 30, "456")
        patron.add_borrowed_book("Dune")
        patron.return_borrowed_book("Dune")
        self.assertEqual(patron.get_borrowed_books(), [])

    def test_return_borrowed_book_not_on_list(self):
        patron = Patron("Jane", "Doe", 30, "456")
        patron.add_borrowed_book("Dune")
        patron.return_borrowed_book("1984")
        self.assertEqual(patron.get_borrowed_books(), ["dune"])

    def test_equal(self):
        patron1 = Patron("Alice", "Smith", 20, "789")
        patron2 = Patron("Alice", "Smith", 20, "789")
        self.assertEqual(patron1 == patron2, True)

    def test_equal_false(self):
        patron1 = Patron("Alice", "Smith", 20, "789")
        patron2 = Patron("Bob", "Smith", 20, "789")
        self.assertEqual(patron1 == patron2, False)

    def test_get_first_name(self):
        patron = Patron("Tom", "Hanks", 40, "999")
        self.assertEqual(patron.get_fname(), "Tom")

    def test_get_last_name(self):
        patron = Patron("Tom", "Hanks", 40, "999")
        self.assertEqual(patron.get_lname(), "Hanks")

    def test_get_age(self):
        patron = Patron("Tom", "Hanks", 40, "999")
        self.assertEqual(patron.get_age(), 40)

    def test_get_memberID(self):
        patron = Patron("Tom", "Hanks", 40, "999")
        self.assertEqual(patron.get_memberID(), "999")

if __name__ == "__main__":
    unittest.main()
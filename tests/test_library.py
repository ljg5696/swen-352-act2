import unittest
from unittest.mock import Mock
from library.library import Library

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.ext_api = Mock()
        self.db_interface = Mock()

        self.library = Library()
        self.library.api = self.ext_api
        self.library.db = self.db_interface


    def test_is_ebook_true(self):
        self.ext_api.get_ebooks = Mock(return_value=[{"title": "Dune", "ebook_count": 1}])
        self.assertEqual(self.library.is_ebook("Dune"), True)

    def test_is_ebook_false(self):
        self.ext_api.get_ebooks = Mock(return_value=[{"title": "Other Book", "ebook_count": 1}])
        self.assertEqual(self.library.is_ebook("Dune"), False)

    def test_get_ebooks_count(self):
        self.ext_api.get_ebooks = Mock(return_value=[
            {"title": "Dune", "ebook_count": 2},
            {"title": "Dune", "ebook_count": 3}
        ])
        self.assertEqual(self.library.get_ebooks_count("Dune"), 5)

    def test_is_book_by_author_true(self):
        self.ext_api.books_by_author = Mock(return_value=["Dune"])
        self.assertEqual(self.library.is_book_by_author("Frank Herbert", "Dune"), True)

    def test_is_book_by_author_false(self):
        self.ext_api.books_by_author = Mock(return_value=["Other Book"])
        self.assertEqual(self.library.is_book_by_author("Frank Herbert", "Dune"), False)

    def test_get_languages_for_book(self):
        self.ext_api.get_book_info = Mock(return_value=[
            {"title": "Dune", "language": ["eng", "fr"]},
            {"title": "Dune", "language": ["de"]}
        ])
        self.assertEqual(self.library.get_languages_for_book("Dune"), {"eng", "fr", "de"})

    def test_register_patron_new(self):
        self.db_interface.insert_patron = Mock(return_value="123")
        self.assertEqual(self.library.register_patron("John", "Doe", 25, "123"), "123")

    def test_register_patron_existing(self):
        self.db_interface.insert_patron = Mock(return_value=None)
        self.assertEqual(self.library.register_patron("John", "Doe", 25, "123"), None)

    def test_is_patron_registered_true(self):
        patron_mock = Mock()
        patron_mock.get_memberID = Mock(return_value="123")
        self.db_interface.retrieve_patron = Mock(return_value=patron_mock)
        self.assertEqual(self.library.is_patron_registered(patron_mock), True)

    def test_is_patron_registered_false(self):
        patron_mock = Mock()
        patron_mock.get_memberID = Mock(return_value="123")
        self.db_interface.retrieve_patron = Mock(return_value=None)
        self.assertEqual(self.library.is_patron_registered(patron_mock), False)

    def test_borrow_book(self):
        patron_mock = Mock()
        patron_mock.add_borrowed_book = Mock()
        self.db_interface.update_patron = Mock()
        self.library.borrow_book("Dune", patron_mock)
        self.assertEqual(patron_mock.add_borrowed_book.call_args[0][0], "dune")

    def test_return_borrowed_book(self):
        patron_mock = Mock()
        patron_mock.return_borrowed_book = Mock()
        self.db_interface.update_patron = Mock()
        self.library.return_borrowed_book("Dune", patron_mock)
        self.assertEqual(patron_mock.return_borrowed_book.call_args[0][0], "dune")

    def test_is_book_borrowed_true(self):
        patron_mock = Mock()
        patron_mock.get_borrowed_books = Mock(return_value=["dune"])
        self.assertEqual(self.library.is_book_borrowed("Dune", patron_mock), True)

    def test_is_book_borrowed_false(self):
        patron_mock = Mock()
        patron_mock.get_borrowed_books = Mock(return_value=["other"])
        self.assertEqual(self.library.is_book_borrowed("Dune", patron_mock), False)

if __name__ == "__main__":
    unittest.main()
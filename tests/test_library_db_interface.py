import unittest
from unittest.mock import Mock, call
from library import library_db_interface

class TestLibraryDBInterface(unittest.TestCase):

    def setUp(self):
        self.db_interface = library_db_interface.Library_DB()
        #library_db_interface.Patron = Mock()

    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(side_effect=lambda x: 10 if x==data else 0)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)
    
    def test_insert_patron_already_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=('name', 'name', 'age', 'memberID'))
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock()
        self.assertEqual(self.db_interface.insert_patron(patron_mock), None)
    
    def test_insert_patron_not_patron(self):
        patron_mock = Mock()
        self.db_interface.db.insert = Mock()
        self.assertEqual(self.db_interface.insert_patron(not patron_mock), None)
    
    def test_get_patron_count(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.db.all = Mock(return_value=[data])
        self.assertEqual(self.db_interface.get_patron_count(), 1)

    def test_get_all_patrons(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.db.all = Mock(return_value=[data])
        self.assertEqual(self.db_interface.get_all_patrons(), [data])

    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()
    
    def test_update_incorrect_patron(self):
        db_update_mock = Mock()
        self.assertEqual(self.db_interface.update_patron(not db_update_mock), None)
    
    def test_retrieve_patron(self):
        patron_mock = Mock(return_value='memberID')
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID', 'borrowed_books': []}
        self.db_interface.db.search = Mock(return_value=[data])
        self.assertEqual(self.db_interface.retrieve_patron(patron_mock), library_db_interface.Patron('name', 'name', 'age', 'memberID'))

    def test_retrieve_patron_none(self):
        patron_mock = Mock(return_value='notMemberID')
        self.db_interface.db.search = Mock(return_value=None)
        self.assertEqual(self.db_interface.retrieve_patron(patron_mock), None)

    def test_close_db(self):
        db_close_mock = Mock()
        self.db_interface.db.close = db_close_mock
        self.db_interface.close_db()
        db_close_mock.assert_called()

    def test_convert_patron_to_db_format(self):
        patron_mock = Mock()

        patron_mock.get_fname = Mock(return_value=1)
        patron_mock.get_lname = Mock(return_value=2)
        patron_mock.get_age = Mock(return_value=3)
        patron_mock.get_memberID = Mock(return_value=4)
        patron_mock.get_borrowed_books = Mock(return_value=5)
        self.assertEqual(self.db_interface.convert_patron_to_db_format(patron_mock),
                         {'fname': 1, 'lname': 2, 'age': 3, 'memberID': 4,
                          'borrowed_books': 5})
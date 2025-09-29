import unittest
from unittest.mock import Mock
from library import ext_api_interface
import requests
import json

class TestExtAPiInterface(unittest.TestCase):
    def setUp(self):
        self.api = ext_api_interface.Books_API()
        self.book = "learning python"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())

    def test_make_request_True(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value= Mock(status_code = 200, **attr))
        self.assertEqual(self.api.make_request(""), dict())

    def test_make_request_connection_error(self):
        ext_api_interface.requests.get = Mock(side_effect=requests.ConnectionError)
        url = "some url"
        self.assertEqual(self.api.make_request(url), None)

    def test_make_request_False(self):
        requests.get = Mock(return_value=Mock(status_code = 100))
        self.assertEqual(self.api.make_request(""), None)

    def test_get_ebooks(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertEqual(self.api.get_ebooks(self.book), self.books_data)

    def test_get_ebooks_not_in_data(self):
        self.api.make_request = Mock(return_value="")
        self.assertEqual(self.api.get_ebooks(self.book), [])
    
    
    def test_is_book_available_True(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertEqual(self.api.is_book_available(self.book), True)

    def test_is_book_available_False(self):
        self.api.make_request = Mock(return_value="")
        self.assertEqual(self.api.is_book_available(self.book), False)

    def test_get_book_info_not_in_data(self):
        # Test when no data is returned
        self.api.make_request = Mock(return_value="")
        self.assertEqual(self.api.get_book_info(self.book), [])

    def test_get_book_info_returns_expected_list(self):
        data = {
            'docs': [
                {
                    'title': 'Learning Python for Forensics',
                    'publisher': 'Packet Publishing',
                    'publish_year': 2016,
                    'language': 'EN'
                },
            ]
        }
        expected = [
            {
                'title': 'Learning Python for Forensics',
                'publisher': 'Packet Publishing',
                'publish_year': 2016,
                'language': 'EN'
            },
        ]
        self.api.make_request = Mock(return_value=data)
        self.assertEqual(self.api.get_book_info('python'), expected)

    def test_books_by_author(self):
        data = {
            'docs': [
                {
                    'title_suggest': 'David Ascher'
             
                }
            ]
        }
        expected = [
            
                'David Ascher'
             
             
            ]
        self.api.make_request = Mock(return_value=data)
        self.assertEqual(self.api.books_by_author('author'), expected)

    def test_books_by_author_not_in_data(self):
        self.api.make_request = Mock(return_value="")
        self.assertEqual(self.api.books_by_author(self.book),[])

    # def test_books_by_author(self):
    #     self.api.make_request = Mock(return_value=self.json_data)
    #     self.assertEqual(self.api.books_by_author("Ascher, David"), self.json_data)
        
        

if __name__ == "__main__":
    unittest.main()
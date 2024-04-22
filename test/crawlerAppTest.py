import os
import sys
# Add the parent directory of 'test' and 'util' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import crawlerApp
from crawlerApp import CrawlerApp
import unittest

class CrawlerAppTest(unittest.TestCase):
    
    def setUp(self):
        self.app = CrawlerApp()
        self.app.testing = True
        self.client = self.app.app.test_client()
    
    def test_index_route(self):
        print("\n1. Starting test_index_route...")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print("test_index_route test passed.")
    
    # def test_run_crawler_route(self):
    #     # Test with valid data
    #     data = {
    #         'seed_url': 'https://quotes.toscrape.com/',
    #         'max_pages': 10,
    #         'max_depth': 2
    #     }
    #     response = self.client.post('/runcrawler', json=data)
    #     print(response)
    #     self.assertEqual(response.status_code, 200)

    def test_run_crawler_invalid_seed_url(self):
        print("\n2. Starting test_run_crawler_invalid_seed_url...")
        # Test with invalid data
        invalid_data = {
            'seed_url': '',
            'max_pages': 10,
            'max_depth': 2
        }
        response = self.client.post('/runcrawler', json=invalid_data)
        print(response.json)
        self.assertEqual(response.status_code, 400)
        print("test_run_crawler_invalid_seed_url test passed.")
    
    
    # def test_search_route(self):
    #     # Test with valid query
    #     data = {'query': 'world'}
    #     response = self.client.post('/search', json=data)
    #     self.assertEqual(response.status_code, 200)
    #     # Add assertions to check the response content
        
    #     # Test with invalid query
    #     invalid_data = {'invalid_key': 'example query'}
    #     response = self.client.post('/search', json=invalid_data)
    #     self.assertEqual(response.status_code, 400)
    #     # Add assertions to check error response

if __name__ == '__main__':
    unittest.main()

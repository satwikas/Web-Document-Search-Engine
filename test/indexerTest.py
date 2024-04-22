import unittest
import os
import shutil
import sys
import pickle
import tempfile
from sklearn.feature_extraction.text import TfidfVectorizer

# Add the parent directory of 'test' and 'util' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from web_indexer.indexer import Indexer

class IndexerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.html_dir = "test_html"
        cls.temp_index_file = os.path.join(cls.temp_dir, "test_index.pkl")
        os.makedirs(cls.html_dir, exist_ok=True)
        cls.html_files = ["<html><body><p>In 1879, Albert Einstein was born in Ulm, Germany.</p></body></html>",
                           "<html><body><p>Good friends, good books, and a sleepy conscience: this is the ideal life..</p></body></html>",
                           "<html><body><p>The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.</p></body></html>"]
        for i, content in enumerate(cls.html_files):
            with open(os.path.join(cls.html_dir, f"test_{i}.html"), "w") as f:
                f.write(content)
    
    @classmethod
    def tearDownClass(cls):
        # Clean up temporary directory and remove the temporary index file
        shutil.rmtree(cls.html_dir)
        os.remove(cls.temp_index_file)

    def setUp(self,min_df=2):
        self.documents = []
        self.index = {}
        self.indexer = Indexer()

    def test_add_document(self):
        print("\n1. Starting test_add_document...")
        self.indexer.add_document("1", "In 1879, Albert Einstein was born in Ulm, Germany.")
        self.indexer.add_document("2", "Good friends, good books, and a sleepy conscience: this is the ideal life.")
        self.indexer.add_document("3", "The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.")
        self.assertEqual(len(self.indexer.documents), 3)
        print("test_add_document test passed.")
        

    def test_build_index(self):
        print("\n2. Starting test_build_index...")
        self.indexer.load_html_to_indexer(self.html_dir)
        self.indexer.build_index()
        self.assertTrue(self.indexer.index)
        self.assertIsInstance(self.indexer.vectorizer, TfidfVectorizer)
        print("test_build_index test passed.")

    def test_save_index(self):
        print("\n3. Starting test_save_index...")
        # Save the index to the temporary file
        self.indexer.index = self.index
        self.indexer.save_index(self.temp_index_file)

        # Load the saved index from the file
        with open(self.temp_index_file, 'rb') as f:
            loaded_index = pickle.load(f)

        # Compare the loaded index with the original index
        self.assertEqual(loaded_index, self.index)
        print("test_build_index test passed.")

    def test_search(self):
        print("\n3. Starting test_search...")
        self.indexer.load_html_to_indexer(self.html_dir)
        self.indexer.build_index()
        results = dict(self.indexer.search("friends", top_n=3))
        self.assertEqual(len(results), 3)
        self.assertTrue(results['2'], f"Document 2 has the search word and its scrore is greater than 0")
        self.assertTrue(results['1']==0.0, f"Document 1 does not have the search word and its scrore is 0")
        self.assertTrue(results['3']==0.0, f"Document 3 does not have the search word and its scrore is 0")
        print("test_searchtest passed.")

    def test_load_html_to_indexer(self):
        print("\n4. Starting test_load_html_to_indexer...")
        self.indexer.load_html_to_indexer(self.html_dir)
        expected_documents = {
            "1": "In 1879, Albert Einstein was born in Ulm, Germany.",
            "2": "Good friends, good books, and a sleepy conscience: this is the ideal life..",
            "3": "The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid."
        }
        actual_documents = dict(self.indexer.documents)
        self.assertEqual(actual_documents, expected_documents)
        print("test_load_html_to_indexer test passed.")

if __name__ == '__main__':
    unittest.main()

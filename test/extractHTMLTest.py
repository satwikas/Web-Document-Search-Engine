import unittest
from bs4 import BeautifulSoup
import os
import sys

# Add the parent directory of 'test' and 'util' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from util.extractHTML import generate_html_content,extract_text_from_html

class extractHTMLTest(unittest.TestCase):

    def test_extract_text_from_html(self):
        print("1. Starting test_extract_text_from_html...")
        # Sample HTML content
        sample_html = "<html><body><p>This is a sample paragraph.</p></body></html>"

        # Test extract_text_from_html function
        extracted_text = extract_text_from_html([sample_html])
        expected_text = ["This is a sample paragraph."]
        self.assertEqual(extracted_text, expected_text)
        print("extract_text_from_html test passed.")
    
    def test_extract_text_from_html_invalid_content(self):
        print("\n2. Starting test_extract_text_from_html_invalid_content...")
        # Simulate invalid HTML content
        invalid_content = "<not_html>"
        extracted_text = extract_text_from_html([invalid_content])
        self.assertEqual(extracted_text, [""], "Expected empty string for invalid content")
        print("test_extract_text_from_html_invalid_content test passed.")

    def test_generate_html_content(self):
        print("\n3. Starting test_generate_html_content...")
        # Create a temporary directory with sample HTML files
        test_dir = "downloaded_html"
        os.makedirs(test_dir, exist_ok=True)
        sample_html = ["<html><body><p>Sample HTML content 1</p></body></html>",
                       "<html><body><p>Sample HTML content 2</p></body></html>"]
        for i, content in enumerate(sample_html):
            with open(os.path.join(test_dir, f"test_{i}.html"), "w") as f:
                f.write(content)

        # Test generate_html_content function
        html_contents = generate_html_content(test_dir)
        expected_contents = sample_html
        self.assertEqual(html_contents.sort(), expected_contents.sort())
        print("generate_html_content test passed.")

        # Clean up: remove temporary directory
        for filename in os.listdir(test_dir):
            os.remove(os.path.join(test_dir, filename))
        os.rmdir(test_dir)

        # Assert that the temporary directory does not exist
        self.assertFalse(os.path.exists(test_dir), f"Temporary directory '{test_dir}' should not exist after test execution.")
        print("Temporary directory removed.")

    def test_generate_html_content_empty_dir(self):
        print("\n4. Starting test_generate_html_content_empty_dir...")
        test_dir = "test_dir"
        os.makedirs(test_dir, exist_ok=True)

        # Test generate_html_content function with an empty directory
        html_contents = generate_html_content(test_dir)
        self.assertEqual(html_contents, [])

        # Clean up: remove temporary directory
        os.rmdir(test_dir)
        print("test_generate_html_content_empty_dir test passed.")
    
    def test_generate_html_content_non_exist_dir(self):
        print("\n5. Starting test_generate_html_content_non_exist_dir...")
        test_dir = "test_dir"

        # Test generate_html_content function with a non-existent directory
        with self.assertRaises(FileNotFoundError):
            generate_html_content(test_dir)
        print("generate_html_content with non-existent directory test passed.")


if __name__ == '__main__':
    unittest.main()

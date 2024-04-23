from bs4 import BeautifulSoup
import os

def generate_html_content(html_dir):
    """
    Generate a list of HTML contents from HTML files in a directory.
    
    Args:
    html_dir (str): Directory path containing HTML files.
    
    Returns:
    list: List of HTML contents.
    """
    html_contents = []
    for filename in sorted(os.listdir(html_dir)):
        if filename.endswith(".html"):
            file_path = os.path.join(html_dir, filename)
            try:
                with open(file_path, 'r') as file:
                    html_contents.append(file.read())
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    return html_contents

def extract_text_from_html(html_content):
    """
    Extract text content from HTML content using BeautifulSoup.
    
    Args:
    html_content (list): List of HTML contents.
    
    Returns:
    list: List of extracted text.
    """
    extracted_text = []
    for content in html_content:
        try:
            soup = BeautifulSoup(content, 'html.parser')
            extracted_text.append(soup.get_text(separator=',', strip=True))
        except Exception as e:
            print(f"Error extracting text from HTML content: {e}")
            extracted_text.append("")  # Append empty string if extraction fails
    return extracted_text


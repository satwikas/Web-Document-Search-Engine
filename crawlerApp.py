import webbrowser
from flask import Flask, request, jsonify, render_template, redirect
import web_indexer.indexer as indexer
import subprocess
import os
import shutil

class CrawlerApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.html_dir = os.path.join(self.project_dir, 'downloaded_files')
        self.indexer = indexer.Indexer()

        @self.app.route('/', methods=['GET'])
        def index():
            return render_template('index.html')

        @self.app.route('/runcrawler', methods=['POST'])
        def run_crawler():
            try:
                # # shutil.rmtree(self.html_dir)
                self.remove_files_in_dir(self.html_dir)
                seed_url = request.json['seed_url']
                max_pages = request.json['max_pages']
                max_depth = request.json['max_depth']
                command = f"scrapy runspider webcrawler.py -a seed_url='{seed_url}' -a max_pages={max_pages} -a max_depth={max_depth}"
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                print(result)
                # Check if html_dir is not empty
                if not os.listdir(self.html_dir):
                    return jsonify({"error": "Invalid url unable to scrape webpage"}), 400
                self.indexer.load_html_to_indexer(self.html_dir)
                self.indexer.build_index()
                self.indexer.save_index("index.pkl")
                self.indexer.load_index("index.pkl")
                output = result.stdout
                return jsonify({"message": "Successfully crawled webpages", "output": output})
            except Exception as e:
                print("Exception caught:", e)
                return jsonify({"error": str(e)}), 400

        @self.app.route('/search', methods=['POST'])
        def process_query():
            if request.is_json and 'query' in request.json:
                query = request.json['query']
                if not self.validate_query(query):
                    return jsonify({'error': 'Invalid query'}), 400
                top_k = 10
                sorted_scores = self.search(query, top_k)
                results = [{'doc_id': doc_id, 'score': score} for doc_id, score in sorted_scores if score > 0]
                return jsonify(results)
            else:
                return jsonify({'error': 'Missing or invalid JSON data'}), 400

    def validate_query(self, query):
        if not query.strip():
            return False
        return True

    def search(self, query, top_k):
        results = self.indexer.search(query, top_k)
        print("Search results:", results)
        return results
    
    def remove_files_in_dir(self,directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def open_browser(self):
        webbrowser.open('http://127.0.0.1:5000')

    def run(self):
        self.open_browser()
        self.app.run(debug=False)

if __name__ == '__main__':
    search_app = CrawlerApp()
    search_app.run()

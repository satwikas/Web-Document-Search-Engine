import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import util.extractHTML as extractHTML
import numpy as np

class Indexer:
    def __init__(self):
        self.documents = []
        self.index = {}
        self.vectorizer = TfidfVectorizer()

    def add_document(self, document_id, text):
        self.documents.append((document_id, text))
        # print(self.documents)

    def build_index(self):
        corpus = [text for _, text in self.documents]
        # print(corpus)
        # Fit the vectorizer here
        tfidf_matrix = self.vectorizer.fit_transform(corpus)  

        feature_names = self.vectorizer.get_feature_names_out()
        for i, document in enumerate(self.documents): 
            document_id, _ = document
            feature_index = tfidf_matrix[i,:].nonzero()[1]
            for idx in feature_index:
                if feature_names[idx] not in self.index:
                    self.index[feature_names[idx]] = []
                self.index[feature_names[idx]].append((document_id, tfidf_matrix[i, idx]))

    def save_index(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.index, f)

    def load_index(self, filename):
        with open(filename, 'rb') as f:
            self.index = pickle.load(f)
        # Fit the vectorizer with the loaded documents
        corpus = [text for _, text in self.documents]
        self.vectorizer.fit(corpus)

    def search(self, query, top_n):
    # Transform query into TF-IDF vector
        query_vector = self.vectorizer.transform([query])

        # Initialize dictionary to store document vectors
        document_vectors = {}

        # Iterate over each term in the index
        for term, postings in self.index.items():
            # Iterate over each posting (document ID, TF-IDF score) for the current term
            for doc_id, tfidf_score in postings:
                # If the document ID is encountered for the first time, create a new entry in document_vectors
                if doc_id not in document_vectors:
                    document_vectors[doc_id] = np.zeros((1, len(self.vectorizer.vocabulary_)))

                # Accumulate the TF-IDF score for the term in the document vector
                document_vectors[doc_id][0, self.vectorizer.vocabulary_[term]] = tfidf_score

        # Compute cosine similarity between query vector and each document vector
        similarities = []
        for doc_id, doc_vector in document_vectors.items():
            # Calculate cosine similarity
            similarity = cosine_similarity(query_vector, doc_vector)
            similarities.append((doc_id, similarity[0][0]))

        # Sort the similarities based on cosine similarity scores
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return the top N most relevant documents
        return similarities[:top_n]

    def load_html_to_indexer(self, html_dir):
        html_content = extractHTML.generate_html_content(html_dir)
        extracted_text = extractHTML.extract_text_from_html(html_content)
        for j in range(len(extracted_text)):
            self.add_document(str(j+1), extracted_text[j])

import os
import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path=None):
        if file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of portfolio.py
            file_path = os.path.join(base_dir, "resource", "my_portfolio.csv")  # Ensure correct path

        self.file_path = file_path

        # ✅ Debugging: Check if the file exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Error: The file '{self.file_path}' was not found. Check the path!")

        self.data = pd.read_csv(self.file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=[row["Techstack"]],  # Fix: Ensure it's a list
                                    metadatas=[{"links": row["Links"]}],  # Fix: Ensure it's a list
                                    ids=[str(uuid.uuid4())])  # Generate unique IDs

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pandas as pd
import os



def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(text)
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalnum() and word.lower() not in stop_words]
    return ' '.join(words)


def cluster_documents(documents, max_clusters=3):
    
    processed_docs = [preprocess_text(doc) for doc in documents]

    
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(processed_docs)

    
    n_clusters = min(len(documents), max_clusters)

    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)

    
    clusters = kmeans.labels_
    return clusters


def get_cluster_name(cluster_num):
    cluster_names = {0 : "Sports", 1: "Business", 2:"Health"}
    return cluster_names.get(cluster_num, "Unknown")


def save_to_csv(documents, clusters, filename='clustered_documents.csv'):
    data = {
        'Document': documents,
        'Cluster': clusters,
        'Cluster Name':[get_cluster_name(cluster) for cluster in clusters]
    }
    df = pd.DataFrame(data)
    
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, mode='w', header=True, index=False)


class DocumentClusteringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Clustering")

        self.label = tk.Label(root, text="Enter news articles (separate articles with double newlines):")
        self.label.pack()

        self.text_area = scrolledtext.ScrolledText(root, width=50, height=20)
        self.text_area.pack()

        self.cluster_button = tk.Button(root, text="Cluster Documents", command=self.cluster_documents)
        self.cluster_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def cluster_documents(self):
        content = self.text_area.get("1.0", tk.END).strip()
        documents = [doc.strip() for doc in content.split('\n\n') if doc.strip()]
        if not documents:
            messagebox.showwarning("Input Error", "Please enter some news articles to cluster.")
            return

        clusters = cluster_documents(documents)
        save_to_csv(documents, clusters)
        result_text = ""
        for doc, cluster in zip(documents, clusters):
            cluster_name = get_cluster_name(cluster)
            result_text += f"Cluster {cluster} ({cluster_name}):\n{doc}\n\n"

        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentClusteringApp(root)
    root.mainloop()




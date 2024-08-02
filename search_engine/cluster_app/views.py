from django.shortcuts import render
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import csv
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

def cluster_view(request):
    return render(request, 'cluster.html')

def cluster_result(request):
    csv_path = 'C:/Users/dipak/Downloads/clg module/info retrival/assignment_coding/search_engine_project/search_engine/static/newsdata.csv'
    df = pd.read_csv(csv_path, encoding='latin-1')

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    processed_doc = []
    for title in df['Title']:
        tokens = nltk.word_tokenize(title)
        words = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalnum() and word.lower() not in stop_words]
        processed_doc.append(' '.join(words))

    vectorizer = TfidfVectorizer(stop_words='english',ngram_range=(1, 2),max_df=0.95,min_df=2)
    X = vectorizer.fit_transform(processed_doc)

    n_clusters = min(len(df['Title']), 3)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X)

    PCA_1 = PCA(n_components = 2)
    x_reduce = PCA_1.fit_transform(X.toarray())
    silhouette_avg = silhouette_score(x_reduce, kmeans.labels_)
    # print("Silhouette Score:", silhouette_avg) 

    top_n = 10
    terms = vectorizer.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

    top_words_per_cluster = {}
    for i in range(n_clusters):
        top_words = [terms[ind] for ind in order_centroids[i, :top_n]]
        top_words_per_cluster[i] = top_words
        print((f"Cluster{i}:{','.join(top_words)}"))

    if request.method == 'POST':
        new_doc = request.POST.get('document')
        new_processed_doc = []
        query_tokens = nltk.word_tokenize(new_doc)
        new_words = [lemmatizer.lemmatize(word.lower()) for word in query_tokens if word.isalnum() and word.lower() not in stop_words]
        new_processed_doc.append(' '.join(new_words))
        new_X = vectorizer.transform(new_processed_doc)

        predicted = kmeans.predict(new_X)[0]
        cluster_categories = { 0: "Economy",1: "Politics", 2: "Entertainment"}
        cluster_category = cluster_categories.get(predicted, 'unknown')

      

        # Append the new document and its cluster category to the DataFrame
        # new_row = pd.DataFrame({'Title': [new_doc], 'Category': [cluster_category], })
        # with open(csv_path, mode = 'a' , newline = '') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([new_doc,cluster_category])
        context = {
            'cluster_category': cluster_category,
        }
        return render(request, 'result.html', context)
    return render(request, 'cluster.html')













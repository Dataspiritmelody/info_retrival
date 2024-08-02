import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import os
from sklearn.metrics import silhouette_score

csv_path = 'C:/Users/dipak/Downloads/clg module/info retrival/assignment_coding/search_engine_project/search_engine/static/newsdata.csv'
df = pd.read_csv(csv_path, encoding='latin-1')


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# new_doc = 'Mr Kwatra said there were about 35-50 Indians in the Russian forces, of whom 10 had already been brought home. The two countries would now work to bring back the remaining men, he added.'
new_doc = 'Four years later, Murray swiftly put the disappointment of a Wimbledon final defeat by Roger Federer behind him, defeating the Swiss in straight sets at London 2012 to win gold.'
processed_doc = []
for title in df['Title']:
     tokens = nltk.word_tokenize(title)
     words = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalnum() and word.lower() not in stop_words]
     processed_doc.append(' '.join(words))


# processed_docs = [preprocess_text(doc) for doc in documents]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(processed_doc)


n_clusters = min(len(df['Title']), 3)

    
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X)

    
# clusters = kmeans.labels_
# Calculate silhouette score
silhouette_avg = silhouette_score(X, kmeans.labels_)
print(f"Silhouette Score: {silhouette_avg}")


# Top words 

# names = vectorizer.get_feature_names_out()
# centroid = kmeans.cluster_centers_.argsort()[:,::-1]
# for i  in range(n_clusters):
#     #  print(f"top words of cluster {i}" )
#      for j in centroid[i, :15]:
#         #   print(f"{names[j]}")
          
new_processed_doc =[]
query_tokens = nltk.word_tokenize(new_doc)
new_words = [lemmatizer.lemmatize(word.lower()) for word in query_tokens if word.isalnum() and word.lower() not in stop_words]
new_processed_doc.append(' '.join(new_words))
# new_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
new_X = vectorizer.transform(new_processed_doc)

predicted = kmeans.predict(new_X)[0]
cluster_categories = {0:"Entertainment", 1: "Politics", 2:"Economy"}
cluster_category = cluster_categories.get(predicted,'unknown')
print(cluster_category)

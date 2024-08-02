from django.shortcuts import render
from django.http import HttpResponse
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd 
import json

def index_view(request):
    return render(request, 'index.html')

def search_view(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
    else:
        return HttpResponse('No query provided.')

    nltk.download('punkt')
    nltk.download('stopwords')

    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))


    csv_path = 'C:\\Users\\dipak\\Downloads\\clg module\\info retrival\\assignment_coding\\search_engine_project\\pub.csv'
    df = pd.read_csv(csv_path)
    
    
    processed_document = []
    for i in range(len(df)):
        title_token = nltk.word_tokenize(df.iloc[i]['Title'].lower())
        title_stem_token = []
        for token in title_token:
            if token not in stop_words:
                stem_tokens = ps.stem(token)
                title_stem_token.append(stem_tokens)
        title = ' '.join(title_stem_token)

        authors_json = df.iloc[i]['Author']
        authors_processed = []
        authors = json.loads(authors_json.replace("'", "\""))
        for author in authors:
            author_names = author['name']
            author_stem_token = []
            author_token = nltk.word_tokenize(author_names.lower())
            for token in author_token:
                if token not in stop_words:
                    stem_tokens = ps.stem(token)
                    author_stem_token.append(stem_tokens)
            authors_processed.append(' '.join(author_stem_token))

        combined_documents = title + ' ' + ' '.join(authors_processed)
        processed_document.append(combined_documents)
   
    vectorizer = TfidfVectorizer(ngram_range=(1,4), analyzer='char')
    tfidf_matrix = vectorizer.fit_transform(processed_document)

    tokens = nltk.word_tokenize(query.lower())
    query_stem_token = []
    for token in tokens:
        if token not in stop_words:
            stem_tokens = ps.stem(token)
            query_stem_token.append(stem_tokens)
    processed_query = ' '.join(query_stem_token)

    query_vector = vectorizer.transform([processed_query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    sorting = cosine_similarities.argsort()[::-1]
    results = []
    for i in sorting:
        relevence_score = float(cosine_similarities[i])
        title = df.iloc[i]['Title']
        authors = json.loads(df.iloc[i]['Author'].replace("'", "\""))
        processed_authors = [{'name': author['name'], 'link': author.get('link', '#')} for author in authors]
        result = {'title': title, 'publication_link ':df.iloc[i]['Publication link'] ,'authors': processed_authors, 'publication_date':df.iloc[i]['publication Date'], 'relevance_score':   relevence_score }
        results.append(result)


    # Render the results in a template or return them as JSON
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'search_results.html', context)

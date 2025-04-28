import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pandas as pd
import time
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load and preprocess FAQ dataset
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['question_processed'] = df['question'].str.lower()
    df['question_processed'] = df['question_processed'].str.replace(r'[^\w\s]', '', regex=True)
    df['question_processed'] = df['question_processed'].str.strip()
    return df

# TF-IDF Retrieval
def tfidf_retrieval(query, df, vectorizer, tfidf_matrix, top_k=20):
    query_processed = query.lower().replace(r'[^\w\s]', '').strip()
    query_vec = vectorizer.transform([query_processed])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = np.argsort(similarities)[::-1][:top_k]
    top_scores = similarities[top_indices]
    return df.iloc[top_indices][['question', 'answer']].to_dict('records'), top_scores

# Semantic Reranking
def semantic_reranking(query, candidates, model, top_k=5):
    candidate_questions = [cand['question'] for cand in candidates]
    query_embedding = model.encode(query)
    candidate_embeddings = model.encode(candidate_questions)
    similarities = cosine_similarity([query_embedding], candidate_embeddings).flatten()
    top_indices = np.argsort(similarities)[::-1][:top_k]
    top_scores = similarities[top_indices]
    reranked = [candidates[i] for i in top_indices]
    return reranked, top_scores

# Hybrid Retrieval Pipeline
def hybrid_retrieval(query, df, tfidf_vectorizer, tfidf_matrix, embedding_model, top_k=5):
    start_time = time.time()
    tfidf_candidates, tfidf_scores = tfidf_retrieval(query, df, tfidf_vectorizer, tfidf_matrix, top_k=20)
    reranked_candidates, reranked_scores = semantic_reranking(query, tfidf_candidates, embedding_model, top_k=top_k)
    response_time = time.time() - start_time
    return {
        'results': reranked_candidates,
        'scores': reranked_scores.tolist(),
        'response_time': response_time
    }

# Evaluation Metrics
def evaluate_metrics(test_df, df, tfidf_vectorizer, tfidf_matrix, embedding_model, top_k=5):
    precision_at_1 = 0
    recall_at_k = 0
    mrr = 0
    total_queries = len(test_df)

    for _, row in test_df.iterrows():
        query = row['query']
        relevant = row['relevant_question']
        result = hybrid_retrieval(query, df, tfidf_vectorizer, tfidf_matrix, embedding_model, top_k=top_k)
        retrieved_questions = [res['question'] for res in result['results']]

        # Precision@1: Is the top result correct?
        if retrieved_questions[0] == relevant:
            precision_at_1 += 1

        # Recall@K: Is the relevant question in the top K results?
        if relevant in retrieved_questions:
            recall_at_k += 1

        # MRR: Reciprocal rank of the first relevant result
        for rank, question in enumerate(retrieved_questions, 1):
            if question == relevant:
                mrr += 1 / rank
                break

    precision_at_1 /= total_queries
    recall_at_k /= total_queries
    mrr /= total_queries

    return {
        'Precision@1': precision_at_1,
        'Recall@K': recall_at_k,
        'MRR': mrr
    }

# Initialize models
def initialize_models(df):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['question_processed'])
    # Use all-distilroberta-v1 for better semantic understanding
    embedding_model = SentenceTransformer('all-distilroberta-v1')
    return tfidf_vectorizer, tfidf_matrix, embedding_model

# Browser-friendly root route
@app.route('/')
def home():
    return '''
        <h1>FAQ Retrieval System</h1>
        <form action="/faq" method="POST">
            <label>Enter your query:</label><br>
            <input type="text" name="query" placeholder="e.g., How do I track my order?"><br>
            <input type="submit" value="Search">
        </form>
    '''

# FAQ retrieval endpoint (supports both JSON and form submissions)
@app.route('/faq', methods=['POST'])
def faq_retrieval():
    if request.is_json:
        data = request.get_json()
    else:
        data = {'query': request.form.get('query', '')}

    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    result = hybrid_retrieval(query, df, tfidf_vectorizer, tfidf_matrix, embedding_model)
    
    if not request.is_json:
        html = '<h1>Results</h1><ul>'
        for res in result['results']:
            html += f"<li><b>{res['question']}</b>: {res['answer']}</li>"
        html += f'</ul><p>Response Time: {result["response_time"]} seconds</p>'
        html += '<a href="/">Back</a>'
        return html
    return jsonify(result)

if __name__ == '__main__':
    # Load FAQ dataset
    df = load_and_preprocess_data('faq_dataset.csv')
    
    # Initialize models
    tfidf_vectorizer, tfidf_matrix, embedding_model = initialize_models(df)
    
    # Evaluate the system
    try:
        test_df = pd.read_csv('test_queries.csv')
        metrics = evaluate_metrics(test_df, df, tfidf_vectorizer, tfidf_matrix, embedding_model)
        print("Evaluation Metrics:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.3f}")
    except FileNotFoundError:
        print("Warning: test_queries.csv not found. Skipping evaluation.")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
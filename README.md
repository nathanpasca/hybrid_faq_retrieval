# Hybrid FAQ Retrieval System

This project implements a hybrid FAQ retrieval system that combines TF-IDF for keyword-based retrieval with sentence embeddings for semantic reranking, as proposed in the paper "Hybrid FAQ Retrieval with TF-IDF and Sentence Embeddings: Enhancing Accuracy for Paraphrased Queries." The system is designed to handle paraphrased queries efficiently in customer support applications, such as e-commerce platforms. It was developed in Python, deployed as a RESTful API using Flask, and includes a browser-friendly interface for user interaction.

## Overview

The system follows a two-stage pipeline:
1. **TF-IDF Retrieval**: Uses Scikit-learn's `TfidfVectorizer` to retrieve the top 20 FAQs based on keyword similarity.
2. **Semantic Reranking**: Employs the `all-distilroberta-v1` model from Sentence-Transformers to rerank the top 20 FAQs by semantic similarity, returning the top 5.

Key features:
- A synthetic dataset of 50 e-commerce FAQs covering shipping, returns, account management, and payments
- Evaluation metrics: Precision@1 (0.800), Recall@5 (1.000), MRR (0.900)
- Average response time: 0.232 seconds on a CPU in WSL2
- RESTful API with Flask and a browser interface for easy testing

## Prerequisites

- **Operating System**: Tested on WSL2 (Windows Subsystem for Linux 2) with Ubuntu
- **Python**: Version 3.8 or higher
- **Dependencies**: Listed in `requirements.txt`

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hybrid_faq_retrieval
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

The requirements.txt file includes:
```
pandas
numpy
scikit-learn
sentence-transformers
transformers
flask
regex
```

### 4. Generate the FAQ Dataset
Run the script to create faq_dataset.csv:
```bash
python3 generate_faq_dataset.py
```

### 5. Generate the Test Queries
Run the script to create test_queries.csv for evaluation:
```bash
python3 generate_test_queries.py
```

Ensure Windows Firewall allows traffic on port 5000.

## Usage

### 1. Run the Flask Application
Start the Flask server:
```bash
python3 hybrid_faq_retrieval.py
```

The server will run on http://0.0.0.0:5000. You'll see evaluation metrics printed to the console:
```
Evaluation Metrics:
Precision@1: 0.800
Recall@K: 1.000
MRR: 0.900
```

### 2. Test via API
Use curl to send a query:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"query":"How do I track my order?"}' http://localhost:5000/faq
```

Example response:
```json
{
  "response_time": 0.23241758346557617,
  "results": [
    {
      "answer": "Log in to your account, go to 'Order History,' and click your order number for a tracking link. If it's not active, your order is still processing. Contact support@shop.com for help.",
      "question": "How do I track my order?"
    },
    ...
  ],
  "scores": [1.0, ...]
}
```

### 3. Test via Browser
- Open http://127.0.0.1:5000 in a browser
- Enter a query (e.g., "Where's my package?") in the form and submit
- View the top 5 FAQs with their answers and response time

## Project Structure

- `hybrid_faq_retrieval.py`: Main script with the hybrid retrieval pipeline, Flask API, and evaluation metrics
- `generate_faq_dataset.py`: Script to create the FAQ dataset (faq_dataset.csv)
- `generate_test_queries.py`: Script to create the test queries (test_queries.csv)
- `faq_dataset.csv`: Dataset of 50 e-commerce FAQs
- `test_queries.csv`: Test set for evaluation
- `requirements.txt`: List of Python dependencies

## Results

The system was evaluated on a test set of 5 queries:

- Precision@1: 0.800 (80% of queries had the correct FAQ ranked first)
- Recall@5: 1.000 (all relevant FAQs were in the top 5)
- MRR: 0.900 (relevant FAQs were ranked high, averaging rank 1–2)
- Response Time: 0.232 seconds per query on a CPU in WSL2

The system effectively handles both exact and paraphrased queries, with minor improvements needed for certain semantic matches (e.g., "How to reset password?" vs. "How do I reset my password?").

## Future Work

- Expand the test set for more robust evaluation
- Fine-tune the all-distilroberta-v1 model on the FAQ dataset to improve semantic accuracy
- Add multilingual support using models like paraphrase-multilingual-mpnet-base-v2
- Optimize response time with GPU support in WSL2

## License

This project is licensed under the MIT License.

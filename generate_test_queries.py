import pandas as pd

# Test queries with ground truth
test_data = [
    {"query": "How do I track my order?", "relevant_question": "How do I track my order?"},
    {"query": "Where’s my package?", "relevant_question": "Where’s my package?"},
    {"query": "How to reset password?", "relevant_question": "How do I reset my password?"},
    {"query": "What’s the return process?", "relevant_question": "What’s the process for sending something back?"},
    {"query": "How long does shipping take?", "relevant_question": "How long does shipping take?"},
]

# Create DataFrame and save to CSV
test_df = pd.DataFrame(test_data)
test_df.to_csv('test_queries.csv', index=False)
print("Test queries saved to 'test_queries.csv'.")
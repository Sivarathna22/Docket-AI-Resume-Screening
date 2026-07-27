import ollama

# Test 1: Basic chat with the LLM
response = ollama.chat(
    model='qwen2.5:3b-instruct',
    messages=[
        {'role': 'user', 'content': 'Say hello and confirm you are working, in one short sentence.'}
    ]
)
print("=== LLM Test ===")
print(response['message']['content'])

# Test 2: Embeddings
embed_response = ollama.embeddings(
    model='nomic-embed-text',
    prompt='This is a test sentence for embeddings.'
)
print("\n=== Embedding Test ===")
print(f"Embedding vector length: {len(embed_response['embedding'])}")
print(f"First 5 values: {embed_response['embedding'][:5]}")
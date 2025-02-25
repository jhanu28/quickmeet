from transformers import AutoTokenizer, AutoModel
import torch

# Replace with a different model identifier if needed
model_name = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Example summary
summary = "This is a sample meeting summary."

# Tokenize the input text
inputs = tokenizer(summary, return_tensors="pt", truncation=True, padding=True, max_length=512)

# Generate embeddings
with torch.no_grad():
    embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Pooling the token embeddings

print("Generated Embeddings: ", embeddings)

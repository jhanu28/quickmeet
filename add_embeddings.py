from sentence_transformers import SentenceTransformer
from weaviate_integration import client  # Your Weaviate client

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can choose another model

# The meeting transcript data (from your Weaviate data or input data)
meeting_transcripts = [
    "This is a sample transcript for the meeting.",
    "Another example transcript for a different meeting."
]

# Generate embeddings for the meeting transcripts
embeddings = model.encode(meeting_transcripts)

# Add embeddings to Weaviate for each transcript
for i, transcript in enumerate(meeting_transcripts):
    data_object = {
        "text": transcript,  # Text to store
        "embedding": embeddings[i].tolist()  # Convert embedding to list for storage
    }

    # Add data object to Weaviate
    client.data_object.create(data_object, class_name="Meeting")

print("Embeddings and data added successfully!")


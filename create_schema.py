import weaviate

client = weaviate.Client("http://localhost:8080")

# Define the schema with image-related properties
meeting_schema = {
    "classes": [
        {
            "class": "MeetingNotes",
            "description": "Stores transcriptions, summaries, action items, and images for meetings.",
            "properties": [
                {
                    "name": "meeting_id",
                    "dataType": ["string"],
                    "description": "Unique ID for the meeting."
                },
                {
                    "name": "transcript",
                    "dataType": ["text"],
                    "description": "Full transcription of the meeting."
                },
                {
                    "name": "summary",
                    "dataType": ["text"],
                    "description": "Summarized version of the meeting."
                },
                {
                    "name": "action_items",
                    "dataType": ["text"],
                    "description": "Key action points from the meeting."
                },
                {
                    "name": "date",
                    "dataType": ["date"],
                    "description": "Date of the meeting."
                },
                {
                    "name": "image_url",
                    "dataType": ["string"],
                    "description": "URL of the image related to the meeting."
                },
                {
                    "name": "image_blob",
                    "dataType": ["blob"],
                    "description": "Binary data of the image related to the meeting (optional)."
                }
            ]
        }
    ]
}

# Add the schema to Weaviate
client.schema.create(meeting_schema)

print("✅ Schema created successfully!")

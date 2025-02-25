import json
import re
import boto3
from transformers import pipeline

# ✅ Ensure correct AWS region
session = boto3.Session(region_name="us-east-1")  # Update region if needed
dynamodb = session.resource("dynamodb")
table_name = "QuickMeetData"

# ✅ Check if Table Exists
try:
    table = dynamodb.Table(table_name)
    table.load()  # This will throw an error if the table doesn't exist
except:
    raise Exception(f"❌ Table '{table_name}' not found. Check AWS Console.")

# Load Transcription JSON
with open("QuickMeetTest.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract transcript text
transcribed_text = data["results"]["transcripts"][0]["transcript"]
word_count = len(transcribed_text.split())

# Choose Model Based on Transcript Length
if word_count > 1024:
    model_name = "google/long-t5-tglobal-base"
    min_length = max(100, word_count // 4)
    max_length = min(500, word_count // 2)
else:
    model_name = "philschmid/bart-large-cnn-samsum"
    min_length = max(50, word_count // 3)
    max_length = min(300, word_count // 1.5)

print(f"Using Model: {model_name}")
print(f"Min Length: {min_length}, Max Length: {max_length}")

# Load Summarization Model
summarizer = pipeline("summarization", model=model_name, tokenizer=model_name)

# Generate Summary
summary = summarizer(
    transcribed_text,
    min_length=min_length,
    max_length=max_length,
    do_sample=False
)[0]["summary_text"]

# Extract Action Items (Ensuring Correct Name Assignment)
action_items = []
task_patterns = [
    r"(\b[A-Z][a-z]+)\s+will\s+(.*?)(?:\.\s|$)",  # Matches "Name will do something"
    r"(\b[A-Z][a-z]+)\s+is\s+responsible\s+for\s+(.*?)(?:\.\s|$)",  # Matches "Name is responsible for..."
    r"Deadline:\s*(\w+\s+\d{1,2})",  # Matches "Deadline: Month Day"
]

names = set()
for pattern in task_patterns:
    matches = re.findall(pattern, summary)
    for match in matches:
        if isinstance(match, tuple):
            name, task = match
            names.add(name)
            action_items.append(f"- {name}: {task.strip()}")
        else:
            action_items.append(f"- {match.strip()}")

# ✅ Fix "He" or "She" by assigning last mentioned name
name_list = list(names)  # Convert set to list
for i, item in enumerate(action_items):
    if item.startswith("- He") or item.startswith("- She"):
        previous_name = next((name for name in reversed(name_list) if name in action_items[i - 1]), "Unknown")
        action_items[i] = item.replace("He: ", f"{previous_name}: ").replace("She: ", f"{previous_name}: ")

# Save Summary
with open("summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)

# Save Action Items
with open("action_items.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(action_items) if action_items else "No specific action items found.")

# ✅ Store to DynamoDB
try:
    table.put_item(
        Item={
            "MeetingID": data.get("meeting_id", "unknown_meeting"),  # Use default if missing
            "Summary": summary,
            "ActionItems": action_items
        }
    )
    print("\n✅ Data stored in DynamoDB 🚀")
except Exception as e:
    print(f"❌ Failed to store data in DynamoDB: {e}")

print("✅ Summary saved to summary.txt")
print("✅ Action Items saved to action_items.txt")

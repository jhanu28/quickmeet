import weaviate
import argparse
import json
import os

# 🔹 Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")  # Change to your Weaviate endpoint

# Define the class name in Weaviate
class_name = "MeetingSummary"

def semantic_search_by_keyword(keyword):
    """ Perform semantic search on the summaries using the keyword """
    try:
        # Correct way to perform semantic search in Weaviate with a text vectorizer
        response = client.query.get(class_name, ["Summary", "MeetingID"]) \
                              .with_additional("vector") \
                              .with_near_text({"concepts": [keyword]}) \
                              .do()

        if 'data' in response and 'Get' in response['data']:
            results = response['data']['Get'].get(class_name, [])
            if results:
                for result in results:
                    print(f"\n✅ **Match Found in Meeting: {result['MeetingID']}**")
                    print(f"📝 **Summary:** {result['Summary']}")
            else:
                print("\n❌ No matches found for the given keyword.\n")
        else:
            print("\n❌ Invalid response structure. Please check your Weaviate setup.\n")
            print("Response:", response)

    except Exception as e:
        print(f"Error during semantic search: {e}")

def semantic_search_by_attendee(name):
    """ Perform semantic search for action items assigned to a specific attendee """
    try:
        # Search for action items using the name of the attendee
        response = client.query.get(class_name, ["ActionItems", "MeetingID"]) \
                              .with_additional("vector") \
                              .with_near_text({"concepts": [name]}) \
                              .do()

        if 'data' in response and 'Get' in response['data']:
            results = response['data']['Get'].get(class_name, [])
            if results:
                for result in results:
                    print(f"\n👤 **Tasks Assigned to {name.capitalize()} in Meeting: {result['MeetingID']}**")
                    print(f"📋 **Action Items:**")
                    for action in result['ActionItems']:
                        print(f"- {action}")
            else:
                print(f"\n❌ No tasks assigned to {name.capitalize()} found.\n")
        else:
            print("\n❌ Invalid response structure. Please check your Weaviate setup.\n")
            print("Response:", response)

    except Exception as e:
        print(f"Error during semantic search: {e}")

# 🔹 Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--keyword", type=str, help="Search for a keyword in summaries and action items")
parser.add_argument("--name", type=str, help="Search for action items assigned to a specific attendee")
args = parser.parse_args()

# 🔹 Execute based on user input
if args.keyword:
    semantic_search_by_keyword(args.keyword)
elif args.name:
    semantic_search_by_attendee(args.name)
else:
    print("\n⚠️ Please provide a search argument (--keyword or --name).\n")

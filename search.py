import boto3
import argparse
import re

# 🔹 Initialize DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")  # Change if needed
table_name = "QuickMeetSummaries"  # Your actual table name
table = dynamodb.Table(table_name)

def get_meeting_by_id(meeting_id):
    """ Fetch details of a specific meeting using MeetingID """
    response = table.get_item(Key={'MeetingID': meeting_id})
    item = response.get("Item")
    
    if item:
        print(f"\n📌 **Meeting Details for '{meeting_id}':**\n")
        print(f"📝 **Summary:** {item.get('Summary', 'N/A')}\n")
        print(f"📋 **Action Items:**")
        for action in item.get("ActionItems", []):
            print(f"- {action}")
    else:
        print(f"\n❌ No meeting found with MeetingID: '{meeting_id}'.\n")

def extract_matching_sentences(text, keyword):
    """ Extract sentences containing the keyword """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if keyword.lower() in s.lower()]

def search_by_keyword(keyword):
    """ Search for a keyword inside meeting summaries & action items """
    response = table.scan()
    results = []

    for item in response.get("Items", []):
        matching_sentences = extract_matching_sentences(item.get("Summary", ""), keyword)
        matching_actions = [a for a in item.get("ActionItems", []) if keyword.lower() in a.lower()]
        
        if matching_sentences or matching_actions:
            print(f"\n✅ **Matches in Meeting: {item['MeetingID']}**\n")
            for sentence in matching_sentences:
                print(f"- {sentence}")
            for action in matching_actions:
                print(f"📌 **Action Item:** {action}")

def search_by_attendee(name):
    """ Search action items assigned to a specific person """
    response = table.scan()
    results = []

    for item in response.get("Items", []):
        matching_actions = [a for a in item.get("ActionItems", []) if name.lower() in a.lower()]
        
        if matching_actions:
            print(f"\n👤 **Tasks Assigned to {name.capitalize()} in Meeting: {item['MeetingID']}**\n")
            for action in matching_actions:
                print(f"- {action}")

# 🔹 Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--meetingid", type=str, help="Search by MeetingID")
parser.add_argument("--keyword", type=str, help="Search for a keyword in summaries and action items")
parser.add_argument("--name", type=str, help="Search for action items assigned to a specific attendee")
args = parser.parse_args()

# 🔹 Execute based on user input
if args.meetingid:
    get_meeting_by_id(args.meetingid)
elif args.keyword:
    search_by_keyword(args.keyword)
elif args.name:
    search_by_attendee(args.name)
else:
    print("\n⚠️ Please provide a search argument (--meetingid, --keyword, or --name).\n")

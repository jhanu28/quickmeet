import boto3
import json
import time
import os
import requests

REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "quickmeet-files")

transcribe = boto3.client("transcribe", region_name=REGION)
s3 = boto3.client("s3")

def start_transcription_job(job_name, media_file_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": media_file_uri},
        MediaFormat="mp3",
        LanguageCode="en-US",
        OutputBucketName=BUCKET_NAME
    )
    return response

def wait_for_transcription(job_name):
    while True:
        result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = result["TranscriptionJob"]["TranscriptionJobStatus"]
        if status in ["COMPLETED", "FAILED"]:
            break
        print("Transcription job in progress. Waiting 5 seconds...")
        time.sleep(5)
    
    if status == "COMPLETED":
        return result["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    else:
        print("Transcription job failed.")
        return None

if __name__ == "__main__":
    media_file_uri = f"s3://{BUCKET_NAME}/test_audio.mp3"
    job_name = "QuickMeetTranscriptionJob2"

    print("Starting transcription job...")
    start_transcription_job(job_name, media_file_uri)

    print("Waiting for transcription to complete...")
    transcript_url = wait_for_transcription(job_name)

    if transcript_url:
        print("Transcription completed!")
        print("Transcript URL:", transcript_url)

        # First, try downloading with `boto3`
        try:
            s3.download_file(BUCKET_NAME, "QuickMeetTranscriptionJob1.json", "QuickMeetTest.json")
            print("Transcript downloaded using boto3 and saved as QuickMeetTest.json")
        except Exception as e:
            print("Boto3 download failed. Trying requests...")
            
            response = requests.get(transcript_url)
            print(f"Response Status Code: {response.status_code}")

            if response.status_code == 200:
                transcript_data = response.json()
                with open("QuickMeetTest.json", "w", encoding="utf-8") as file:
                    json.dump(transcript_data, file, indent=2)
                print("Transcript downloaded and saved as QuickMeetTest.json")
            else:
                print("Failed to download the transcript JSON.")
    else:
        print("There was an error processing the transcription job.")

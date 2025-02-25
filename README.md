# Meeting Assistant

This application helps transcribe meeting recordings, generate summaries, extract action items, and create video summaries using AI. It features semantic search capabilities for finding previous meetings.

## Features

- Audio/video recording transcription using AWS Transcribe
- Meeting summary generation using Hugging Face models
- Action item extraction using NLP
- Video summary creation with HeyGen API
- Semantic search using Weaviate vector store
- Modern, responsive UI with Vue.js and Tailwind CSS

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
FLASK_SECRET_KEY=your-secret-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=us-west-2
S3_BUCKET=your-bucket
WEAVIATE_URL=your-weaviate-url
WEAVIATE_API_KEY=your-weaviate-key
HEYGEN_API_KEY=your-heygen-key
```

3. Run the application:
```bash
python app.py
```

## Usage

1. Upload a meeting recording (audio/video)
2. Wait for processing (transcription, summary, action items)
3. View generated summary and action items
4. Watch AI-generated video summary
5. Use semantic search to find previous meetings

## AWS Free Tier Usage

The application is designed to work within AWS Free Tier limits:
- Amazon Transcribe: 60 minutes free per month
- S3: 5GB storage + limited requests
- Consider implementing usage tracking to stay within limits

## Contributing

Feel free to open issues or submit pull requests for improvements.
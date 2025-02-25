import boto3
from typing import List, Dict

class SentimentAnalyzer:
    def __init__(self):
        """Initialize AWS Comprehend client."""
        self.comprehend = boto3.client('comprehend')

    def analyze_meeting_segments(self, segments: List[Dict]) -> List[Dict]:
        """
        Analyze sentiment for each transcript segment.

        Args:
            segments: List of transcript segments with topics.

        Returns:
            List of sentiment analysis results.
        """
        analyzed_segments = []
        for segment in segments:
            sentiment_result = self._analyze_sentiment(segment['content'])
            analyzed_segments.append({
                'topic': segment['topic'],
                'sentiment': sentiment_result['Sentiment'],
                'confidence': sentiment_result['SentimentScore']
            })
        return analyzed_segments

    def _analyze_sentiment(self, text: str) -> Dict:
        """
        Use AWS Comprehend to analyze sentiment.

        Args:
            text: Text content.

        Returns:
            Sentiment analysis result.
        """
        try:
            response = self.comprehend.detect_sentiment(Text=text, LanguageCode='en')
            return response
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {'Sentiment': 'NEUTRAL', 'SentimentScore': {}}

    def get_overall_sentiment(self, sentiment_results: List[Dict]) -> Dict:
        """
        Compute the overall sentiment of the meeting.

        Args:
            sentiment_results: List of sentiment scores per segment.

        Returns:
            Overall sentiment summary.
        """
        sentiment_counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0, 'MIXED': 0}

        for result in sentiment_results:
            sentiment_counts[result['sentiment']] += 1

        overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)

        return {
            'overall_sentiment': overall_sentiment,
            'detailed_count': sentiment_counts
        }

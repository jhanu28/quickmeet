import boto3
import os
import html
import logging
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        """Initialize AWS SES client"""
        self.ses_client = boto3.client('ses',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.sender_email = os.getenv('SENDER_EMAIL')

        if not self.sender_email:
            raise ValueError("❌ Missing required environment variable: SENDER_EMAIL")

    def send_meeting_summary(self, recipient_email, meeting_data):
        """
        Send meeting summary via email using AWS SES
        """
        try:
            msg = MIMEMultipart()
            msg['Subject'] = f"Meeting Summary - {meeting_data.get('meeting_id', 'Unknown')}"
            msg['From'] = self.sender_email
            msg['To'] = recipient_email

            # Generate the HTML email body
            html_content = self._create_email_template(meeting_data)
            msg.attach(MIMEText(html_content, 'html'))

            # Send the email
            response = self.ses_client.send_raw_email(
                Source=self.sender_email,
                Destinations=[recipient_email],
                RawMessage={'Data': msg.as_string()}
            )

            message_id = response['MessageId']
            logger.info(f"✅ Email sent successfully! Message ID: {message_id}")
            return message_id

        except ClientError as e:
            error_message = e.response['Error']['Message']
            logger.error(f"❌ Error sending email: {error_message}")
            raise RuntimeError(f"Email sending failed: {error_message}")

    def _create_email_template(self, meeting_data):
        """
        Create HTML email template for meeting summary
        Uses HTML escaping to prevent potential security issues.
        """
        summary = html.escape(meeting_data.get('summary', 'No summary available.'))
        sentiment = html.escape(meeting_data.get('sentiment', 'Not available'))
        meeting_url = html.escape(meeting_data.get('meeting_url', '#'))

        topics_list = "".join(f'<li>{html.escape(topic)}</li>' for topic in meeting_data.get('topics', ['No topics available.']))
        action_items_list = "".join(f'<li>{html.escape(item)}</li>' for item in meeting_data.get('action_items', ['No action items available.']))

        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h1 style="color: #007BFF;">Meeting Summary</h1>
                <h2>Overview</h2>
                <p>{summary}</p>
                
                <h2>Key Topics</h2>
                <ul>{topics_list}</ul>
                
                <h2>Action Items</h2>
                <ul>{action_items_list}</ul>
                
                <h2>Sentiment Analysis</h2>
                <p><strong>Overall meeting sentiment:</strong> {sentiment}</p>
                
                <p style="margin-top: 20px; font-size: 14px; color: #666;">
                    <a href="{meeting_url}" style="color: #007BFF;">View Full Transcript</a>
                </p>
            </body>
        </html>
        """


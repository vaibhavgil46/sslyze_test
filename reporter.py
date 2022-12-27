import os
import boto3
import datetime

def send_report(recipients, attachment_file, region_name):
    # Set the AWS credentials as environment variables
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Set the email parameters
    sender = "sslyze@noc.webscoot.io"
    domain = os.getenv('DOMAIN')
    subject = f"SSL info about Domain {domain} on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    body_text = f"Hi Team,\n\nPlease find the SSL report for the {domain} attached with this email.\n\nRegards,\nThe Serverless Guy"

    # Read the attachment file
    with open(attachment_file, "rb") as file:
        attachment = file.read()

    # Create an SES client
    client = boto3.client('ses', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=region_name)
    # Send the email
    response = client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': recipients,
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': body_text,
                    'Charset': 'utf-8'
                },
            },
        },
        Attachments=[
            {
                'Filename': attachment_file,
                'Content': attachment,
                'ContentType': 'application/x-yaml'
            },
        ]
    )

    print(response)

# Example usage of the send_report function
send_report(["ad@webscoot.io", "tech@webscoot.io"], "report.yaml", "ap-south-1")

import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime

def send_report(recipients, attachment_file, region_name, domain):
    # Set the AWS credentials as environment variables
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Set the email parameters
    sender = "sslyze@noc.webscoot.io"
    subject = f"SSL info about Domain {domain} on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    body_text = f"Hi Team,\n\nPlease find the SSL report for the {domain} attached with this email.\n\nRegards,\nThe Serverless Guy"

    # Read the attachment file
    with open(attachment_file, "rb") as file:
        attachment = file.read()

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=region_name, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    CHARSET = "utf-8"
    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(body_text.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(body_text.encode(CHARSET), 'html', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Define the attachment part and
    # Encode the attachment file using MIMEApplication.
    att = MIMEApplication(open(attachment_file, 'rb').read())

# Add a header to tell the email client to treat this part as an attachment,
# and to give the attachment a name.
    att.add_header('Content-Disposition','attachment',filename=os.path.basename(attachment_file))

# Attach the multipart/alternative child container to the multipart/mixed
# parent container.
    msg.attach(msg_body)

   # Add the attachment to the parent container.
    msg.attach(att)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_raw_email(
            Source=sender,
            Destinations=[recipients],
            RawMessage={'Data':msg.as_string()},
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

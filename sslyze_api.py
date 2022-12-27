import sys
import os
from sslyze import ServerScanRequest
from sslyze import ServerNetworkLocation
from sslyze import Scanner
from sslyze import ServerHostnameCouldNotBeResolved
from sslyze import ServerScanStatusEnum
from sslyze import SslyzeOutputAsJson
from sslyze import ServerScanResultAsJson
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import json
import yaml
from libary import send_report
# variables
send_report(["ad@webscoot.io", "tech@webscoot.io"], "report.yaml", "ap-south-1")

DOMAIN = os.getenv("DOMAIN")
EMAIL = os.getenv("EMAIL")
TYPE = os.getenv("TYPE")

def json_to_yaml():
    with open("report.json", "r") as f:
        json_data = json.load(f)

    # convert the JSON data to a YAML string
    yaml_data = yaml.safe_dump(json_data)

    # write the YAML string to a file
    with open("report.yaml", "w") as f:
        f.write(yaml_data)


def example_json_result_output(
    json_file_out_1,
    all_server_scan_results_1,
    date_scans_started,
    date_scans_completed
) -> None:
    json_output = SslyzeOutputAsJson(
        server_scan_results=[ServerScanResultAsJson.from_orm(result) for result in all_server_scan_results_1],
        invalid_server_strings=[],  # Not needed here - specific to the CLI interface
        date_scans_started=date_scans_started,
        date_scans_completed=date_scans_completed,
    )
    json_output_as_str = json_output.json(sort_keys=True, indent=4, ensure_ascii=True)
    f = open("report.json", "w+")
    f.write(json_output_as_str)
    f.close()


def scan():
    date_scans_started = datetime.utcnow()
    try:
        scan_request = [ServerScanRequest(server_location=ServerNetworkLocation(hostname=DOMAIN))
                        ]
    except ServerHostnameCouldNotBeResolved:
        # Handle bad input ie. invalid hostnames
        print("Error resolving the supplied hostnames")
        return False

    scanner = Scanner()
    scanner.queue_scans(scan_request)
    all_server_scan_results = []
    for result in scanner.get_results():
        all_server_scan_results.append(result)
        if result.scan_status == ServerScanStatusEnum.ERROR_NO_CONNECTIVITY:
            # No we weren't
            print(
                f"\nError: Could not connect to {result.server_location.hostname}:"
                f" {result.connectivity_error_trace}"
            )
            return -1
        assert result.scan_result

    json_file_out = f"api_sample_results.json"
    example_json_result_output(json_file_out, all_server_scan_results, date_scans_started, datetime.utcnow())
    return 1


def send_mail(type_of_file):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "a@gm"
    receiver_email = MAIL
    password = "sad"
    body = f"SSLYZE Report for {DOMAIN} at {datetime.utcnow()}."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Attachment from python"
    message["Bcc"] = receiver_email

    message.attach(MIMEText(body, "plain"))

    filename = f"report.{TYPE}"
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def print_help():
    print('''
            Enter a valid domain name as the argument and you will be mailed a report containing information of its SSL:
            Environment variable for DOMAIN and MAIL are given below:
            -e "DOMAIN=google.com"
            -e "MAIL=temp@gmail.com"

            By default you will receive the report in yaml format if you don't provide the option for it.
            You can also get the file in the json format you can enter the environment variable TYPE for that i.e.
            -e "TYPE=--json"

            If you are executing this script from command line enter domain and mail as arguments while executing.
            for eg: python3 sslyze.py google.com temp@gmail.com --yaml
                  ''')

flag = True
if len(sys.argv) < 2:
    print("Enter a domain name and your mail where you want the report sent. Enter options -h or --help for help:")
    flag = False
elif len(sys.argv) < 3:
    if sys.argv[1] in ("-h", "--help", "--Help"):
        print_help()
    else:
        print("Enter a domain name and your mail where you want the report sent. Enter options -h or --help for help:")
    flag= False
else:
    DOMAIN = str(sys.argv[1])
    MAIL = str(sys.argv[2])
    TYPE = "yaml"
    if len(sys.argv) == 4:
        if sys.argv[3] == "--json":
            TYPE="json"
        elif sys.argv[3] == "--yaml":
            TYPE="yaml"
        else:
            flag= False

    if sys.argv[2] in ("-h", "--help", "--Help") or flag == False:
        print_help()
    else:
        flag = scan()
        if flag == True:
            json_to_yaml()
            send_mail(TYPE)
        else:
            print("Enter options -h or --help for help")

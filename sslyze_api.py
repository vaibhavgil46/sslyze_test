import os
from sslyze import ServerScanRequest
from sslyze import ServerNetworkLocation
from sslyze import Scanner
from sslyze import ServerHostnameCouldNotBeResolved
from sslyze import ServerScanStatusEnum
from sslyze import SslyzeOutputAsJson
from sslyze import ServerScanResultAsJson
from libary import reporter
from datetime import datetime
import json
import yaml

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
            return False
        assert result.scan_result

    json_file_out = f"api_sample_results.json"
    example_json_result_output(json_file_out, all_server_scan_results, date_scans_started, datetime.utcnow())
    return 1


def print_help():
    print('''
            Enter a valid domain name as the argument and you will be mailed a report containing information of its SSL:
            Environment variable for DOMAIN and MAIL are given below:
            -e "DOMAIN=google.com"
            -e "EMAIL=temp@gmail.com"

            By default you will receive the report in yaml format if you don't provide the option for it.
            You can also get the file in the json format you can enter the environment variable TYPE for that i.e.
            -e "TYPE=--json"

            If you are executing this script from command line enter domain and mail as arguments while executing.
            for eg: python3 sslyze_api.py -e DOMAIN=avgh -e EMAIL=temp@gmail.com -e TYPE=--json
                  ''')


flag = True

if DOMAIN in ('-h',None) or EMAIL in ('-h',None):
    print_help()
    flag = False

if flag == True:
    flag = scan()

if flag == True:
    if TYPE == '--yaml':
        json_to_yaml()
        reporter.send_report(EMAIL, "report.yaml", "ap-south-1", DOMAIN)
    elif TYPE == 'json':
        reporter.send_report(EMAIL, "report.json", "ap-south-1", DOMAIN)
    else:
        print_help()


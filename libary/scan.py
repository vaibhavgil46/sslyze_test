from sslyze import ServerScanRequest
from sslyze import ServerNetworkLocation
from sslyze import Scanner
from sslyze import ServerHostnameCouldNotBeResolved
from sslyze import ServerScanStatusEnum
from sslyze import SslyzeOutputAsJson
from sslyze import ServerScanResultAsJson
from datetime import datetime




def json_result_output(
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


def scan(DOMAIN):
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
            print(
                f"\nError: Could not connect to {result.server_location.hostname}:"
                f" {result.connectivity_error_trace}"
            )
            return False
        assert result.scan_result

    json_file_out = f"api_sample_results.json"
    json_result_output(json_file_out, all_server_scan_results, date_scans_started, datetime.utcnow())
    return True
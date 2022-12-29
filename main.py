import os
from libary import scan
from libary import reporter
from libary import convert
from libary import help


#variables
DOMAIN = os.getenv("DOMAIN")
EMAIL = os.getenv("EMAIL")
TYPE = os.getenv("TYPE")


flag = True

if DOMAIN in ('-h',None) or EMAIL in ('-h',None):
    help.print_help()
    flag = False

if flag == True:
    flag = scan.scan(DOMAIN)

if flag == True:
    if TYPE == 'yaml':
        convert.json_to_yaml()
        reporter.send_report(EMAIL, "report.yaml", "ap-south-1", DOMAIN)
    elif TYPE == 'json':
        reporter.send_report(EMAIL, "report.json", "ap-south-1", DOMAIN)
    else:
        help.print_help()
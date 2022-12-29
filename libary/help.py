def print_help():
    print('''
            Enter a valid domain name as the argument and you will be mailed a report containing information of its SSL:
            Environment variable for DOMAIN and MAIL are given below:
            -e "DOMAIN=google.com"
            -e "EMAIL=temp@gmail.com"

            By default you will receive the report in yaml format if you don't provide the option for it.
            You can also get the file in the json format you can enter the environment variable TYPE for that i.e.
            -e "TYPE=json"

            If you are executing this script from command line enter domain and mail as arguments while executing.
            for eg: python3 sslyze_api.py -e DOMAIN=google.com -e EMAIL=temp@gmail.com -e TYPE=json
                  ''')
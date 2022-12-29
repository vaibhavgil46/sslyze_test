import json
import yaml


def json_to_yaml():
    with open("report.json", "r") as f:
        json_data = json.load(f)

    # convert the JSON data to a YAML string
    yaml_data = yaml.safe_dump(json_data)

    # write the YAML string to a file
    with open("report.yaml", "w") as f:
        f.write(yaml_data)
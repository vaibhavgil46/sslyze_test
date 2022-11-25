#!/usr/bin/env python3
import yaml, json, sys
sys.stdout.write(yaml.dump(json.load(sys.stdin),sort_keys=False))

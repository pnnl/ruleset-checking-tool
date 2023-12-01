import json
import os


def deserialize_rpd_file(rpd_file):
    with open(rpd_file) as f:
        if f:
            data = json.load(f)
            return data
        else:
            return None
    return None

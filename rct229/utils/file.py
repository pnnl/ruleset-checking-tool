import json
import os


def deserialize_rpd_file(rpd_file):
    # with open(file_name) as f:
    if rpd_file:
        data = json.load(rpd_file)

        return data

    else:
        return None

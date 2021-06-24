import json
import os


def deserialize_rmr_file(rmr_file):
    # with open(file_name) as f:
    if rmr_file:
        data = json.load(rmr_file)

        return data

    else:
        return None

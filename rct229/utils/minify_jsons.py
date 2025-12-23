import os
import json


def minify_json_file(file_path):
    """
    Minifies a JSON file in place
    Parameters
    ----------
    file_path: str the file path

    Returns
    -------

    """
    # Step 1. If the json file name ends with _master, remove it
    if file_path.endswith("_master.json"):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Could not remove {file_path}: {e}")
    else:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            with open(file_path, "w") as f:
                json.dump(data, f, separators=(",", ":"))
            print(f"Minified: {file_path}")
        except Exception as e:
            print(f"Failed to minify {file_path}: {e}")


def recursively_minify_json_files(directory):
    """
    Recursively traverses the directory and minifiles all JSON files.
    Parameters
    ----------
    directory

    Returns
    -------

    """
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                minify_json_file(file_path)


def main():
    # Get the directory of the current script
    utils_directory = os.path.dirname(os.path.abspath(__file__))
    # Navigate up two levels to get to the `rct229` directory
    project_directory = os.path.abspath(
        os.path.join(utils_directory, os.pardir, os.pardir)
    )
    # Start the minification process
    recursively_minify_json_files(project_directory)


if __name__ == "__main__":
    main()

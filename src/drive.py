# drive.py

import json
import os

class Drive:
    @staticmethod
    def write_to_json(file_path, data):
        """
        Writes the given data to a JSON file.
        :param file_path: The path where the JSON file will be saved.
        :param data: The data to write to the JSON file.
        """
        try:
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Data successfully written to {file_path}")
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")

    @staticmethod
    def read_from_json(file_path):
        """
        Reads data from a JSON file.
        :param file_path: The path of the JSON file to read.
        :return: The data read from the JSON file, or None if an error occurs.
        """
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist.")
            return None
        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                print(f"Data successfully read from {file_path}")
                return data
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"An error occurred while decoding JSON data: {e}")
            return None

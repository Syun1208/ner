import yaml
import json
from typing import Dict, Any


def load_yaml(file_path: str):
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return None
    


def load_json(path) -> Dict[str, Any]:
    with open(path, 'r', encoding="utf-8") as json_file:
        documents = json.load(json_file)
    return documents



def to_json(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving JSON file {path}: {e}")
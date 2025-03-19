import yaml
def load_yaml(file_path: str):
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return None
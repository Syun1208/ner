import yaml
import json
from datetime import datetime, timedelta
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
        
        
def get_current_year() -> str:
    """
    Get the current year in YYYY format.
    
    Returns:
        str: Current year in YYYY format
    """
    return datetime.now().strftime("%Y")



def get_current_datetime() -> str:
    """
    Get the current datetime in YYYY-MM-DD format.
    
    Returns:
        str: Current date in YYYY-MM-DD format
    """
    return datetime.now().strftime("%Y-%m-%d")



def get_current_month() -> str:
    """
    Get the current month in MM format.
    
    Returns:
        str: Current month in MM format
    """
    return datetime.now().strftime("%m")

def get_current_day() -> str:
    """
    Get the current day in DD format.
    
    Returns:
        str: Current day in DD format
    """
    return datetime.now().strftime("%d")


def get_current_previous_date() -> str:
    """
    Get the previous date in DD format.
    
    Returns:
        str: Previous date in DD format
    """
    return (datetime.now() - timedelta(days=1)).strftime("%d")

def get_last_week_dates() -> tuple[str, str]:
    """
    Get the dates from 7 days ago to today in DD/MM/YYYY format.
    
    Returns:
        tuple[str, str]: A tuple containing (seven_days_ago, today) in DD/MM/YYYY format
    """
    # Get current date
    current_date = datetime.now()
    
    # Get date from 7 days ago
    seven_days_ago = current_date - timedelta(days=7)
    
    # Format dates as DD/MM/YYYY
    from_date = seven_days_ago.strftime("%d/%m/%Y")
    to_date = current_date.strftime("%d/%m/%Y")
    
    return from_date, to_date

def format_entities_for_prompt(entities: Dict[str, str]) -> str:
    """
    Converts a dictionary of entities into a formatted string representation.
    
    Args:
        entities: Dictionary containing entity key-value pairs
        
    Returns:
        Formatted string with entities listed in bullet points
    """
    formatted_str = ""
    for key, value in entities.items():
        # Convert snake_case to Title Case
        formatted_key = " ".join(word.capitalize() for word in key.split('_'))
        formatted_str += f"- {formatted_key}: '{value}'\n"
    return formatted_str.rstrip()
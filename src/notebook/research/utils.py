import re
import json



def filter_special_characters(text):
    """
    Removes special characters like ?.,@#$%!^&*({}|":~`) from the input text.
    
    Args:
        text (str): The input string to be filtered.
    
    Returns:
        str: The filtered string with special characters removed.
    """
    return re.sub(r'[?.,@#$%!^&*({}|":~`)]', '', text)


def filter_possessive_suffix(text):
    """
    Removes possessive suffix ('s) from words like "C890's" and returns "C890".
    
    Args:
        text (str): The input string to be filtered.
    
    Returns:
        str: The filtered string with possessive suffix removed.
    """
    return re.sub(r"(\w+)'s", r"\1", text)


def reformat_data4ner(data):
    
    reformated_data = []
    
    for d in data:
        
        d['query'] = filter_special_characters(d['query'])
        d['query'] = filter_possessive_suffix(d['query'])
        tokenized_text = d['query'].strip().split(' ')
   
        entities = d['entities']
        ner = []
        for e in entities:
            
            label = e['label']
            entity = e['entity'].strip().split(' ')

            if len(entity) >= 2:
                start_index = tokenized_text.index(entity[0])
                end_index = tokenized_text.index(entity[-1])
            else:
                start_index = tokenized_text.index(entity[0])
                end_index = start_index
                
            ner.append([
                start_index,
                end_index,
                label
            ])
            
        reformated_data.append({
            'tokenized_text': tokenized_text,
            'ner': ner
        })

    return reformated_data


def save_json(data, file_path):
    """
    Saves a Python object as a JSON file.

    Args:
        data (object): The Python object to save (e.g., list, dict).
        file_path (str): The file path where the JSON file will be saved.

    Returns:
        None
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data successfully saved to {file_path}")
    

def load_json(file_path):
    """
    Loads a JSON file and returns its content as a Python object.

    Args:
        file_path (str): The file path of the JSON file to load.

    Returns:
        object: The Python object representing the JSON file content.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
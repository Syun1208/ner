import requests
import json
from typing import Dict, Any
import tqdm

from info import PRODUCT, PRODUCT_DETAIL, USER, LEVEL
from prompting import ALPHA_QUERY_SYSTEM_PROMPT, get_alpha_query_user_prompt, get_scenario_prompt
from format_schema import ner_schema, scenario_schema


def create_json_prompt_for_synthetic_data(**kwargs):
    
    # Use dictionary comprehension to filter out 'n/a' values and to keep the code flexible
    attributes = {key: value for key, value in kwargs.items() if value != "n/a"}
    
    # Building the initial part of the prompt
    prompt = """
    **Objective:**
    Produce realistic text passages that include clearly identified named entities. Each entity should be meticulously labeled according to its type for straightforward extraction.

    **Format Requirements:**
    - The output should be formatted in JSON, containing the text and the corresponding entities list.
    - Each entity in the text should be accurately marked and annotated in the 'entities' list.
    - Meticulously follow all the listed attributes.

    **Entity Annotation Details:**
    - All entity types must be in lowercase. For example, use "type" not "TYPE".
    - Entity types can be multiwords separate by space. For instance, use "entity type" rather than "entity_type".
    - Entities spans can be nested within other entities.
    - A single entity may be associated with multiple types. list them in the key "types".

    **Output Schema:**

    <start attribute_1="value1" attribute_2="value2" ...>
    {
    "text": "{text content}",
    "entities": [
        {"entity": "entity name", "types": ["type 1", "type 2", ...]},
        ...
    ]
    }
    <end>

    **Here are some real world examples**:"""

    # Create a string of attributes for the <start> tag, excluding any 'n/a' values
    attributes_string = " ".join([f'{key}="{value}"' for key, value in attributes.items()])

    # Adding the dynamically created attributes string to the prompt
    prompt += f"""
    <start {attributes_string}>
    """

    return prompt


def generate_data(
    user_prompt: str,
    system_prompt: str,
    format_schema: Dict[str, Any],
    api: str = 'https://saillm.oneops.net/api/chat',
    model: str = "qwen2.5:14b"
) -> Dict[str, str]:
    
    headers = {
      "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]


    data = {
        "model": model,
        "messages": messages,
        "format": format_schema,
        "stream": False
    }

    response = requests.post(api, headers=headers, json=data, timeout=600)


    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}: {response.text}")

    response_data = response.json()
    

    if 'message' not in response_data or 'content' not in response_data['message']:
        raise Exception("Unexpected response format")

    return json.loads(response_data['message']['content'])


def save_json(
    data: Dict, 
    file_path: str
) -> None:
    """
    Save a dictionary as a JSON file.

    Args:
        data (Dict): The data to save.
        file_path (str): The path to the file where the JSON will be saved.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        # print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving JSON: {e}")


def generate_data4ner() -> None:
    
    total_iterations = len(PRODUCT) * len(PRODUCT_DETAIL) * len(USER) * len(LEVEL)
    dataset = []
    with tqdm.tqdm(total=total_iterations, desc="Generating NER Data", unit="iteration") as pbar:
        for p in PRODUCT:
            for pde in PRODUCT_DETAIL:
                for u in USER:
                    for l in LEVEL:
                        keywords = {
                            'product': p,
                            'product_detail': pde,
                            'user': u,
                            'level': l
                        }

                        ALPHA_QUERY_USER_PROMPT = get_alpha_query_user_prompt(**keywords)
                        
                        data = generate_data(
                            user_prompt=ALPHA_QUERY_USER_PROMPT,
                            system_prompt=ALPHA_QUERY_SYSTEM_PROMPT,
                            format_schema=ner_schema,
                            model="qwen2.5:14b",
                            api='http://0.0.0.0:8090/api/chat'
                        )
                        dataset.append(data)
                        save_json(data=dataset, file_path='./arb_datasets.json')

                        pbar.update(1)
       
       
def generate_data4scenario() -> None: 
    
    user_prompt, system_prompt = get_scenario_prompt()
    times = 10
    dataset = []
    with tqdm.tqdm(total=times, desc="Generating Scenario", unit="iteration") as pbar:
        
        for _ in range(times):
            data = generate_data(
                user_prompt=user_prompt,
                system_prompt=system_prompt,
                format_schema=scenario_schema,
                model="qwen2.5:14b",
                api = 'https://saillm.oneops.net/api/chat',
            )
            dataset.append(data)
            save_json(data=dataset, file_path='./scenario_datasets.json')
    
    
if __name__ == "__main__":
    # generate_data4ner()
    generate_data4scenario()
    
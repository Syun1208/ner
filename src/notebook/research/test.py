import re
from info import *

test_str = "I want to product SportsBook and product detail SABA Basketball only"

def filter_by_label(query, label):
    list_index = []
    for l in label:
        index_pattern = find_pattern_index(query, l)
        list_index.append(index_pattern)
    return list_index
        

def find_pattern_index(query, entity="SportsBook"):

    splitted_query = query.split(" ")
    if entity in splitted_query:
        index = splitted_query.index(entity)
        pos = [index - 1, index]
        
        return {
            'entity': entity,
            'position': pos 
        }
        
    return {
            'entity': entity,
            'position': [] 
        }

# Example usage
labels = [PRODUCT, PRODUCT, LEVEL, USER]
for label in labels:
    t = filter_by_label(test_str, label=label)
    print(t)

json_string = """[
    {
        "query": "Generate a Win/Loss Detail Report for user ZZZZZ2810 at Direct Member level who participated in Sportsbook under the Sportsbook Product between 01/02/2024 and 15/02/2024.",
        "entities": [
            {"entity": "Sportsbook", "from_index": 19, "to_index": 19, "label": "product"},
            {"entity": "Sportsbook", "from_index": 16, "to_index": 16, "label": "product_detail"},
            {"entity": "01/02/2024 and 15/02/2024", "from_index": 22, "to_index": 24, "label": "date_range"},
            {"entity": "ZZZZZ2810", "from_index": 9, "to_index": 9, "label": "user"},
            {"entity": "Direct Member", "from_index": 13, "to_index": 13, "label": "level"}
        ]
    },
    {
        "query": "Provide a report on Win/Loss for user ZZZZZ2810 categorized under Direct Member level who engaged in Sportsbook within the Sportsbook Product from 01/02/2024 to 15/02/2024.",
        "entities": [
            {"entity": "Sportsbook", "from_index": 20, "to_index": 20, "label": "product"},
            {"entity": "Sportsbook", "from_index": 17, "to_index": 17, "label": "product_detail"},
            {"entity": "01/02/2024 to 15/02/2024", "from_index": 23, "to_index": 25, "label": "date_range"},
            {"entity": "ZZZZZ2810", "from_index": 10, "to_index": 10, "label": "user"},
            {"entity": "Direct Member", "from_index": 14, "to_index": 14, "label": "level"}
        ]
    },
    {
        "query": "Can you fetch a Win/Loss report for ZZZZZ2810, a Direct Member, who was active in the Sportsbook Product with Sportsbook details during 01/02/2024 - 15/02/2024?",
        "entities": [
            {"entity": "Sportsbook", "from_index": 21, "to_index": 21, "label": "product"},
            {"entity": "Sportsbook", "from_index": 18, "to_index": 18, "label": "product_detail"},
            {"entity": "01/02/2024 - 15/02/2024", "from_index": 26, "to_index": 28, "label": "date_range"},
            {"entity": "ZZZZZ2810", "from_index": 11, "to_index": 11, "label": "user"},
            {"entity": "Direct Member", "from_index": 15, "to_index": 15, "label": "level"}
        ]
    }
]"""
ner_schema = {
    "type": "object",
    "properties": {
        "ner_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "entities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "entity": {"type": "string"},
                                "from_index": {"type": "integer"},  
                                "to_index": {"type": "integer"},  
                                "label": {"type": "string"}
                            },
                            "required": ["entity", "from_index", "to_index", "label"]
                        }
                    }
                },
                "required": ["query", "entities"]
            }
        }
    },
    "required": ["ner_data"]
}



synthetic_schema ={
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "entities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "entity": {"type": "string"},
                    "types": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["entity", "types"]
            }
        }
    },
    "required": ["text", "entities"]
}



scenario_schema = {
    "type": "object",
    "properties": {
        "scenario_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "object",
                        "properties": {
                            "api_key": {"type": "string"},
                            "data": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": 'string'},
                                    "query": {"type": "string"}
                                }
                            }
                        }
                    },
                    "output": {
                        "type": "object",
                        "properties": {
                            "status_code": {'type': 'string'},
                            'error_message': {'type': 'string'},
                            'date': {
                                'type': 'object',
                                'properties': {
                                    'user_id' : {'type': 'string'},
                                    'is_new_session': {'type': 'string'},
                                    "is_action": {'type': 'string'}, 
                                    "endpoint": {'type': 'string'},  
                                    'params': {
                                        'type': 'object',
                                        'properties': {
                                            "from_date": {'type': 'string'}, 
                                            "to_date": {'type': 'string'},
                                            "product": {'type': 'string'}, 
                                            "product_detail": {'type': 'string'}, 
                                            "level": {'type': 'string'},
                                            "user": {'type': 'string'}
                                        }
                                    },
                                    "response": {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


ALPHA_QUERY_SYSTEM_PROMPT = """
You are a Named Entity Recognizer and Sentence Generation Agent. 
Your task is to generate sentences that incorporate the given keywords and recognize the entities based on the input from user. 
Treat the keywords as entities and ensure they are contextually relevant and clearly defined within the sentence. 
The sentences should be coherent, grammatically correct, and meaningful, do not need to generate a sentence too long.
"""

def get_alpha_query_user_prompt(**keywords) -> str:
    
    product = keywords['product']
    product_detail = keywords['product_detail']
    user = keywords['user']
    level = keywords['level']
    
    expected_result = """[
        {
            "query": "Generate a Win/Loss Detail Report for user ZZZZZ2810 at Direct Member level who participated in Sportsbook under the Sportsbook Product between 01/02/2024 and 15/02/2024.",
            "entities": [
                {"entity": "Sportsbook", "from_index": 15, "to_index": 15, "label": "product"},
                {"entity": "Sportsbook", "from_index": 18, "to_index": 18, "label": "product_detail"},
                {"entity": "01/02/2024 and 15/02/2024", "from_index": 21, "to_index": 23, "label": "date_range"},
                {"entity": "ZZZZZ2810", "from_index": 7, "to_index": 7, "label": "user"},
                {"entity": "Direct Member", "from_index": 9, "to_index": 10, "label": "level"}
            ]
        },
        {
            "query": "Provide a report on Win/Loss for user ZZZZZ2810 categorized under Direct Member level who engaged in Sportsbook within the Sportsbook Product from 01/02/2024 to 15/02/2024.",
            "entities": [
                {"entity": "Sportsbook", "from_index": 16, "to_index": 16, "label": "product"},
                {"entity": "Sportsbook", "from_index": 19, "to_index": 19, "label": "product_detail"},
                {"entity": "01/02/2024 to 15/02/2024", "from_index": 22, "to_index": 24, "label": "date_range"},
                {"entity": "ZZZZZ2810", "from_index": 7, "to_index": 7, "label": "user"},
                {"entity": "Direct Member", "from_index": 10, "to_index": 11, "label": "level"}
            ]
        },
        {
            "query": "Can you fetch a Win/Loss report for ZZZZZ2810, a Direct Member, who was active in the Sportsbook Product with Sportsbook details during 01/02/2024 - 15/02/2024?",
            "entities": [
                {"entity": "Sportsbook", "from_index": 15, "to_index": 15, "label": "product"},
                {"entity": "Sportsbook", "from_index": 19, "to_index": 19, "label": "product_detail"},
                {"entity": "01/02/2024 - 15/02/2024", "from_index": 22, "to_index": 24, "label": "date_range"},
                {"entity": "ZZZZZ2810", "from_index": 7, "to_index": 7, "label": "user"},
                {"entity": "Direct Member", "from_index": 9, "to_index": 10, "label": "level"}
            ]
        }
    ]"""
    
    explain_output = """

    [
        {
            "query": "<generated sentence>",
            "entities": [
                {"entity": "<entity_value>", "from_index": <start>, "to_index": <end>, "label": "<label>"},
                ...
            ]
        }
    ]
    
    1. query:

        This is the original text query that the user has provided.

    2. entities:

        This is a list of identified entities from the query. Each entity represents a specific piece of information extracted from the query.
        Each object in the list contains the following keys:

            * entity: The actual value of the extracted entity.
            * from_index: The starting position (word index) of the entity in the query splitted by blank spaces.
            * to_index: The ending position (word index) of the entity in the query splitted by blank spaces.
            * label: The category or type of the entity.
            
        For example:
            [
                {
                    "query": "Can you fetch a Win/Loss report for ZZZZZ2810, a Direct Member, who was active in the Sportsbook Product with Sportsbook details during 01/02/2024 - 15/02/2024?",
                    "entities": [
                        {"entity": "Sportsbook", "from_index": 15, "to_index": 15, "label": "product"},
                        {"entity": "Sportsbook", "from_index": 19, "to_index": 19, "label": "product_detail"},
                        {"entity": "01/02/2024 - 15/02/2024", "from_index": 22, "to_index": 24, "label": "date_range"},
                        {"entity": "ZZZZZ2810", "from_index": 7, "to_index": 7, "label": "user"},
                        {"entity": "Direct Member", "from_index": 9, "to_index": 10, "label": "level"}
                    ]
                }
            ]
            
        Explain:
                
                Firstly, you need to split the query based the blank space, that means:
                [
                    "Can", "you", "fetch", "a", "Win/Loss", "report", "for", "ZZZZZ2810,", 
                    "a", "Direct", "Member,", "who", "was", "active", "in", "the", 
                    "Sportsbook", "Product", "with", "Sportsbook", "details", "during", 
                    "01/02/2024", "-", "15/02/2024?"
                ]
                Then, you need to define the index of the given label from the query list. The index must be started at 0.
                
                + {"entity": "Sportsbook", "from_index": 16 "to_index": 16, "label": "product"}

                    "Sportsbook" is recognized as a product.
                    Found at position 16 in the query.

                + {"entity": "Sportsbook", "from_index": 19, "to_index": 19, "label": "product_detail"}

                    "Sportsbook" again, but this time recognized as a product_detail.
                    Found at position 19 in the query.
                    (The difference between product and product_detail depends on the context in which they are used.)

                + {"entity": "01/02/2024 - 15/02/2024", "from_index": 22, "to_index": 24, "label": "date_range"}

                    The date range for which the report is requested.
                    Found at positions from 22 to 24 in the query.

                + {"entity": "ZZZZZ2810", "from_index": 7, "to_index": 7, "label": "user"}

                    "ZZZZZ2810" is recognized as a user ID.
                    Found at position 7 in the query.

                + {"entity": "Direct Member", "from_index": 9, "to_index": 10, "label": "level"}

                    "Direct Member" is identified as the membership level of the user.
                    Found at position from 9 to 10 in the query.
    """
    
    ALPHA_QUERY_USER_PROMPT = f"""
    # Prompt:
    Generate multiple grammatically correct and meaningful sentences using the provided keywords. Ensure that each sentence is coherent and clearly defines the context of the keywords. Additionally, include random date ranges in each sentence to add variety.

    # Keywords:
        - Product: {product}
        - Product Detail: {product_detail}
        - User: {user}
        - Level: {level}

    # Instructions:

        - Naturally incorporate the provided keywords into the sentences.
        - Generate multiple variations while maintaining clarity and correctness.
        - Randomly insert a date range in different formats, such as:
        - Specific Dates: "10/1 to 20/4", "26/06/2021 - 12/08/2022"
        - Relative Dates: "next week", "tomorrow", "last year", "day 10"
        - Ensure the sentences reflect different ways of requesting the same information.
        
    # Defined Entity Types:
        - "date_range": Specifies the report period (e.g., "tomorrow", "last week")
        - "product": The product category being filtered
        - "product_detail": A more specific product category
        - "level": The user level or category for filtering
        - "user": A specific user (if applicable)
    
    # Example Input:
        - Product: Sportsbook
        - Product Detail: Sportsbook
        - User: ZZZZZ2810
        - Level: Direct Member

    # Example Output:
    ```python
    {expected_result}
    ```
    
    # Explain The Structured Output:
    {explain_output}
    """

    return ALPHA_QUERY_USER_PROMPT


def get_scenario_prompt():
    user_prompt = (
        "Generate multiple diverse scenarios where users interact with a report bot "
        "to request win/loss reports and other information. Ensure each scenario "
        "includes a unique user query."
    )

    system_prompt = """
    You are an AI trained to generate structured API interaction scenarios. 
    Your task is to create realistic scenarios where users interact with a reporting bot. 
    The interactions should align with the given API structure, including request and response formats.

    ### Instructions:
    1. Each scenario should have a **unique user query** reflecting different ways users might request information.
    2. The API response should follow this structure:
        - **Input parameters:**
            - `api_key`: a unique identifier (likely a token) used for authentication.
            - `data`: contains the actual request payload with details about the user and their query.
                - `user_id`: a unique identifier for the user making the request.
                - `query`: a textual request describing what the user wants.

        - **Output parameters:**
            - `status_code`: HTTP-style status code indicating the result of the request.
            - `error_message`: provides details about an error if one occurs.
            - `data`: contains the actual response data related to the request.
                - `user_id`: the unique identifier for the user making the request.
                - `is_new_session`: indicates whether this is a new session in the next conversation.
                - `is_action`: a flag determining whether a parameter has been detected from the query.
                - `endpoint`: defines the API endpoint to be used.
                - `params`: contains filters extracted from the user's query:
                    - `from_date`: start date for the report/query.
                    - `to_date`: end date for the report/query.
                    - `product`: specifies the product category to filter by.
                    - `product_detail`: specifies a more detailed product category.
                    - `level`: defines the user level or category for filtering.
                    - `user`: specifies a particular user for filtering (if applicable).
                - `response`: A casual conversational reply from an LLM. If `None`, `is_action` is `True` and `params` is not `None`.

    3. Include different scenarios such as:
        - Users providing partial information and requiring clarification.
        - Users requesting specific details like 'Virtual Sports' or 'SABA Soccer'.
        - Users engaging in casual conversation with the bot.
        - Users asking follow-up questions to refine their queries.

    ### Example Scenarios:

    **Scenario 1: Casual greeting**
    ```json
    {
        "api_key": "nfuibay8175105njknia",
        "data": {
            "user_id": "0827275",
            "query": "Hello bot, how are you today?"
        }
    }
    {
        "status_code": 200,
        "error_message": "",
        "data": {
            "user_id": "0827275",
            "is_new_session": false,
            "is_action": false,
            "endpoint": null,
            "params": null,
            "response": "Hello, I’m Alpha Report Bot. How can I help you?"
        }
    }
    ```

    **Scenario 2: Requesting a Win/Loss Report with missing details**
    ```json
    {
        "api_key": "nfuibay8175105njknia",
        "data": {
            "user_id": "0827275",
            "query": "I want to get a Win/Loss Report, please."
        }
    }
    {
        "status_code": 200,
        "error_message": "",
        "data": {
            "user_id": "0827275",
            "is_new_session": false,
            "is_action": false,
            "endpoint": null,
            "params": null,
            "response": "Could you provide more details such as: From date (Required), To date (Required), Product (Default All), Product Detail (Default All), Level (Default All), User (Optional)?"
        }
    }
    ```

    **Scenario 3: Specific request with full details**
    ```json
    {
        "api_key": "nfuibay8175105njknia",
        "data": {
            "user_id": "0827275",
            "query": "Get me a Win/Loss Detail Report on day 10."
        }
    }
    {
        "status_code": 200,
        "error_message": "",
        "data": {
            "user_id": "0827275",
            "is_new_session": false,
            "is_action": true,
            "endpoint": "/winlost_detail_report",
            "params": {
                "from_date": "2025-03-10",
                "to_date": "2025-03-10",
                "product": "All",
                "product_detail": "All",
                "level": "All",
                "user": null
            },
            "response": null
        }
    }
    ```

    Generate multiple such scenarios with varying complexity and user intent.
    """
    
    return user_prompt, system_prompt

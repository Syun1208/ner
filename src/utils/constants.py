import dataclasses

@dataclasses.dataclass
class Prompt:
    
    FUNCTION_CALLING_SYSTEM_PROMT = """
        Now, User want to do an action. You are a chatbot that helps users perform basic tasks like getting performance report. \
        Based on the user's command, extract the necessary information accurately to fulfill the request. \
        You must automatically infer the time period based on the user's request.\ MUST response by user'language.
        \
        STRICT GUIDELINES (MUST BE FOLLOWED):\
            1. DO NOT ASSUME OR FILL IN MISSING INFORMATION BY YOURSELF. Always ask the user for clarification if any detail is unclear.\
            2. MUST CONFIRM ALL ARGUMENTS OF THE FUNCTION AND THE NEXT ACTION WITH THE USER before executing any function, ensuring the extracted information is correct.\
            3. NO CHANGE FUNCTION NAMES, ONLY SELECT FROM PREDEFINED FUNCTION LIST. You must strictly select function names and their arguments only from the predefined function list. \
                Under no circumstances should you generate, modify, translate, or alter function names or arguments. \
                If an argument is not in the function’s definition, you must rise a warning for user.\
                If a required argument is missing, request it instead of assuming or generating values. \
                Only return the exact function and arguments as defined—no extra parameters, no modifications.\
            4. DO NOT CALL ANY TOOL IF REQUIRED PARAMETERS ARE MISSING. If any required parameter is not provided, ask the user to supply the missing information before proceeding.
        FAILURE TO FOLLOW THESE RULES MAY RESULT IN INCORRECT FUNCTION EXECUTION.\
        \
        IMPORTANT NOTES: \
            1. MUST CONFIRM ALL ARGUMENTS WITH THE USER BEFORE EXECUTING ANY FUNCTION\
        """
                 
    LLM_CONFIRMATION_SYSTEM_PROMPT = """
        You are agent detecting the confirmation from user's query, you need to consistently detect and recognize whether user confirms or not.
        """



@dataclasses.dataclass
class AlphaWinlostInfo:
    
    PRODUCT = [
        "Sportsbook", "Number Game", "Virtual Sports", "Saba Casino", "RNG Keno", "AG Casino",
        "Sportsbook 2", "RNG Slot", "Cricket", "Allbet", "Macau Games", "Cash Out", "Lottery",
        "Voidbrige Jackpot", "Exchange", "PP", "Arcadia Gaming", "SG", "Saba Promotion",
        "Virtual Games", "SA Gaming", "Table Game", "Live Casino", "SABA.games", "Togel 4D",
        "RNG Games", "AE Sexy", "IBCBet Live Casino", "BBIN", "GPI", "WM", "ION", "RNG Casino",
        "Saba Virtual Sports", "PG Soft", "Joker", "BG", "MaxGame", "Habanero", "CG",
        "Sports Lottery", "PP Live Casino", "Vgaming", "AdvantPlay", "AdvantPlay Mini", 
        "Bitcoin", "FGG", "SEAL Entertainment", "MG-RNG", "Player Tips", "Jili", "YeeBet", 
        "UU SLOTS", "Live22", "WE Live Casino", "Saba Coins", "Yolo Play", "Nextspin",
        "SABA xD", "FastSpin", "FA CHAI", "GPI Live Casino", "PLAYSTAR", "HOTDOG", "ON Casino",
        "Smartsoft", "Playtech", "SABA Keno", "ASKMESLOT", "Funky Games"
    ]

    PRODUCT_DETAIL = [
        "SABA Basketball", "SABA Basketball PinGoal", "SABA E-Sports PinGoal",
        "SABA Other Sports", "SABA Soccer", "SABA Soccer PinGoal", "SABA Tennis",
        "Sportsbook", "Allbet Promotion", "PP Jackpot Contribution", "PP Jackpot Prize",
        "SG Jackpot Contribution", "SG Jackpot Prize", "AE Sexy Lucky Draw",
        "Vgaming Promotion Prize", "MG-RNG Promotion Prize", "Live22 Promotion Prize",
        "FastSpin Promotion Prize", "FA CHAI Promotion Prize", "ASKMESLOT Promotion Prize"
    ]

    LEVEL = ['Super Agent', 'Master Agent', 'Agent', 'Direct Member']
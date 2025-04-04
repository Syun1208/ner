import pandas as pd

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

# customer = pd.read_csv(r'/home/hoangtv/Desktop/Long/llm-tuning/data/customer.csv')
customer = pd.read_csv(r'D:\\Desktop\\AlphaReportChatbot\\data\\customer.csv')
USER = customer.dropna()['username'].tolist()
    
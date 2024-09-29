import pandas as pd

def sum_credits(csvFile):
    # read the csv file 
    df = pd.read_csv(csvFile)
    
    # get the sum and fill the nan numbers with 0
    total_credits = df['credits'].fillna(0).sum()
    
    # match case to determine credit rating
    match total_credits:
        case _ if total_credits >= 18:
            return 1
        case _ if total_credits == 17:
            return 2
        case _ if total_credits == 16:
            return 3
        case _ if total_credits == 15:
            return 4
        case _ if total_credits <= 14:
            return 5
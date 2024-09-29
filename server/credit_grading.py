import pandas as pd

def sum_credits(csvFile):
    # read the csv file 
    df = pd.read_csv(csvFile)
    
    # get the sum and skip the Nan values
    total_credits = df['credits'].sum(skipna = True)
    
    # match case to determine credit rating
    match total_credits:
        case _ if total_credits > 18:
            return 1
        case _ if total_credits == 18:
            return 2
        case _ if total_credits == 17:
            return 3
        case _ if total_credits == 16:
            return 4
        case _ if total_credits <= 15:
            return 5
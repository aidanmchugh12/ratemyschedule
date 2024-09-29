import google.generativeai as genai
from dotenv import load_dotenv
import os
import pandas as pd

def createBlurb(finalGrade):
    # get the file paths
    csv_file_path = 'schedule.csv'  
    txt_file_path = 'explaination.txt'  

    # store the program overview in a message variable
    message = """Overview:
    The program is a schedule grader that evaluates a user's course schedule based on certain criteria:
    1. The rmp_grading.py file averages three criteria
        a. The professors current rating out of five (where decimals are allowed)
        b. The difficulty of a certain class with said professor
        c. The 'would take again' percentage in terms of the class with said professor
        This average ends up a number out of 5 and the higher it is the better therefore making the overall letter grade better.

    2. The breaks_grading.py file compares the length of the break between classes with the time it takes to walk to that class (also on a scale of five)
        - The program then subtracts these two values to see the difference between how long you have and how long it'll take you to get to class
        - The program uses the coordinates of the buildings to generate how long it will take to walk between them
        
        rating breakdown:
        difference < 2 is given a 1
        difference < 4 is given a 2
        difference < 6 is given a 3
        difference < 10 is given a 4
        difference >= 10 is given a 5

        example: Benedum Hall to Cathedral of Learning is a 9 minute walk and Lena has 10 minutes between the classes in those two buildings so it would rate it a 1

    The credit_grading.py file give a rating based on the amount of credits you are taking from 12-18
        rating breakdown:
         A 1 is the worst ranking, you have a lot of credits and have a packed schedule.
       A 2 is bad, but better than 1. You have a very tough schedule.
       A 3 is medium difficulty, it's manageable, but could be better.
       A 4 is a good schedule, it's slightly challenging but very possible and balanced.
       A 5 is a perfect schedule, you are taking a very manageable amount of credits.
        
    All three of these components are then combined in the function def get_overall_grade in the app.py file. The following code takes the grade from each of the above criteria and assigns a letter grade based on the value.
    The numbers that total_sum is currently compared to is arbitrary and is just shown to explain how the ratings return a grade of the person's schedule.

    def get_overall_grade(grade1, grade2, grade3):
        total_sum = grade1 + grade2 + grade3
        
        if total_sum >= 13.5:
            return 'A'
        elif total_sum >= 11.5:
            return 'B'
        elif total_sum >= 10.5:
            return 'C'
        elif total_sum >= 8:
            return 'D'
        return 'F'

    Input and Output Structure:

    The user is able to input their schedule as a .ics (that can be downloaded straight from their peopleSoft application) amd the program will convert it to a .csv file to read all the data.
    - this includes: class name, professor, credits, start time, end time, duration of class

    It will output a grade (A,B,C,D,F) based on the grading (out of 5) of all the criteria above. Each of the criteria is given the same weightage so as to ensure there is no human bias towards which criteria "affects" a schedule the most.

    example:
    If a student is taking 18 credits and has a higher walking time than the amount of time their next class starts, they will have a lower schedule grade compared to someone who is taking 12 credits and has longer breaks between classes.
    Also, if a student has a higher amount of credits, but very good professors and another student has a lower amount of credits, then the grade might even out similarly.

    I want you to write out a blurb (Between 100-150 characters) on why a student got a specific grade based on their criteria using data from the CSV to explain it to them.

    """

    # read csv into dataframe
    df = pd.read_csv(csv_file_path)

    # open file in write mode to truncate
    with open('explaination.txt', 'w') as file:
        pass  # clears the files contents

    # combine the explaination and csv data
    csv_data = df.to_string(index=False)  # convert the DataFrame to a string without index
    full_message = f"{message}\n\nCSV Data:\n{csv_data}"
    
    # write the final grade to the message
    final_grade_message = f"The student's final grade was: {finalGrade}. Use the data below to explain this grade.\n"
    full_message += final_grade_message

    # append all the content to the .txt file
    with open(txt_file_path, 'a') as txt_file:  # open in append mode
        txt_file.write(full_message)

    #print(full_message)
    # configure the api
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    # send gemini the txt
    response = model.generate_content(full_message)
    
    return response.text

def creditRating(creditScore):
    # get the file paths
    csv_file_path = 'schedule.csv'  
    txt_file_path = 'explaination.txt'  

    # store the program overview in a message variable
    message = """Overview:
    The program is a schedule grader that evaluates a user's course schedule based on certain criteria:
    The Credit Score being passed is the RATING of the credits, not the AMOUNT of credits being taken.
     The credit_grading.py file give a rating based on the amount of credits you are taking from 12-18
        rating breakdown:
        A 1 is the worst ranking, you have a lot of credits and have a packed schedule.
       A 2 is bad, but better than 1. You have a very tough schedule.
       A 3 is medium difficulty, it's manageable, but could be better.
       A 4 is a good schedule, it's slightly challenging but very possible and balanced.
       A 5 is a perfect schedule, you are taking a very manageable amount of credits.
        
    I want you to write out a blurb (Between 150-300 characters) on why a student got their specific score based on their credits taken.
    Their data is being written to this file, only concern yourself with the amount of credits taken.

    """

    # read csv into dataframe
    df = pd.read_csv(csv_file_path)

    # open file in write mode to truncate
    with open('explaination.txt', 'w') as file:
        pass  # clears the files contents

    # combine the explaination and csv data
    csv_data = df.to_string(index=False)  # convert the DataFrame to a string without index
    full_message = f"{message}\n\nCSV Data:\n{csv_data}"
    
    # write the final grade to the message
    final_grade_message = f"The student's rating for credits taken is: {creditScore}. Use the professor data below to explain this ranking.\n"
    full_message += final_grade_message

    # append all the content to the .txt file
    with open(txt_file_path, 'a') as txt_file:  # open in append mode
        txt_file.write(full_message)

    #print(full_message)
    # configure the api
    genai.configure(api_key='AIzaSyA7zDuJi_5LlvqSsTCzqv-Sj3-Jl1gyixM')
    model = genai.GenerativeModel("gemini-1.5-flash")

    # send gemini the txt
    response = model.generate_content(full_message)
    
    return response.text

def profRating(profScore):
    # get the file paths
    csv_file_path = 'schedule.csv'  
    txt_file_path = 'explaination.txt'  

    # store the program overview in a message variable
    message = """Overview:
    The program is a schedule grader that evaluates a user's course schedule based on certain criteria:
    1. The rmp_grading.py file averages three criteria
        a. The professors current rating out of five (where decimals are allowed)
        b. The difficulty of a certain class with said professor
        c. The 'would take again' percentage in terms of the class with said professor
        This average ends up a number out of 5 and the higher it is the better therefore making the overall letter grade better.
        
    example:
    If a student is taking a professor with a high difficulty ranking, they will have a lower score.
    
    I want you to write out a blurb (Between 150-300 characters) on why a student got their specific score based on their professor taken.
    Their data is being written to this file, only concern yourself with the professor data taken.

    """

    # read csv into dataframe
    df = pd.read_csv(csv_file_path)

    # open file in write mode to truncate
    with open('explaination.txt', 'w') as file:
        pass  # clears the files contents

    # combine the explaination and csv data
    csv_data = df.to_string(index=False)  # convert the DataFrame to a string without index
    full_message = f"{message}\n\nCSV Data:\n{csv_data}"
    
    # write the final grade to the message
    final_grade_message = f"The student's ranking for credits taken is: {profScore}. Use the credit data below to explain this ranking.\n"
    full_message += final_grade_message

    # append all the content to the .txt file
    with open(txt_file_path, 'a') as txt_file:  # open in append mode
        txt_file.write(full_message)

    #print(full_message)
    # configure the api
    genai.configure(api_key='AIzaSyA7zDuJi_5LlvqSsTCzqv-Sj3-Jl1gyixM')
    model = genai.GenerativeModel("gemini-1.5-flash")

    # send gemini the txt
    response = model.generate_content(full_message)
    
    return response.text

def breaksRating(breakScore):
    # get the file paths
    csv_file_path = 'breaks.csv'  
    txt_file_path = 'explaination.txt'  

    # store the program overview in a message variable
    message = """Overview:
    The program is a schedule grader that evaluates a user's course schedule based on certain criteria:
     2. The breaks_grading.py file compares the length of the break between classes with the time it takes to walk to that class (also on a scale of five)
        - The program then subtracts these two values to see the difference between how long you have and how long it'll take you to get to class
        - The program uses the coordinates of the buildings to generate how long it will take to walk between them
        
        rating breakdown:
        difference < 2 is given a 1
        difference < 4 is given a 2
        difference < 6 is given a 3
        difference < 10 is given a 4
        difference >= 10 is given a 5

        example: Benedum Hall to Cathedral of Learning is a 9 minute walk and Lena has 10 minutes between the classes in those two buildings so it would rate it a 1
    
    
    I want you to write out a blurb (Between 150-300 characters) on why a student got their specific score based on the length of their break and time it takes to walk between classes.
    Their data is being written to this file, only concern yourself with the data concerning this metric (breaks).

    """

    # read csv into dataframe
    df = pd.read_csv(csv_file_path)

    # open file in write mode to truncate
    with open('explaination.txt', 'w') as file:
        pass  # clears the files contents

    # combine the explaination and csv data
    csv_data = df.to_string(index=False)  # convert the DataFrame to a string without index
    full_message = f"{message}\n\nCSV Data:\n{csv_data}"
    
    # write the final grade to the message
    final_grade_message = f"The student's ranking for breaks is: {breakScore}. Use the break data below to explain this ranking.\n"
    full_message += final_grade_message

    # append all the content to the .txt file
    with open(txt_file_path, 'a') as txt_file:  # open in append mode
        txt_file.write(full_message)

    #print(full_message)
    # configure the api
    genai.configure(api_key='AIzaSyA7zDuJi_5LlvqSsTCzqv-Sj3-Jl1gyixM')
    model = genai.GenerativeModel("gemini-1.5-flash")

    # send gemini the txt
    response = model.generate_content(full_message)
    
    return response.text
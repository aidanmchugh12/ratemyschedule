import ratemyprofessor

import pandas as pd

def get_prof_grades(profs):
    profGradeSum = 0
    
    for p in profs:
        currentProf = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name("University of Pittsburgh"), p)
        if currentProf is not None:
            profGradeSum += (currentProf.rating + currentProf.difficulty + (currentProf.would_take_again/100 * 5)) / 3

    return round(profGradeSum / len(profs), 1)


def get_final_grade(filePath):
    # read the dataframe but only get the professors column
    df = pd.read_csv(filePath, usecols=['professor'])
    
    profs = []
    
    # loop through the professors and assign their average rating in the column
    for index, professor in enumerate(df['professor']):
        # check if professor has a value and is not nan
        if pd.notna(professor):
            #append professor to profs array
            profs.append(professor)
        else:
            pass
        
    # return a pass to the get_prof_grades function with the array
    return int(get_prof_grades(profs))

    
#print(getProfGrades(["jarret", "ramirez", "bonidie"]))
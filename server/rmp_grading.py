import ratemyprofessor

# professor = ratemyprofessor.get_professor_by_school_and_name(
#     ratemyprofessor.get_school_by_name("University of Pittsburgh"), "Jarret Billingsley")
# if professor is not None:
#     print("%s works in the %s Department of %s." % (professor.name, professor.department, professor.school.name))
#     print("Rating: %s / 5.0" % professor.rating)
#     print("Difficulty: %s / 5.0" % professor.difficulty)
#     print("Total Ratings: %s" % professor.num_ratings)
#     if professor.would_take_again is not None:
#         print(("Would Take Again: %s" % round(professor.would_take_again, 1)) + '%')
#     else:
#         print("Would Take Again: N/A")

def getProfGrades(profs):
    profGradeSum = 0
    
    for p in profs:
        currentProf = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name("University of Pittsburgh"), p)
        if currentProf is not None:
            profGradeSum += (currentProf.rating + currentProf.difficulty + (currentProf.would_take_again/100 * 5)) / 3
            print(currentProf.name)
            print(profGradeSum)

    return round(profGradeSum / len(profs), 1)
    
#print(getProfGrades(["jarret", "ramirez", "bonidie"]))
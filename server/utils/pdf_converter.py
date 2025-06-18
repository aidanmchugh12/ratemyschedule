from PyPDF2 import PdfReader
import json


def convert_to_json(file):
    reader = PdfReader(file)

    schedule_data = []

    course_data_template = {
        "Course" : "",
        "CourseTag" : "",
        "Type" : "",
        "Units" : 0,
        "Instructor" : "",
        "Days" : "",
        "Start" : "",
        "End" : "",
        "Location" : "",
    }


    for page in reader.pages:
        text = page.extract_text()
        lines = text.split('\n')
        prev_line = None
        curr_course_tag = None
        
        for line in lines:
            
            curr_index = len(schedule_data) - 1
            
            # Save course tag from prev line since there is no identifier
            if line.startswith("Section: "):
                curr_course_tag = prev_line
                
            
            # New course found
            if line.startswith("Description:"):
                course_data = course_data_template.copy()
                course_data["Course"] = line.replace("Description:", "")
                course_data["CourseTag"] = curr_course_tag
                schedule_data.append(course_data)
            elif line.startswith("Units:"):
                temp = line.replace("Units: ", "")
                schedule_data[curr_index]["Units"] = int(temp[0])
                
                # If there are no credits, it is a recitation
                if int(temp[0]) != 0:
                    schedule_data[curr_index]["Type"] = "LECTURE"
                    
                    # Instructor is on the same line for some reason, so account for that now
                    schedule_data[curr_index]["Instructor"] = temp.replace(f'{int(temp[0])}Instructor: ', "")
                else:
                    schedule_data[curr_index]["Type"] = "RECITATION"
                    schedule_data[curr_index]["Instructor"] = "N/A"
            elif line.startswith("Days:"):
                schedule_data[curr_index]["Days"] = line.replace("Days: ", "")
            elif line.startswith("Start:"):
                schedule_data[curr_index]["Start"] = line.replace("Start: ", "")
            elif line.startswith("End:"):
                schedule_data[curr_index]["End"] = line.replace("End: ", "")
            elif line.startswith("Room:"):
                schedule_data[curr_index]["Location"] = line.replace("Room: ", "")
                
            prev_line = line
                
    json_data = json.dumps(schedule_data)
        
    return json_data
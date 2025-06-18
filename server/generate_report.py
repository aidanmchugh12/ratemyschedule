import json
from datetime import datetime
from utils.db import pitt_walktimes_collection
from metrics.walking_distance import getWalkTime
from metrics.professors import get_rmp_link
from utils.pdf_converter import convert_to_json
from utils.gemini import get_time_summary, get_credit_summary, get_score


def generate_report(scheduleData, name):
    
    # Make copy of report template
    report = report_template.copy()
    
    # Metadata
    report["reportName"] = name
    report["scheduleData"] = scheduleData
    report["reportDateTime"] = datetime.now()
    
    ############## PROFESSOR METRIC ##############
        
    # grab professor links
    links = get_prof_links(scheduleData)
    classes = get_prof_classes(scheduleData)
    
    report["reportData"]["instructorEval"]["instructorClasses"] = classes
    report["reportData"]["instructorEval"]["instructorLinks"] = links
    report["reportData"]["instructorEval"]["summary"] = "Unfortunately, we aren't able to scrape RateMyProfessor scores at this time unlike our previous version due to TOS restrictions. Here's a link to the professors, so you can see for yourself!"
    
    ############## TIME METRIC ##############
    
    distanceData = get_time_data(scheduleData)
    distanceSummary = get_time_summary(distanceData)
    
    report["reportData"]["timeMetrics"]["data"] = distanceData
    report["reportData"]["timeMetrics"]["summary"] = distanceSummary
    
    
    ############## CREDIT LOAD ##############
    
    credit_data = get_credit_data(scheduleData)
    credit_summary = get_credit_summary(credit_data)

    report["reportData"]["academicRigor"]["creditData"] = credit_data
    report["reportData"]["academicRigor"]["summary"] = credit_summary
    
    
    ############## SCORES ##############
    
    report["reportData"]["scores"]["instructorEvalScore"] = 95
    report["reportData"]["scores"]["timeMetricsScore"] = int(get_score(distanceSummary))
    report["reportData"]["scores"]["academicRigorScore"] = int(get_score(credit_summary))
    
    overall_score = int((report["reportData"]["scores"]["instructorEvalScore"] + report["reportData"]["scores"]["timeMetricsScore"] + report["reportData"]["scores"]["academicRigorScore"]) / 3)
    
    report["reportData"]["scores"]["overallScore"] = overall_score
    
    return report


def get_prof_classes(scheduleData) :
    prof_classes = {}
    
    for item in scheduleData:
        instructor = item.get("Instructor")
        if instructor and instructor != "N/A":
            prof_classes[instructor] = item.get("Course")
            
    #print(prof_classes)
    return prof_classes


def get_prof_links(scheduleData) :
    instructors = set()
    
    for item in scheduleData:
        instructor = item.get("Instructor")
        if instructor and instructor != "N/A":
            instructors.add(instructor)
            
    
    prof_links = {}
    
    for prof in instructors:
        prof_links[prof] = get_rmp_link(prof)
    
    
    return prof_links

def get_credit_data(scheduleData):
    
    # Get total credit load & credits per course type
    
    totalCredits = 0
    credits_per_type = {}
    for item in scheduleData:
        course_type = item["CourseTag"].split(" ")[0]
        credits = int(item["Units"])
        
        if course_type not in credits_per_type:
            credits_per_type[course_type] = credits
        else:
            credits_per_type[course_type] += credits
            
        totalCredits += credits
        
    data = {
        "totalCredits" : totalCredits,
        "creditsPerType" : credits_per_type
    }
    
    return data
    
    
        
            

def get_time_data(scheduleData):
    # Time metrics
    temp_description = {
        "Mo" : [], 
        "Tu": [],
        "We" : [],
        "Th" : [],
        "Fr" : []
        }
    
    schedule = {
        "Mo" : [], 
        "Tu": [],
        "We" : [],
        "Th" : [],
        "Fr" : []
        }
    
    schedule_entry_template = {
        "from" : "",
        "fromCourse" : "",
        "fromStartTime" : "",
        "fromEndTime" : "",
        "to" : "",
        "toCourse" : "",
        "toStartTime" : "",
        "toEndTime" : "",
        "timeBetween" : "",
        "walkTime" : ""
    }
    
    # Break into day by day
    for item in scheduleData:
        #print(type(item), item)
        if "Mo" in item["Days"]:
            temp_description["Mo"].append(item["Location"] + "," + item["Start"] + "," + item["End"] + "," + item["Course"])
        if "Tu" in item["Days"]:
            temp_description["Tu"].append(item["Location"] + "," + item["Start"] + "," + item["End"] + "," + item["Course"])
        if "We" in item["Days"]:
            temp_description["We"].append(item["Location"] + "," + item["Start"] + "," + item["End"] + "," + item["Course"])
        if "Th" in item["Days"]:
            temp_description["Th"].append(item["Location"] + "," + item["Start"] + "," + item["End"] + "," + item["Course"])
        if "Fr" in item["Days"]:
            temp_description["Fr"].append(item["Location"] + "," + item["Start"] + "," + item["End"] + "," + item["Course"])
        
    
    # Sort information in chronological order
    for day, schedules in temp_description.items():
        temp_description[day] = sorted(
            schedules,
            key=lambda x: (datetime.strptime(x.split(",")[1], "%I:%M %p"))
        )
        
    
    # For class in each day, find the time between the current and previous class
    for day, classes in temp_description.items():
        for i, entry in enumerate(classes):
            if i != 0:
                # Compute time between
                prev_end_time = datetime.strptime(classes[i-1].split(",")[2], "%I:%M %p")
                curr_start_time = datetime.strptime(classes[i].split(",")[1], "%I:%M %p")
                time_between = int((curr_start_time - prev_end_time).total_seconds() / 60)
                
                
                # Add fields to clean dataset
                schedule_entry = schedule_entry_template.copy()
                schedule_entry["from"] = strip_room(classes[i-1].split(",")[0])
                schedule_entry["fromCourse"] = classes[i-1].split(",")[3]
                schedule_entry["fromStartTime"] = classes[i-1].split(",")[1]
                schedule_entry["fromEndTime"] = classes[i-1].split(",")[2]
                schedule_entry["to"] = strip_room(classes[i].split(",")[0])
                schedule_entry["toCourse"] = classes[i].split(",")[3]
                schedule_entry["toStartTime"] = classes[i].split(",")[1]
                schedule_entry["toEndTime"] = classes[i].split(",")[2]
                schedule_entry["timeBetween"] = time_between
                
                
                # Comput walktime using HERE API
                
                # Check database for existing data first
                exists = walktime_exists(schedule_entry["from"], schedule_entry["to"])
                
                # If data is already stored, use that. If not, compute new data, use it, and store it.
                if exists:
                    schedule_entry["walkTime"] = exists["walkTime"]
                else:
                    #print("getting walktime!")
                    walk_time = getWalkTime(schedule_entry["from"], schedule_entry["to"])
                    schedule_entry["walkTime"] = walk_time
                    
                    new_entry = {
                        "from" : schedule_entry["from"],
                        "to" : schedule_entry["to"],
                        "walkTime" : walk_time
                    }
                    
                    pitt_walktimes_collection.insert_one(new_entry)
                
                
                schedule[day].append(schedule_entry)
    
    return schedule
                
def walktime_exists(from_loc, to_loc):
    query = {
        "$or": [
            {"from": from_loc, "to": to_loc},
            {"from": to_loc, "to": from_loc}
        ]
    }
    return pitt_walktimes_collection.find_one(query)

def strip_room(location):
    # Remove the room number (first word) if present
    return " ".join(location.split(" ")[1:])
                
                
report_template = {
  "reportName": "",
  "reportDateTime": "",
  "scheduleData": {},
  "reportData": {
    "scores": {
      "overallScore": "",
      "timeMetricsScore": "",
      "academicRigorScore": "",
      "instructorEvalScore": "",
      "scoreSummary": ""
    },
    "timeMetrics": {
      "data": {},
      "summary": ""
    },
    "academicRigor": {
      "creditData": "",
      "summary": ""
    },
    "instructorEval": {
      "instructorLinks": {},
      "summary": ""
    },
  }
}


# if __name__ == "__main__":
#     data = json.loads(convert_to_json("./test/Test_Schedule.pdf"))
#     #print(data)
#     #print("########################")
    
#     report = generate_report(data)
#     print(report)
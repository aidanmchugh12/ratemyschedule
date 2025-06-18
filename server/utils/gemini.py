from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=f'{os.getenv("GEMINI_API_KEY")}')


def get_time_summary(data):
    prompt = (
    "Here is a list of class transitions including locations, time between classes, and estimated walking times.\n"
    "Give me a brief summary, highlighting any transitions where walktime is dangerously close or exceeds time between classes.\n"
    "In the summary, consider things like time for lunch, breakfast, and dinner or any concerns about downtime as well.\n"
    "Format the response like the following example:\n\n"
    "EXAMPLE RESPONSE:\n"
    "**Overall Summary:**\n"
    "The schedule appears manageable for most days, with ample time between many classes. Tuesday and Thursday have significant gaps between classes, likely allowing for lunch and downtime. Friday also has a large gap between classes. However, Monday and Wednesday have transitions that require immediate attention.\n\n"
    "**Key Concerns:**\n"
    "*   **Monday:** The transition from '244 Cathedral of Learning' to '404 Information Sciences Build' has only 10 minutes between classes, with an 8-minute walk time. This leaves very little buffer for unexpected delays or getting settled before the next class.\n"
    "*   **Wednesday:** The transition from '244 Cathedral of Learning' to '404 Information Sciences Build' has only 10 minutes between classes, with an 11-minute walk time. This is impossible to make on time.\n\n"
    "**Additional Considerations:**\n"
    "*   **Lunch:** Tuesday and Thursday have a 2 hour and 15 minute gap between classes, which should be sufficient for lunch. Friday has a 1 hour and 10 minute gap between classes, which should be sufficient for lunch. Monday and Wednesday have a 2 hour and 45 minute gap between classes, which should be sufficient for lunch.\n"
    "*   **Breakfast:** The first class on Friday starts at 9:00 am, which should allow time for breakfast.\n"
    "*   **Dinner:** There is no information about classes after 5:00 pm, so it is assumed that there is enough time for dinner.\n\n"
    "**Recommendations:**\n"
    "*   **Prioritize Monday and Wednesday:** The transitions from '244 Cathedral of Learning' to '404 Information Sciences Build' on Monday and Wednesday need to be addressed. Consider contacting the professors to explain the situation and ask for understanding if arriving slightly late. Alternatively, explore options to adjust the schedule if possible.\n"
    "*   **Optimize Walking Routes:** Familiarize yourself with the quickest and most efficient walking routes between buildings to minimize travel time.\n"
    "*   **Be Prepared:** On days with tight transitions, pack your bag strategically the night before, have any necessary materials readily available, and be ready to leave class promptly.\n"
    "*   **Account for Unexpected Delays:** Build in a small buffer for unexpected delays, such as crowded hallways or elevator wait times.\n\n"
    "By addressing the critical transitions and being proactive with time management, the schedule can be managed effectively.\n\n"
    "Now, analyze the following data and provide a response in the same format:\n"
    f"{data}\n"
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            temperature=0.1
        ),
        contents=prompt
        )
    
    return response.text


def get_credit_summary(data):
    prompt = (
        "Here is a summary of a student's course credit load for the semester, broken down by subject area and total credits:\n"
        f"{data}\n\n"
        "Give me a brief summary and analysis of this student's credit distribution. "
        "Highlight whether the total credit load is considered part-time (<12 credits), full-time (12–18 credits), or above the standard full-time range (>18 credits). "
        "Warn if the student is below 12 credits (not full-time), or above 18 credits (written permission required at most universities). "
        "If the student is at the lower end of the full-time range (12–14 credits), suggest considering more classes if appropriate. "
        "If the student is at the higher end (16–18 credits), warn about increased rigor and time commitment. "
        "Comment on the balance between different subject areas and mention any potential concerns or recommendations for workload, major requirements, or opportunities for a more balanced schedule.\n\n"
        "Format the response like the following example:\n\n"
        "EXAMPLE RESPONSE:\n"
        "**Overall Summary:**\n"
        "The student is enrolled in 18 total credits, which is the upper limit for full-time status at most universities. The credit load is distributed across several subject areas, with a heavy emphasis on Computer Science (9 credits), and additional courses in Communication, French, and Information Science.\n\n"
        "**Key Concerns:**\n"
        "*   The total credit load of 18 is considered heavy. Written permission may be required to enroll in more than 18 credits.\n"
        "*   Students taking 16–18 credits should be aware of the increased workload and time commitment required.\n"
        "*   If the student feels overwhelmed, they may consider reducing their course load or ensuring they have adequate support and time management strategies.\n\n"
        "**Additional Considerations:**\n"
        "*   The schedule appears to have a good mix of major and elective courses, but the high number of Computer Science credits may indicate a challenging semester.\n"
        "*   If the student is aiming to graduate on time or early, this credit load may be appropriate, but they should monitor their stress and performance closely.\n"
        "*   If the student is taking only 12–14 credits, they may want to consider adding another class to make better progress toward graduation, if they feel comfortable doing so.\n\n"
        "**Recommendations:**\n"
        "*   Review university policies regarding maximum credit loads and seek written permission if necessary.\n"
        "*   Ensure a balanced schedule and avoid overloading on difficult courses in a single semester.\n"
        "*   Seek academic advising if unsure about course selection or workload.\n\n"
        "Now, analyze the following data and provide a response in the same format:\n"
        f"{data}\n"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            temperature=0.1
        ),
        contents=prompt
    )
    return response.text

def get_score(data):
    prompt = (
        "Based on the given summary and data, output only a numerical score from 0 to 100 that serves as a grade for that data."
        "If there is no concerns, give the student a 100. If there are concerns, it is up to you're judgement on what the score should be."
        "Now, analyze the given data and output ONLY a number from 0 to 100:"
        f'{data}'
    )
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            temperature=0.1
        ),
        contents=prompt
    )
    return response.text

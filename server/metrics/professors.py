# Returns a link to a search page with the professor
def get_rmp_link(professor):
    professor = professor.replace(" ", "%20")
    return f'https://www.ratemyprofessors.com/search/professors/1247?q={professor}'

# Unfortunately, there is no good way to scrape or use an API to get RMP information. 
# Rely on other metrics or simply include a link for professors
import requests
from bs4 import BeautifulSoup

# TODO
# 1. JSON Structure, serialize
# 2. DRIs

URL = "https://pub-calgary.escribemeetings.com/Meeting.aspx?Id=9a27aea6-df27-4322-907f-164396fcf3b0&Agenda=PostMinutes&lang=English"
page = requests.get(URL)

# Complete HTML File
soup = BeautifulSoup(page.content, "html.parser")

# Most of the page content is found in this container
page_content = soup.find(id="package-container")

# MM Header
agenda_header = page_content.find("header", class_="AgendaHeader")

# MM Body
agenda_items = page_content.find_all("div", class_="AgendaItems")



## Header information

# Get the Agenda Header
agenda_header_subtitle = agenda_header.find("p", class_="AgendaHeaderSubTitle").text

# Get the start time
start_time = agenda_header.find("time").text

# Get the location
location = agenda_header_subtitle = agenda_header.find("div", class_="Value LocationValue").text ### Does this get all location info?

attendance_table = agenda_header.find("div", class_="AgendaHeaderAttendanceTable").find_all("div")

# Get the attendence (seperated by who can and can't vote)
present = [x.text for x in attendance_table[2].find_all("li")]
also_present = [x.text for x in attendance_table[5].find_all("li")]
import requests
from bs4 import BeautifulSoup

# REQUIREMENTS: https://pixeltree.notion.site/City-Council-Scraping-34a2f5a24d59400faf9a128f2653ebf2
# Meeting Minutes Directory: https://pub-calgary.escribemeetings.com

# TODO
# 1. JSON Structure, serialize
# 2. Complete the rest of the fields
# 3. Classify using spaCy

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

## Body information

### Code to collect:
# - list of all the motions
#     - title of the motion
#     - who it was moved by
#     - other details
#     - whether or not the motion was carried
#     - links to any attachments

# Select the section of the HTML with the meeting details
section_1= soup.select('div.AgendaItems > div.AgendaItemContainer')

# Create nested dictionary
Result = defaultdict(dict)

# Iterate through page HTML to extract information
for i, each_section in enumerate(section_1):
    
    # For items without sub motions
    if each_section.findChildren('div', class_="AgendaItemContainer") == []:   
        # Extract title of motion
        Result[i]['Title of motion'] = [each_section.find('a').text]
        # Extract Moved by
        Result[i]['Moved by'] = [x.get_text() for x in each_section.select('div.MovedBy > span.Value')] #.find('div', class_='MovedBy').find('span', class_='Value')
        # Extract Details of motion
        Result[i]['Details'] = [x.get_text() for x in each_section.find_all('p')]
        # Extract status of motion (was motion carried?)
        Result[i]['Status of Motion'] = [x.get_text() for x in each_section.select('div.MotionResult')]  #find('div', {'class':"MotionResult"}).text]
        # Get JS item number for attachment link
        attachment_num_list = [re.findall('[0-9]+', x.get('href'))[0] for x in each_section.find_all('a', href=re.compile('attachments'))]
        for num in attachment_num_list:
            attachment_num = num
        # Extract attachment links 
        attachment_list=[]
        for element in set(soup.find_all('div', class_= re.compile('AgendaItemAttachment AgendaItemAttachment'+attachment_num))):    
            attachment_list.append('https://pub-calgary.escribemeetings.com/'+element.find('a')['href'])
        Result[i]['Attachments'] = attachment_list

    # For items with sub motions
    else:
        pass

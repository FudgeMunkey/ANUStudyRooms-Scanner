# Post to https://library-admin.anu.edu.au/book-a-library-group-study-room/index.html

# inp_uid: Uni ID
# inp_passwd: Password

import requests
from bs4 import BeautifulSoup
import datetime
import json
import os

ON_PRODUCTION = True

CRED_PATH = "../secrets/credentials.txt"
URL = "https://library-admin.anu.edu.au/book-a-library-group-study-room/index.html"

BUILDINGS = ["Chifley", "Hancock", "Law", "Menzies"]
DAYS_TO_SCAN = 7

PARAMS_BOOKINGS = {"ajax": 1,
                   "building": "Hancock",
                   "bday": "2019-08-31",
                   "showBookingsForSelectedBuilding": 1}


# Read in the username and password from the secrets file
def createParamLogin():
    try:
        f = open(CRED_PATH, 'r')
    except FileNotFoundError:
        print("Credentials not found, please create the file in root /secrets/credentials.txt with the format UID:PASSWORD")

    contents = ""
    if f.mode == 'r':
        contents = f.read()

    split = contents.split(':')

    loginParams = {"inp_uid": split[0].strip(),
                   "inp_passwd": split[1].strip()}

    return loginParams


# Create the booking params for a building and date
def createParamBookings(building, date):
    bookingParams = {"ajax": 1,
                      "building": building,
                      "bday": date,
                      "showBookingsForSelectedBuilding": 1}

    return bookingParams


# Generate a list of dates in the format: YYYY-MM-DD
def generateDates(num_days):
    date_list = []

    start_date = datetime.datetime.today()

    for n in range(num_days):
        date = start_date + datetime.timedelta(days=n)
        date = date.strftime("%Y-%m-%d")
        date_list.append(date)

    return date_list


# Split 09:00 - 11:00 into 09:00 and 11:00
# merge repeated booking blocks
def cleanTimes(tList):
    cleaned = []

    for tb in tList:
        split = tb.split(" - ")
        start = split[0]
        end = split[1]

        if start not in cleaned:
            cleaned.append(start)
        else:
            cleaned.remove(start)

        if end not in cleaned:
            cleaned.append(end)
        else:
            cleaned.remove(end)

    return cleaned


def outputToFile(out_dict):

    if ON_PRODUCTION:
        BASE = "/var/www/html/"
    else:
        BASE = "../scans/"

    # title = BASE + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    title = BASE + "scan.json"

    out_dict["Scan_End"] = str(datetime.datetime.now())
    print("Scanning Finished: {}".format(out_dict["Scan_End"]))
    out_json = json.dumps(out_dict)

    try:
        os.mkdir(BASE)
        print("Folder created.")
    except FileExistsError:
        print("Folder already exists.")

    f = open(title, "w")
    f.write(out_json)

    return


if __name__ == "__main__":
    # Create the output file
    out = {}
    out["Scan_Start"] = str(datetime.datetime.now())
    print("Scanning at: {}".format(out["Scan_Start"]))

    # Create the session
    s = requests.Session()
    s.post(URL, createParamLogin())  # Log in

    # Loop through each building
    for b in BUILDINGS:
        print("SCANNING Building {}".format(b))
        out[b] = {}
        # Loop through each date
        dates = generateDates(DAYS_TO_SCAN)

        dateDict = {}
        for d in dates:
            # print("Date {}".format(d))
            dateDict[d] = {}
            
            # Generate the POST Parameters
            params = createParamBookings(b, d)

            # Grab the booking page for the building + date
            r = s.post(URL, params)

            # Format the response and look for booking times
            soup = BeautifulSoup(r.content, 'html.parser')
            parentElements = soup.find_all(class_="hideboard")[:-1]

            for e in parentElements:
                # Extract the room name
                roomName = e.get('id').split('-')[0]
                # print(roomName)

                # Extract the booked times
                # Not available: <09:00 - 11:00>
                timeElements = e.find_all(class_="xideboard")
                timeList = []
                for te in timeElements:
                    timeBlock = te.text.split(':', 1)[1][1:-1]
                    timeList.append(timeBlock)

                clean = cleanTimes(timeList)
                dateDict[d][roomName] = clean
                # print(clean)
        out[b] = dateDict
    # pprint.pprint(out)
    outputToFile(out)

'''
ajax	1
building Chifley, Hancock, Law, Menzies
bday	YYYY-MM-DD - 11 DAYS
showBookingsForSelectedBuilding	1

# Grab HTML elements based on class = "hideboard"
# Grab the id of this element and split on '-', take the first one (Room Name)
# Each child div has the not available time for that room
# Split on first ':' and format the times


'''

from datetime import datetime
import email
import smtplib
from http import server

import requests



def create_session(center, session):
    return{"name": center["name"],
           "date":  session["date"],
           "capacity": session["available_capacity"],
           "age_limit": session["min_age_limit"]}
def get_session(data):
    for center in data["centers"]:
        for session in center["sessions"]:
            yield create_session(center,session)

def is_available(session):
    return session["capacity"]>0

def is_for_age(session):
    return session["age_limit"] == 18



def getSlot(start_date):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    params = {"pincode" : your pincode, "date" : start_date.strftime("%d-%m-%Y")}
    headers = {"User-Agent": "Google Chrome/91.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()
    return [session for session in get_session(data) if is_for_age(session) and is_available(session)]

def create_output(session_info):
    return f"{session_info['date']} - {session_info['name']} ({session_info['capacity']})"

print(getSlot(datetime.today()))

content = "\n".join([create_output(session_info) for session_info in getSlot(datetime.today())])
username = "enter your email id"
password = "enter your password "

if not content:
    print("No slots available")
else:
    email_msg = email.message.EmailMessage()
    email_msg["Subject"] = "Vaccination Slot Available"
    email_msg["From"] = username
    email_msg["To"] = username
    email_msg.set_content(content)

    with smtplib.SMTP(host='smtp.gmail.com', port='587') as server:
        server.starttls()
        server.login(username, password)
        server.send_message(email_msg,username,username)

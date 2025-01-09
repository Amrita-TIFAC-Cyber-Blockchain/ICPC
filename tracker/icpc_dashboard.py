'''
Name: ICPC Participants - Codeforces Handle Tracker
Author: Ramaguru Radhakrishnan
Date: 08 Jan 2025
'''

import requests
from flask import Flask, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

# List of student Codeforces handles
student_handles = [
    "ramaguru",
    "sharvesh2709",
    "Mohanvamsi06",
    "Joshua10",
    "akshay789",
    "Govardhan53",
    "Sathwik_18",
    "Haemanth",
    "kavss",
    "ponvedica",
    "rohit-sundar",
    "shobhana_",
    "Shyamraj"
    "soffia_275",
    "ummadimythri",
    "vedha73varshini",
    "tagorenarnenarne"
]

# Function to fetch student info from Codeforces API
def fetch_student_info(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url).json()
    
    if response["status"] == "OK":
        user_data = response["result"][0]
        return {
            "handle": user_data["handle"],
            "rank": user_data.get("rank", "Unrated"),
            "rating": user_data.get("rating", "N/A"),
            "max_rating": user_data.get("maxRating", "N/A"),
            "contrib": user_data.get("contribution", 0),
            "last_online": datetime.utcfromtimestamp(user_data["lastOnlineTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S'),
            "registration_time": datetime.utcfromtimestamp(user_data["registrationTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S')
        }
    return None

# Function to fetch the number of active days in a given timeframe
def fetch_active_days(handle, timeframe):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url).json()
    
    if response["status"] == "OK":
        submissions = response["result"]
        today = datetime.utcnow()
        start_date = today - timedelta(days=timeframe)
        active_days = set()

        for submission in submissions:
            submission_time = datetime.utcfromtimestamp(submission["creationTimeSeconds"])
            if start_date <= submission_time <= today:
                active_days.add(submission_time.date())

        return len(active_days)
    return 0

# Route to display student progress
@app.route('/')
def index():
    students_info = []
    for handle in student_handles:
        student_data = fetch_student_info(handle)
        if student_data:
            student_data["active_days_last_year"] = fetch_active_days(handle, 365)
            student_data["active_days_last_month"] = fetch_active_days(handle, 30)
            students_info.append(student_data)
    
    # Sort students by their rating in descending order
    students_info.sort(key=lambda x: int(x["rating"]) if str(x["rating"]).isdigit() else 0, reverse=True)
    
    return render_template('index.html', students_info=students_info)

if __name__ == "__main__":
    app.run(debug=True)

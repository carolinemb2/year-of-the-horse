"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Soccer Team": {
        "description": "Team practices and competitive matches focused on fitness and teamwork",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 24,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Track and Field": {
        "description": "Running, jumping, and throwing events to build speed and endurance",
        "schedule": "Tuesdays and Thursdays, 3:45 PM - 5:15 PM",
        "max_participants": 28,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore drawing, painting, and mixed media techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and stage performances for school productions",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["amelia@mergington.edu", "ethan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice public speaking and argumentation through structured debates",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["harper@mergington.edu", "james@mergington.edu"]
    },
    "Math Olympiad Club": {
        "description": "Solve advanced math problems and prepare for competitions",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["charlotte@mergington.edu", "benjamin@mergington.edu"]
    },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")



@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

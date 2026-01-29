"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
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
    "Basketball": {
        "description": "Team sport focusing on basketball skills and friendly competitions",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
        "description": "Learn tennis techniques and participate in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["sarah@mergington.edu"]
        },
        "Drama Club": {
        "description": "Perform in theatrical productions and develop acting skills",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["jessica@mergington.edu", "marcus@mergington.edu"]
        },
        "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 18,
        "participants": ["david@mergington.edu"]
        },
        "Debate Team": {
        "description": "Develop argumentation and public speaking skills through debates",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["rachel@mergington.edu", "kevin@mergington.edu"]
        },
        "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu"]
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
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Already signed up")
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


# Unregister endpoint
@app.post("/activities/{activity_name}/unregister")
async def unregister_participant(activity_name: str, request: Request):
    data = await request.json()
    email = data.get("email")
    if activity_name not in activities:
        return JSONResponse(status_code=404, content={"success": False, "error": "Activity not found"})
    activity = activities[activity_name]
    if email not in activity["participants"]:
        return JSONResponse(status_code=404, content={"success": False, "error": "Participant not found"})
    activity["participants"].remove(email)
    return {"success": True}

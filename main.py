from fastapi import FastAPI, HTTPException, Path
import requests
from typing import Dict, Any

app = FastAPI()

# Replace with your Canvas instance URL and access token
CANVAS_API_BASE_URL = "https://dixietech.instructure.com/api/v1"
ACCESS_TOKEN = "2~UuZ2JvFKL77ZwcaBDtfavuLPCaDCTyKG4FXDvCLQH6nJNGKv7x7AMy6nB7yzUUyy"

def get_headers() -> Dict[str, str]:
    """Helper function to get authorization headers."""
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

@app.get("/courses")
async def get_courses():
    """Fetches the list of courses from Canvas."""
    response = requests.get(f"{CANVAS_API_BASE_URL}/courses", headers=get_headers())
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch courses")
    
    return response.json()

@app.get("/courses/{course_id}/assignments")
async def get_assignments(course_id: int = Path(..., title="The ID of the course")):
    """Fetches the list of assignments for a specific course."""
    response = requests.get(f"{CANVAS_API_BASE_URL}/courses/{course_id}/assignments", headers=get_headers())
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch assignments")
    
    return response.json()

@app.post("/courses/{course_id}/assignments/{assignment_id}/submit")
async def submit_assignment(
    course_id: int = Path(..., title="The ID of the course"),
    assignment_id: int = Path(..., title="The ID of the assignment"),
    submission: Dict[str, Any] = None
):
    """Submits an assignment for a specific course and assignment ID."""
    url = f"{CANVAS_API_BASE_URL}/courses/{course_id}/assignments/{assignment_id}/submissions"
    
    response = requests.post(url, headers=get_headers(), json=submission)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to submit assignment")
    
    return response.json()

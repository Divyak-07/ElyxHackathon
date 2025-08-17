# main.py
# This is the simplified backend. The AI /chat endpoint has been removed.
# Its only job is to serve the journey_data.json file.

import json
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# --- Pydantic Models for Data Validation ---
class Tag(BaseModel):
    type: Optional[str] = None
    linked_id: Optional[int] = None

class Message(BaseModel):
    id: int
    timestamp: datetime
    sender: str
    role: str
    content: str
    tags: Tag

class PersonaState(BaseModel):
    before: str
    after: str

class EpisodeAnalysis(BaseModel):
    month_name: str
    primary_goal_trigger: str
    friction_points: List[str]
    final_outcome: str
    persona_analysis: PersonaState

class SentimentPoint(BaseModel):
    month: str
    score: float

class WeeklyReport(BaseModel):
    week_of: str
    summary: str

# --- FastAPI Application Setup ---
app = FastAPI(
    title="Elyx Member Journey API",
    description="An API to serve the 8-month communication log for Rohan Patel's health journey.",
    version="1.0.0"
)

# --- CORS Middleware ---
origins = [
    "null",
    "http://localhost",
    "http://localhost:8080",
    "https://elyxhackathon.netlify.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Loading ---
def load_journey_data() -> List[Message]:
    try:
        with open("journey_data.json", "r") as f:
            data = json.load(f)
            return [Message(**item) for item in data]
    except FileNotFoundError:
        print("ERROR: journey_data.json not found.")
        return []
    except Exception as e:
        print(f"An error occurred loading JSON data: {e}")
        return []

MESSAGES = load_journey_data()

# --- AI Analysis Simulation ---
def get_ai_analysis(month_name: str, messages: List[Message]) -> EpisodeAnalysis:
    pre_written_analyses = {
        "February 2025": {
            "primary_goal_trigger": "Rohan expresses anxiety over an upcoming board presentation, citing dizziness and fatigue. The team makes this a key milestone.",
            "friction_points": ["Rohan notes his Garmin HR zones are wrong.", "He feels the initial Health Optimization Plan is sparse ('mostly headings').", "Impatience over delays in receiving medical records."],
            "final_outcome": "A foundational plan is created, a successful jet-lag experiment is conducted, and a decision is made to upgrade his wearable to a Whoop strap for better data.",
            "persona_analysis": { "before": "Anxious and data-skeptical, questioning the value and speed of the service.", "after": "Becoming more engaged after seeing a tangible win (jet-lag experiment) and a clear path forward (Whoop upgrade)." }
        },
        "May 2025": {
            "primary_goal_trigger": "Rohan wakes up with a sudden viral illness, jeopardizing a major presentation.",
            "friction_points": ["Significant frustration over the setback and feeling that progress is being undone.", "The need to postpone a critical work commitment."],
            "final_outcome": "The Elyx team executes a 'Sick Day Protocol,' managing the illness with data from his wearable, coordinating logistics, and providing a medical letter. Rohan recovers and the team structures his safe return to training.",
            "persona_analysis": { "before": "Feeling confident and seeing consistent progress in his health metrics.", "after": "Frustrated by the setback, but ultimately sees the value of the team's crisis management, making the plan more robust." }
        },
        "August 2025": {
            "primary_goal_trigger": "With a stable health baseline, Rohan shifts his focus to setting long-term, ambitious goals for longevity and peak performance.",
            "friction_points": ["Significant muscle soreness from a new strength program affects his work focus.", "Minor irritation from the Whoop strap requires logistical support."],
            "final_outcome": "Long-term, measurable goals are formalized (e.g., deadlift 1.5x bodyweight). New experiments are run to optimize recovery. Rohan decides to pursue learning piano as a cognitive longevity intervention.",
            "persona_analysis": { "before": "An engaged member focused on optimizing current health metrics.", "after": "A proactive co-manager of his health, thinking in multi-year timelines and integrating health goals (piano) with cognitive performance." }
        }
    }
    if month_name in pre_written_analyses:
        return EpisodeAnalysis(month_name=month_name, **pre_written_analyses[month_name])
    else:
        return EpisodeAnalysis(
            month_name=month_name,
            primary_goal_trigger="Ongoing health optimization and data tracking.",
            friction_points=["General logistical coordination for travel and appointments."],
            final_outcome="Steady progress on established health goals.",
            persona_analysis={ "before": "Following the established plan.", "after": "More integrated and consistent with the established health protocols." }
        )

def get_sentiment_scores() -> List[SentimentPoint]:
    """Simulates an AI sentiment analysis on Rohan's messages."""
    member_messages = [msg for msg in MESSAGES if msg.role == 'Member']
    monthly_scores = {}
    
    for msg in member_messages:
        month = msg.timestamp.strftime('%Y-%m')
        score = 0 # Neutral
        content = msg.content.lower()
        if any(word in content for word in ['good', 'excellent', 'better', 'powerful', 'great', 'successful']):
            score = 1 # Positive
        elif any(word in content for word in ['issue', 'problem', 'anxious', 'frustration', 'setback', 'wrong', 'not heard']):
            score = -1 # Negative
        
        if month not in monthly_scores:
            monthly_scores[month] = []
        monthly_scores[month].append(score)

    sentiment_trend = []
    for month, scores in sorted(monthly_scores.items()):
        avg_score = sum(scores) / len(scores)
        month_str = datetime.strptime(month, '%Y-%m').strftime('%b %Y')
        sentiment_trend.append(SentimentPoint(month=month_str, score=round(avg_score, 2)))
        
    return sentiment_trend

def get_weekly_report(end_date_str: str) -> WeeklyReport:
    """Simulates an AI generating a weekly report for a specific week."""
    # For this demo, we'll return a pre-written report for a specific week in August.
    summary = """
    <ul class='list-disc list-inside space-y-2'>
        <li><span class='font-semibold'>Key Achievement:</span> Successfully managed muscle soreness from the new strength program by implementing a post-workout nutrition protocol (protein/creatine shake). Recovery metrics improved significantly.</li>
        <li><span class='font-semibold'>New Goal:</span> Formalized long-term longevity goals with Rachel, including targets for strength (Deadlift 1.5x BW), cardio (VO2 Max), and stability.</li>
        <li><span class='font-semibold'>Logistics:</span> Resolved skin irritation from the Whoop strap by switching to a new band material.</li>
        <li><span class='font-semibold'>Focus for Next Week:</span> Continue adapting to the new strength program and schedule the baseline DEXA and VO2 Max tests.</li>
    </ul>
    """
    return WeeklyReport(week_of="August 11, 2025", summary=summary)

# --- API Endpoints ---
@app.get("/", tags=["General"])
async def read_root():
    return {"message": "Welcome to the Elyx Member Journey API"}

@app.get("/messages", response_model=List[Message], tags=["Messages"])
async def get_all_messages():
    if not MESSAGES:
        raise HTTPException(status_code=404, detail="Journey data not loaded.")
    return MESSAGES

@app.get("/messages/timeline", response_model=List[Message], tags=["Messages"])
async def get_timeline_events():
    milestones = [msg for msg in MESSAGES if msg.tags.type == 'milestone']
    if not milestones:
        raise HTTPException(status_code=404, detail="No milestone events found.")
    return milestones

@app.get("/messages/decision/{message_id}", response_model=Dict, tags=["Messages"])
async def get_decision_and_reasons(message_id: int):
    decision_message = next((msg for msg in MESSAGES if msg.id == message_id and msg.tags.type == 'decision'), None)
    if not decision_message:
        raise HTTPException(status_code=404, detail=f"Decision with ID {message_id} not found.")
    
    reason_messages = [msg for msg in MESSAGES if msg.tags.type == 'reason' and msg.tags.linked_id == message_id]
    
    return {"decision": decision_message, "reasons": reason_messages}

@app.get("/metrics/internal", response_model=Dict, tags=["Metrics"])
async def get_internal_metrics():
    if not MESSAGES:
        raise HTTPException(status_code=404, detail="Journey data not loaded.")
    
    role_counts = {}
    for msg in MESSAGES:
        if msg.role not in ["Member", "Personal Assistant"]:
            role_counts[msg.role] = role_counts.get(msg.role, 0) + 1
            
    return {
        "total_elyx_team_interactions": sum(role_counts.values()),
        "interactions_by_role": role_counts
    }

@app.get("/episodes/{month_name}", response_model=EpisodeAnalysis, tags=["Episodes"])
async def get_episode_analysis(month_name: str):
    try:
        month_messages = [
            msg for msg in MESSAGES 
            if datetime.strptime(msg.timestamp.strftime('%B %Y'), '%B %Y') == datetime.strptime(month_name, '%B %Y')
        ]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid month format. Use 'Month YYYY'.")

    if not month_messages:
         raise HTTPException(status_code=404, detail=f"No data found for {month_name}.")

    analysis = get_ai_analysis(month_name, month_messages)
    return analysis





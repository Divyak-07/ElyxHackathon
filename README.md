Elyx Hackathon: Member Journey Visualization
Our submission for the Elyx Life Hackathon, designed to visualize a member's complex 8-month health journey, making it easy to understand progress, context, and the rationale behind every decision.

Team: 3.2bit

Live Demo: https://elyxhackathon.netlify.app/

✨ Key Features
Interactive Journey Log: A complete, WhatsApp-style view of the 8-month conversation.

"Why" Traceability: Click on any decision made by the Elyx team to instantly highlight the messages that led to that action.

AI Chat Assistant: Ask questions like "Why was the Whoop strap ordered?" to get immediate, context-aware answers.

Timeline View: A high-level sidebar visualizing key milestones for a quick overview of the journey.

AI-Generated Insights: Access simulated AI-powered monthly analyses, weekly reports, and a member sentiment chart.

Metrics Dashboard: Visualizes internal team metrics, like interaction counts broken down by role.

🚀 Tech Stack
Backend: Python & FastAPI

Frontend: HTML, JavaScript, Tailwind CSS

Data Visualization: Chart.js

Deployment: Backend on Render, Frontend on Netlify.

🛠️ How to Run Locally
Backend
Clone the repo and navigate into the directory.

Set up a Python virtual environment and activate it.

Install dependencies:

pip install -r requirements.txt

Run the server:

uvicorn main:app --reload

The API will be live at http://127.0.0.1:8000.

Frontend
Simply open the index.html file in your web browser. No build step is needed.

🤖 Note on AI Usage
As per the guidelines, AI was used extensively in this project. The entire 8-month conversation log (journey_data.json) and the simulated AI analyses in the backend were generated using a Large Language Model, guided by detailed prompts based on the hackathon problem statement

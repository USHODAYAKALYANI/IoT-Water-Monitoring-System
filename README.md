IoT Water Monitoring System

Overview
The IoT Water Monitoring System is a web-based dashboard that simulates monitoring water usage using sensor data and activity prediction.
Users can input sensor values like distance and temperature, and the system predicts the possible water activity (such as shower, faucet, or toilet). The results are displayed through an interactive dashboard with graphs, tank visualization, and prediction history.
This project demonstrates how IoT concepts, web development, and cloud deployment can work together to create a smart monitoring system.

Key Features: 

Water activity prediction based on sensor data
Visual water tank level display
Real-time sensor graphs
Prediction history tracking
Activity distribution chart

Tech used:
-Frontend
-React.js
-Recharts (for graphs)
-Backend
-Python
-FastAPI
-Uvicorn

Deployment:

-Netlify – frontend hosting
-Render – backend hosting

Version Control:

-Git & GitHub

Project Structure:

-Running the Project Locally

-Start Backend

cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
-
Backend runs at:
{http://127.0.0.1:8000}
API documentation:
{http://127.0.0.1:8000/docs}

-Start Frontend

cd frontend
npm install
npm start

-Frontend runs at:
http://localhost:3000
SYSTEM WORKFLOW:
-User enters sensor values (distance & temperature) and sensor readings sent periodically.
-Frontend sends the data to the backend API.
-Backend processes the data and predicts the activity.
-The result is returned to the dashboard.
-The dashboard updates graphs, tank visualization, and history.


AUTHOR
Ushodaya Kalyani K
Electrical and Electronics Engineering

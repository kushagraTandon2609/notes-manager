# Notes Manager

Tech: React (frontend) + Streamlit + Flask (backend) + MySQL (database)

## Run locally

### Backend
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# source venv/bin/activate
pip install -r requirements.txt

# create backend/.env from .env.example and set DB_PASSWORD

streamlit run streamlit_flask_backend.py

Flask API will be at http://localhost:5000

### Frontend
cd frontend
npm install

# copy .env.example -> .env.local if needed
npm start
Open http://localhost:3000

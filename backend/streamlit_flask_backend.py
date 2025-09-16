# backend/streamlit_flask_backend.py
import os
import threading
import streamlit as st
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv

# Load env
here = os.path.dirname(__file__)
env_path = os.path.join(here, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "notesdb")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Flask app for API
app = Flask(__name__)
CORS(app)

@app.route("/api/notes", methods=["GET"])
def get_notes():
    user_id = request.args.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route("/api/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
    conn.commit()
    note_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "ok", "note_id": note_id}), 201

@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=%s", (note_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "deleted"}), 200

def run_flask():
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=False)

# Start Flask server in background thread when Streamlit runs
if "flask_started" not in st.session_state:
    threading.Thread(target=run_flask, daemon=True).start()
    st.session_state.flask_started = True

# Streamlit UI (optional admin info)
st.set_page_config(page_title="Notes Backend", page_icon="📝")
st.title("Notes Manager — Backend (Streamlit + Flask)")
st.write(f"Flask API is running on port: {FLASK_PORT}")
st.write("Endpoints:")
st.write("- GET /api/notes?user_id=<id>")
st.write("- POST /api/notes  (JSON body: user_id, title, content)")
st.write("- DELETE /api/notes/<note_id>")

import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = process.env.REACT_APP_API_URL || "http://localhost:5000";
const TEST_USER_ID = 1;

function App() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      const res = await axios.get(`${API}/api/notes`, { params: { user_id: TEST_USER_ID }});
      setNotes(res.data);
    } catch (err) {
      console.error("Fetch notes error:", err);
      alert("Failed to fetch notes. Is backend running?");
    }
  };

  const addNote = async () => {
    if (!title && !content) return;
    try {
      await axios.post(`${API}/api/notes`, { user_id: TEST_USER_ID, title, content });
      setTitle(""); setContent("");
      fetchNotes();
    } catch (err) {
      console.error("Add note error:", err);
    }
  };

  const deleteNote = async (id) => {
    try {
      await axios.delete(`${API}/api/notes/${id}`);
      fetchNotes();
    } catch (err) {
      console.error("Delete note error:", err);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "20px auto", padding: 20 }}>
      <h1>Notes Manager</h1>

      <div style={{ marginBottom: 20 }}>
        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ width: "100%", padding: 8, marginBottom: 8 }}
        />
        <textarea
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          style={{ width: "100%", padding: 8, height: 100 }}
        />
        <button onClick={addNote} style={{ marginTop: 8 }}>Add Note</button>
      </div>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {notes.map((n) => (
          <li key={n.id} style={{ border: "1px solid #ddd", padding: 12, marginBottom: 8 }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <strong>{n.title}</strong>
              <small>{new Date(n.created_at).toLocaleString()}</small>
            </div>
            <p style={{ marginTop: 8 }}>{n.content}</p>
            <button onClick={() => deleteNote(n.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import re
import plotly.graph_objects as go
import os
from auth import sign_out

# === CONSTANTS ===
VIDEO_DIR = "videos"
DATA_DIR = "data"
DB_PATH = "pitcher_biomech.db"
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

COLOR_MAP = {
    "TE": "#1f77b4",
    "FK": "#ff7f0e",
    "TS": "#2ca02c",
    "FH": "#d62728",
    "Angle 1 - o": "#9467bd",
    "Angle 1 - a": "#8c564b",
    "Angle 1 - b": "#e377c2"
}

# === DB Init ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        team TEXT,
        notes TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        date TEXT,
        session_name TEXT,
        video_source TEXT,
        kinovea_csv TEXT,
        notes TEXT,
        FOREIGN KEY(player_id) REFERENCES players(id)
    )''')
    conn.commit()
    conn.close()

init_db()

# === Utility Functions ===
def extract_youtube_id(url):
    patterns = [
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtube\.com/shorts/([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def plot_custom_lines(df, x_col="Time (ms)", chart_key="default", selected_metrics=None):
    fig = go.Figure()
    metrics = selected_metrics if selected_metrics else COLOR_MAP.keys()

    for col in df.columns:
        if col in metrics and col in COLOR_MAP and col != x_col:
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[col],
                mode='lines',
                name=col,
                line=dict(color=COLOR_MAP.get(col, "#cccccc"))
            ))
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title="Speed (px/s)",
        height=400,
        legend_title="Metric",
        template="simple_white"
    )
    st.plotly_chart(fig, use_container_width=True, key=chart_key)

# === MAIN APP ===
def main_app(user_email):
    st.title("Pitcher Biomechanics Tracker")
    st.success(f"Welcome, {user_email}!")

    if st.button("Logout"):
        sign_out()

    tab1, tab2, tab3, tab4 = st.tabs([" Upload Session", " View Sessions", " Compare Sessions", "Admin"])

    # === TAB 1: Upload Session ===
    with tab1:
        # Full Upload Session code goes here
        st.subheader("Upload Session (placeholder)")

    # === TAB 2: View Sessions ===
    with tab2:
        # Full View Sessions code goes here
        st.subheader("View Sessions (placeholder)")

    # === TAB 3: Compare Sessions ===
    with tab3:
        # Full Compare Sessions code goes here
        st.subheader("Compare Sessions (placeholder)")

    # === TAB 4: Admin Tools ===
    with tab4:
        # Full Admin Tools code goes here
        st.subheader("Admin Tools (placeholder)")

    # Debug: Show raw data
    if st.checkbox(" Show Raw Database (Players + Sessions)", value=False):
        conn = sqlite3.connect(DB_PATH)
        players = pd.read_sql("SELECT * FROM players", conn)
        sessions = pd.read_sql("SELECT * FROM sessions", conn)
        st.subheader("Players Table")
        st.dataframe(players)
        st.subheader("Sessions Table")
        st.dataframe(sessions)

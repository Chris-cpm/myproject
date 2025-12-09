import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="MindMate Harmony - Mental Wellness Tracker by Chrisphiliph",
    page_icon="🧠",
    layout="wide"
)
 # Custom CSS
st.markdown("""
    <style>
    /* Blue/Purple Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Make content readable on colored backgrounds */
    /*.stApp > div {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem;
    }
    
    .main-header {
        font-size: 3rem;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .severity-high {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f44336;
    }
    .severity-medium {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
    }
    .severity-low {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }*/
.stApp {
    background: linear-gradient("https://sl.bing.net/i9Ld0Qve5N6");
}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'entries' not in st.session_state:
    st.session_state.entries = []

# Simulated backend call (replace with actual JAC backend API)
def analyze_mood(user_id, mood_text, severity=None):
    """
    This simulates calling your JAC backend.
    In production, replace this with actual HTTP request to JAC server.
    """
    
    # Simulate keyword analysis
    trigger_scores = {}
    text_lower = mood_text.lower()
    
    if any(word in text_lower for word in ["election", "government", "politics"]):
        trigger_scores["political"] = 0.8
    if any(word in text_lower for word in ["people", "society", "community"]):
        trigger_scores["social"] = 0.7
    if any(word in text_lower for word in ["climate", "environment", "pollution"]):
        trigger_scores["environmental"] = 0.75
    if any(word in text_lower for word in ["work", "job", "boss", "career"]):
        trigger_scores["work"] = 0.8
    if any(word in text_lower for word in ["relationship", "partner", "breakup"]):
        trigger_scores["relationship"] = 0.85
    if any(word in text_lower for word in ["sick", "pain", "health"]):
        trigger_scores["health"] = 0.8
    if any(word in text_lower for word in ["money", "debt", "bills"]):
        trigger_scores["financial"] = 0.75
    
    # Determine primary trigger
    primary_trigger = max(trigger_scores, key=trigger_scores.get) if trigger_scores else "other"
    
    # Auto-detect severity if not provided
    if not severity:
        stress_words = ["overwhelmed", "anxious", "depressed", "crisis", "help", "can't"]
        severity = "high" if any(word in text_lower for word in stress_words) else "medium"
    
    # Generate advice
    if severity == "high":
        advice = "IMMEDIATE SUPPORT:\n• Deep breathing (4-7-8 technique)\n• Contact trusted person\n• Crisis line: 988\n• Remove from immediate stressors"
        music = "Weightless - Marconi Union"
        insight = "Significant emotional distress detected. Professional support recommended."
    elif severity == "medium":
        advice = "STRESS MANAGEMENT:\n• Journal your thoughts\n• 15-minute walk\n• Mindfulness practice\n• Connect with support network"
        music = "Clair de Lune - Debussy"
        insight = "Notable stress levels. Implementing coping strategies is beneficial."
    else:
        advice = "MAINTAIN BALANCE:\n• Continue healthy routines\n• Engage in joy activities\n• Stay connected\n• Track mood patterns"
        music = "Here Comes The Sun - The Beatles"
        insight = "Manageable stress levels. Keep up the good work!"
    
    return {
        "success": True,
        "record_id": f"entry_{len(st.session_state.entries) + 1}",
        "user_id": user_id,
        "primary_trigger": primary_trigger,
        "trigger_scores": trigger_scores,
        "severity": severity,
        "advice": advice,
        "music_track": music,
        "deep_insight": insight,
        "timestamp": datetime.now().isoformat()
    }

# Header
st.markdown('<h1 class="main-header">🧠 MindMate</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Your AI-powered mental wellness companion</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard")
    user_id = st.text_input("User ID", value="demo_user")
    
    st.divider()
    
    if st.session_state.entries:
        st.metric("Total Entries", len(st.session_state.entries))
        high_count = sum(1 for e in st.session_state.entries if e['severity'] == 'high')
        st.metric("High Severity", high_count, delta=None if high_count == 0 else "⚠️")
        
        # Most common trigger
        triggers = [e['primary_trigger'] for e in st.session_state.entries]
        if triggers:
            most_common = max(set(triggers), key=triggers.count)
            st.metric("Top Trigger", most_common.title())
    else:
        st.info("No entries yet. Start tracking your mood!")
    
    st.divider()
    
    if st.button("🗑️ Clear All Data", type="secondary"):
        st.session_state.entries = []
        st.rerun()

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📝 New Entry", "📈 Analytics", "📜 History"])

# Tab 1: New Entry
with tab1:
    st.header("How are you feeling?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        mood_text = st.text_area(
            "Describe your mood and what's on your mind:",
            height=150,
            placeholder="I'm feeling overwhelmed by work deadlines and worried about..."
        )
    
    with col2:
        severity = st.selectbox(
            "Severity Level (optional)",
            ["Auto-detect", "Low", "Medium", "High"]
        )
        
        st.info("💡 Leave as 'Auto-detect' for AI to assess severity")
    
    if st.button("🔍 Analyze Mood", type="primary", use_container_width=True):
        if mood_text.strip():
            with st.spinner("Analyzing your mood..."):
                sev = None if severity == "Auto-detect" else severity.lower()
                result = analyze_mood(user_id, mood_text, sev)
                
                if result['success']:
                    st.session_state.entries.append(result)
                    
                    # Display results
                    st.success("✅ Analysis complete!")
                    
                    # Severity indicator
                    severity_class = f"severity-{result['severity']}"
                    st.markdown(f"""
                        <div class="{severity_class}">
                            <h3>Severity: {result['severity'].upper()}</h3>
                            <p><strong>Primary Trigger:</strong> {result['primary_trigger'].title()}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display insights in columns
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.subheader("🎯 Personalized Advice")
                        st.markdown(result['advice'])
                        
                        st.subheader("🎵 Recommended Music")
                        st.info(result['music_track'])
                    
                    with col_b:
                        st.subheader("🧠 Deep Insight")
                        st.markdown(result['deep_insight'])
                        
                        if result['trigger_scores']:
                            st.subheader("📊 Trigger Scores")
                            for trigger, score in result['trigger_scores'].items():
                                st.progress(score, text=f"{trigger.title()}: {score:.0%}")
        else:
            st.error("Please describe your mood before analyzing.")

# Tab 2: Analytics
with tab2:
    if st.session_state.entries:
        st.header("📊 Mood Analytics")
        
        # Create dataframe
        df = pd.DataFrame(st.session_state.entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Entries", len(df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            high_pct = (df['severity'] == 'high').sum() / len(df) * 100
            st.metric("High Severity", f"{high_pct:.0f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            top_trigger = df['primary_trigger'].mode()[0] if not df['primary_trigger'].mode().empty else "N/A"
            st.metric("Top Trigger", top_trigger.title())
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            avg_triggers = df['trigger_scores'].apply(lambda x: len(x)).mean()
            st.metric("Avg Triggers/Entry", f"{avg_triggers:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Visualizations
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            # Severity distribution
            severity_counts = df['severity'].value_counts()
            fig1 = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                title="Severity Distribution",
                color=severity_counts.index,
                color_discrete_map={'high': '#f44336', 'medium': '#ff9800', 'low': '#4caf50'}
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_v2:
            # Trigger distribution
            trigger_counts = df['primary_trigger'].value_counts()
            fig2 = px.bar(
                x=trigger_counts.index,
                y=trigger_counts.values,
                title="Trigger Frequency",
                labels={'x': 'Trigger Type', 'y': 'Count'},
                color=trigger_counts.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Timeline
        st.subheader("📅 Mood Timeline")
        severity_map = {'low': 1, 'medium': 2, 'high': 3}
        df['severity_num'] = df['severity'].map(severity_map)
        
        fig3 = px.scatter(
            df,
            x='timestamp',
            y='severity_num',
            color='primary_trigger',
            size='severity_num',
            hover_data=['primary_trigger', 'severity'],
            title="Mood Entries Over Time"
        )
        fig3.update_yaxes(tickvals=[1, 2, 3], ticktext=['Low', 'Medium', 'High'])
        st.plotly_chart(fig3, use_container_width=True)
        
    else:
        st.info("📭 No data yet. Create your first mood entry to see analytics!")

# Tab 3: History
with tab3:
    if st.session_state.entries:
        st.header("📜 Entry History")
        
        for i, entry in enumerate(reversed(st.session_state.entries)):
            with st.expander(f"Entry #{len(st.session_state.entries) - i} - {entry['primary_trigger'].title()} - {entry['timestamp'][:19]}"):
                severity_class = f"severity-{entry['severity']}"
                st.markdown(f'<div class="{severity_class}"><strong>Severity:</strong> {entry["severity"].upper()}</div>', unsafe_allow_html=True)
                
                st.markdown(f"**Trigger:** {entry['primary_trigger'].title()}")
                st.markdown(f"**Record ID:** `{entry['record_id']}`")
                
                st.divider()
                
                st.markdown("**Advice:**")
                st.markdown(entry['advice'])
                
                st.markdown("**Music Recommendation:**")
                st.info(entry['music_track'])
                
                st.markdown("**Insight:**")
                st.markdown(entry['deep_insight'])
    else:
        st.info("📭 No entries yet. Start tracking your mood in the 'New Entry' tab!")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; padding: 2rem;">
        <p>MindMate - AI-Powered Mental Wellness Tracking</p>
        <p style="font-size: 0.9rem;">⚠️ This tool is for wellness tracking only. In crisis, contact emergency services or call 988.</p>
    </div>
""", unsafe_allow_html=True)
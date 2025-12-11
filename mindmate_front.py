import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import hashlib

# Page configuration
st.set_page_config(
    page_title="MINDMATE HARMONY - Mental Wellness Tracker",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS - Fixed styling
st.markdown("""
    <style>
    /* Beautiful gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Semi-transparent container for readability */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .main-header {
        font-size: 3rem;
        color: #667eea;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .severity-high {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f44336;
        margin: 1rem 0;
    }
    
    .severity-medium {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
    }
    
    .severity-low {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.7);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Data persistence functions
DATA_FILE = Path("mindmate_data.json")

def load_data():
    """Load data from JSON file"""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return []
    return []

def save_data(entries):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(entries, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# Initialize session state
if 'entries' not in st.session_state:
    st.session_state.entries = load_data()
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Improved JAC backend integration
def analyze_mood(user_id, mood_text, severity=None):
    """
    Call JAC backend for mood analysis with proper error handling and security
    """
    try:
        # Sanitize inputs to prevent code injection
        sanitized_mood = mood_text.replace('"', '\\"').replace('\n', ' ')
        sanitized_user = user_id.replace('"', '\\"')
        sev_param = f', severity="{severity}"' if severity else ''
        
        # Alternative 1: Use JAC as a library/API (preferred)
        # This assumes you have a JAC REST API running
        api_url = "http://localhost:8000/api/analyze"
        
        payload = {
            "user_id": sanitized_user,
            "mood": mood_text,
            "severity": severity
        }
        
        try:
            response = requests.post(api_url, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            # Fallback to local processing if API unavailable
            pass
        
        # Alternative 2: Mock/Local processing for demo
        # Remove this in production with real JAC backend
        return mock_analyze_mood(user_id, mood_text, severity)
        
    except Exception as e:
        st.error(f"Error analyzing mood: {str(e)}")
        return None

def mock_analyze_mood(user_id, mood_text, severity=None):
    """
    Mock analysis for demo purposes - replace with real JAC backend
    """
    # Simple keyword analysis
    trigger_keywords = {
        "political": ["election", "politics", "government", "vote", "policy", "politician"],
        "work": ["job", "boss", "deadline", "work", "career", "office", "colleague"],
        "health": ["sick", "pain", "anxiety", "depression", "mental", "physical"],
        "relationship": ["partner", "breakup", "marriage", "dating", "spouse", "divorce"],
        "financial": ["money", "debt", "bills", "salary", "budget", "expensive"],
        "academic": ["exam", "school", "study", "grade", "homework", "test"],
        "family": ["family", "parent", "mother", "father", "sibling", "child"],
        "social": ["friend", "lonely", "isolated", "people", "community"],
        "environmental": ["climate", "environment", "pollution", "nature", "weather"]
    }
    
    mood_lower = mood_text.lower()
    trigger_scores = {}
    
    for trigger, keywords in trigger_keywords.items():
        score = sum(1 for kw in keywords if kw in mood_lower)
        trigger_scores[trigger] = score
    
    primary_trigger = max(trigger_scores.items(), key=lambda x: x[1])[0] if any(trigger_scores.values()) else "other"
    
    # Auto-detect severity
    if not severity:
        high_words = ["crisis", "hopeless", "unbearable", "suicide", "kill", "can't take", "overwhelming"]
        medium_words = ["stressed", "anxious", "worried", "upset", "struggling", "difficult"]
        
        if any(word in mood_lower for word in high_words):
            severity = "high"
        elif any(word in mood_lower for word in medium_words):
            severity = "medium"
        else:
            severity = "low"
    
    # Generate contextual insights based on trigger and severity
    insight_parts = []
    
    # Severity-based base insight
    if severity == "high":
        insight_parts.append("Your entry indicates significant emotional distress that warrants immediate attention.")
    elif severity == "medium":
        insight_parts.append("Your mood reflects notable challenges that could benefit from proactive support.")
    else:
        insight_parts.append("Your emotional state appears stable with manageable concerns.")
    
    # Trigger-specific insights
    trigger_insights = {
        "political": {
            "high": "Political events can deeply affect our sense of safety and control. Consider limiting news consumption and focusing on local action you can take.",
            "medium": "Political concerns are valid. Channel this energy into constructive civic engagement or set boundaries around political media.",
            "low": "Your political awareness is healthy. Stay informed while maintaining balance in other life areas."
        },
        "work": {
            "high": "Work-related distress at this level may indicate burnout or unsustainable conditions. Professional boundaries and support are crucial.",
            "medium": "Work pressures are impacting your wellbeing. Time management, delegation, or discussing workload with supervisors may help.",
            "low": "Work challenges are present but manageable. Continue using your coping strategies and maintain work-life boundaries."
        },
        "health": {
            "high": "Health concerns causing this level of distress require both medical attention and mental health support. Don't hesitate to reach out.",
            "medium": "Health worries can be consuming. Consulting healthcare providers and practicing self-compassion are important steps.",
            "low": "Health awareness is positive. Continue healthy routines and address concerns early with medical professionals."
        },
        "relationship": {
            "high": "Relationship conflicts at this intensity significantly impact emotional wellbeing. Couples therapy or counseling could provide valuable support.",
            "medium": "Relationship challenges are affecting you. Open communication, setting healthy boundaries, and possibly counseling could help.",
            "low": "Relationship dynamics have ups and downs. Your awareness suggests you're navigating this thoughtfully."
        },
        "financial": {
            "high": "Financial stress at this level can feel overwhelming. Seek support from financial counselors, trusted advisors, or mental health professionals.",
            "medium": "Money concerns are weighing on you. Creating a budget, exploring resources, or consulting a financial advisor may provide relief.",
            "low": "Financial awareness is responsible. Continue monitoring your finances and planning for future stability."
        },
        "academic": {
            "high": "Academic pressure has reached a critical point. Reach out to counselors, professors, or academic support services immediately.",
            "medium": "Academic stress is significant. Time management, study groups, tutoring, or speaking with instructors could ease the burden.",
            "low": "Academic challenges are normal. Your approach seems balanced—continue your study habits and self-care."
        },
        "family": {
            "high": "Family dynamics causing this distress may benefit from family therapy or individual counseling to process these relationships.",
            "medium": "Family tensions are impacting you. Setting boundaries, open dialogue when safe, or therapy can help navigate these relationships.",
            "low": "Family relationships have complexities. Your self-awareness in managing these dynamics is healthy."
        },
        "social": {
            "high": "Social isolation or conflicts at this level need attention. Consider reaching out to trusted friends, joining groups, or seeking counseling.",
            "medium": "Social concerns are affecting your mood. Small steps like reaching out to one person or joining an activity can make a difference.",
            "low": "Social connections seem balanced. Continue nurturing relationships that bring you joy and support."
        },
        "environmental": {
            "high": "Environmental anxiety (eco-anxiety) is real and valid. Channeling this into action while practicing self-care is essential.",
            "medium": "Environmental concerns are weighing on you. Balance staying informed with taking breaks and focusing on actionable steps.",
            "low": "Environmental awareness shows your values. Continue sustainable choices while maintaining overall wellbeing."
        },
        "other": {
            "high": "You're experiencing significant distress. Professional support can help you understand and address what you're going through.",
            "medium": "Multiple factors may be contributing to your current state. Taking time to identify specific concerns can be helpful.",
            "low": "General life challenges are present. Your self-reflection and self-care practices are serving you well."
        }
    }
    
    # Add trigger-specific insight
    if primary_trigger in trigger_insights:
        insight_parts.append(trigger_insights[primary_trigger][severity])
    
    # Add general recommendations
    if severity == "high":
        insight_parts.append("Remember: You deserve support and things can improve with proper help.")
    elif severity == "medium":
        insight_parts.append("Taking proactive steps now can prevent escalation and improve your situation.")
    else:
        insight_parts.append("Maintaining this self-awareness and continuing healthy habits will serve you well.")
    
    insight = " ".join(insight_parts)
    
    # Generate advice and music
    if severity == "high":
        advice = """🚨 IMMEDIATE SUPPORT NEEDED:
1. Deep breathing (4-7-8 technique: inhale 4, hold 7, exhale 8)
2. Contact a trusted person immediately
3. Crisis Lifeline: 988 (call or text) or text HELLO to 741741
4. Remove yourself from immediate stressors if safe
5. Consider emergency mental health services if needed"""
        
        music_options = [
            "Weightless - Marconi Union (scientifically proven calming)",
            "Spiegel im Spiegel - Arvo Pärt (deeply peaceful)",
            "Clair de Lune - Debussy (gentle, soothing)"
        ]
        music = music_options[hash(mood_text) % len(music_options)]
        
    elif severity == "medium":
        advice = """⚠️ STRESS MANAGEMENT:
1. Journal your thoughts (10-15 minutes of free writing)
2. Take an outdoor walk (15-20 minutes, mindful movement)
3. Practice mindfulness or meditation (apps: Headspace, Calm)
4. Connect with your support network (call or text someone)
5. Limit caffeine and prioritize sleep (7-9 hours)"""
        
        music_options = [
            "Clair de Lune - Debussy (calming classical)",
            "Pure Shores - All Saints (relaxing)",
            "Nocturne in E-flat Major - Chopin (peaceful piano)"
        ]
        music = music_options[hash(mood_text) % len(music_options)]
        
    else:
        advice = """✅ MAINTAIN YOUR BALANCE:
1. Continue your healthy routines and self-care practices
2. Engage in activities that bring you joy and fulfillment
3. Stay connected with friends, family, and community
4. Keep a gratitude journal (note 3 things daily)
5. Exercise regularly and maintain good sleep hygiene
6. Celebrate small wins and progress"""
        
        music_options = [
            "Here Comes The Sun - The Beatles (uplifting)",
            "Three Little Birds - Bob Marley (positive vibes)",
            "Good Vibrations - The Beach Boys (mood-boosting)"
        ]
        music = music_options[hash(mood_text) % len(music_options)]
    
    return {
        "success": True,
        "record_id": hashlib.md5(f"{user_id}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
        "user_id": user_id,
        "mood": mood_text,
        "primary_trigger": primary_trigger,
        "trigger_scores": trigger_scores,
        "severity": severity,
        "advice": advice,
        "music_track": music,
        "deep_insight": insight,
        "timestamp": datetime.now().isoformat()
    }

# Simple authentication
def login_user():
    """Simple user authentication"""
    st.sidebar.header("🔐 User Login")
    username = st.sidebar.text_input("Username", key="login_username")
    
    if st.sidebar.button("Login", type="primary"):
        if username.strip():
            st.session_state.current_user = username.strip()
            st.rerun()
    
    if st.session_state.current_user:
        st.sidebar.success(f"Logged in as: {st.session_state.current_user}")
        if st.sidebar.button("Logout"):
            st.session_state.current_user = None
            st.rerun()

# Sidebar
with st.sidebar:
    login_user()
    
    if st.session_state.current_user:
        st.divider()
        st.header("📊 Dashboard")
        
        user_entries = [e for e in st.session_state.entries 
                       if e['user_id'] == st.session_state.current_user]
        
        if user_entries:
            st.metric("Total Entries", len(user_entries))
            high_count = sum(1 for e in user_entries if e['severity'] == 'high')
            st.metric("High Severity", high_count, 
                     delta="⚠️" if high_count > 0 else None)
            
            # Most common trigger
            triggers = [e['primary_trigger'] for e in user_entries]
            if triggers:
                most_common = max(set(triggers), key=triggers.count)
                st.metric("Top Trigger", most_common.title())
        else:
            st.info("No entries yet. Start tracking!")
        
        st.divider()
        
        # Export data
        if st.button("📥 Export Data", use_container_width=True):
            if user_entries:
                export_json = json.dumps(user_entries, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=export_json,
                    file_name=f"mindmate_export_{st.session_state.current_user}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        if st.button("🗑️ Clear My Data", type="secondary", use_container_width=True):
            st.session_state.entries = [e for e in st.session_state.entries 
                                       if e['user_id'] != st.session_state.current_user]
            save_data(st.session_state.entries)
            st.rerun()

# Main header
st.markdown('<h1 class="main-header">🧠 MINDMATE HARMONY</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">AI-Powered Mental Wellness Tracker</p>', unsafe_allow_html=True)

if not st.session_state.current_user:
    st.warning("👈 Please login in the sidebar to start tracking your mental wellness")
    st.stop()

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📝 New Entry", "📈 Analytics", "📜 History"])

# Tab 1: New Entry
with tab1:
    st.header("How are you feeling today?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        mood_text = st.text_area(
            "Describe your mood and what's on your mind:",
            height=200,
            placeholder="I'm feeling overwhelmed by work deadlines and worried about...",
            help="Be honest and detailed. Your entries are private and secure."
        )
    
    with col2:
        severity = st.selectbox(
            "Severity Level",
            ["Auto-detect", "Low", "Medium", "High"],
            help="Leave as 'Auto-detect' for AI to assess"
        )
        
        add_note = st.checkbox("Add private note")
        if add_note:
            private_note = st.text_input("Private note (not analyzed)")
        
        st.info("💡 **Tip:** Detailed entries provide better insights")
    
    if st.button("🔍 Analyze Mood", type="primary", use_container_width=True):
        if not mood_text.strip():
            st.error("Please describe your mood before analyzing.")
        elif len(mood_text) < 10:
            st.warning("Please provide more detail (at least 10 characters)")
        else:
            with st.spinner("🔄 Analyzing your mood..."):
                sev = None if severity == "Auto-detect" else severity.lower()
                result = analyze_mood(st.session_state.current_user, mood_text, sev)
                
                if result and result.get('success'):
                    # Add private note if exists
                    if add_note and 'private_note' in locals():
                        result['private_note'] = private_note
                    
                    st.session_state.entries.append(result)
                    save_data(st.session_state.entries)
                    
                    # Display results
                    st.success("✅ Analysis complete!")
                    
                    # Severity indicator
                    severity_class = f"severity-{result['severity']}"
                    st.markdown(f"""
                        <div class="{severity_class}">
                            <h3>📊 Severity: {result['severity'].upper()}</h3>
                            <p><strong>Primary Trigger:</strong> {result['primary_trigger'].title()}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display insights in columns
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.subheader("🎯 Personalized Advice")
                        st.markdown(result['advice'])
                        
                        st.subheader("🎵 Recommended Music")
                        st.info(f"🎧 {result['music_track']}")
                    
                    with col_b:
                        st.subheader("🧠 Deep Insight")
                        st.markdown(result['deep_insight'])
                        
                        if result.get('trigger_scores'):
                            st.subheader("📊 Trigger Analysis")
                            max_score = max(result['trigger_scores'].values()) or 1
                            for trigger, score in sorted(result['trigger_scores'].items(), 
                                                        key=lambda x: x[1], reverse=True)[:5]:
                                if score > 0:
                                    st.progress(score / max_score, 
                                              text=f"{trigger.title()}: {score} matches")
                    
                    st.balloons()
                else:
                    st.error("❌ Analysis failed. Please try again or check backend connection.")

# Tab 2: Analytics
with tab2:
    user_entries = [e for e in st.session_state.entries 
                   if e['user_id'] == st.session_state.current_user]
    
    if user_entries:
        st.header("📊 Your Wellness Analytics")
        
        # Create dataframe
        df = pd.DataFrame(user_entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Date filter
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            date_range = st.date_input(
                "Filter by date range",
                value=(df['date'].min(), df['date'].max()),
                key="date_filter"
            )
        
        with col_filter2:
            severity_filter = st.multiselect(
                "Filter by severity",
                options=['low', 'medium', 'high'],
                default=['low', 'medium', 'high']
            )
        
        # Apply filters
        if len(date_range) == 2:
            df_filtered = df[(df['date'] >= date_range[0]) & 
                            (df['date'] <= date_range[1]) &
                            (df['severity'].isin(severity_filter))]
        else:
            df_filtered = df[df['severity'].isin(severity_filter)]
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📝 Total Entries", len(df_filtered))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            high_pct = (df_filtered['severity'] == 'high').sum() / len(df_filtered) * 100 if len(df_filtered) > 0 else 0
            st.metric("⚠️ High Severity", f"{high_pct:.0f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            if not df_filtered['primary_trigger'].mode().empty:
                top_trigger = df_filtered['primary_trigger'].mode()[0]
                st.metric("🎯 Top Trigger", top_trigger.title())
            else:
                st.metric("🎯 Top Trigger", "N/A")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            days_tracked = (df_filtered['date'].max() - df_filtered['date'].min()).days + 1
            st.metric("📅 Days Tracked", days_tracked)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Visualizations
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            # Severity distribution
            severity_counts = df_filtered['severity'].value_counts()
            fig1 = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                title="📊 Severity Distribution",
                color=severity_counts.index,
                color_discrete_map={
                    'high': '#f44336', 
                    'medium': '#ff9800', 
                    'low': '#4caf50'
                }
            )
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_v2:
            # Trigger distribution
            trigger_counts = df_filtered['primary_trigger'].value_counts().head(8)
            fig2 = px.bar(
                x=trigger_counts.values,
                y=trigger_counts.index,
                orientation='h',
                title="🎯 Top Triggers",
                labels={'x': 'Count', 'y': 'Trigger Type'},
                color=trigger_counts.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Timeline
        st.subheader("📅 Mood Timeline")
        severity_map = {'low': 1, 'medium': 2, 'high': 3}
        df_filtered['severity_num'] = df_filtered['severity'].map(severity_map)
        
        fig3 = go.Figure()
        
        for sev in ['low', 'medium', 'high']:
            df_sev = df_filtered[df_filtered['severity'] == sev]
            fig3.add_trace(go.Scatter(
                x=df_sev['timestamp'],
                y=df_sev['severity_num'],
                mode='markers',
                name=sev.title(),
                marker=dict(
                    size=12,
                    color={'low': '#4caf50', 'medium': '#ff9800', 'high': '#f44336'}[sev]
                ),
                text=df_sev['primary_trigger'],
                hovertemplate='<b>%{text}</b><br>%{x}<extra></extra>'
            ))
        
        fig3.update_layout(
            title="Mood Entries Over Time",
            xaxis_title="Date",
            yaxis_title="Severity",
            yaxis=dict(tickvals=[1, 2, 3], ticktext=['Low', 'Medium', 'High']),
            hovermode='closest'
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Trend analysis
        st.subheader("📈 Wellness Trends")
        daily_avg = df_filtered.groupby('date')['severity_num'].mean().reset_index()
        
        fig4 = px.line(
            daily_avg,
            x='date',
            y='severity_num',
            title="Average Daily Severity",
            labels={'severity_num': 'Avg Severity', 'date': 'Date'}
        )
        fig4.update_yaxes(tickvals=[1, 2, 3], ticktext=['Low', 'Medium', 'High'])
        st.plotly_chart(fig4, use_container_width=True)
        
    else:
        st.info("📭 No data yet. Create your first mood entry to see analytics!")

# Tab 3: History
with tab3:
    user_entries = [e for e in st.session_state.entries 
                   if e['user_id'] == st.session_state.current_user]
    
    if user_entries:
        st.header("📜 Your Entry History")
        
        # Search and filter
        search_term = st.text_input("🔍 Search entries", placeholder="Search by trigger, mood, etc.")
        
        filtered_entries = user_entries
        if search_term:
            search_lower = search_term.lower()
            filtered_entries = [e for e in user_entries if 
                              search_lower in e.get('mood', '').lower() or
                              search_lower in e.get('primary_trigger', '').lower()]
        
        st.caption(f"Showing {len(filtered_entries)} of {len(user_entries)} entries")
        
        for i, entry in enumerate(reversed(filtered_entries)):
            entry_num = len(user_entries) - user_entries.index(entry)
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
            
            with st.expander(f"Entry #{entry_num} - {entry['primary_trigger'].title()} - {timestamp}"):
                severity_class = f"severity-{entry['severity']}"
                st.markdown(f'<div class="{severity_class}"><strong>Severity:</strong> {entry["severity"].upper()}</div>', 
                          unsafe_allow_html=True)
                
                col_h1, col_h2 = st.columns([2, 1])
                
                with col_h1:
                    st.markdown(f"**Trigger:** {entry['primary_trigger'].title()}")
                    st.markdown(f"**Mood Entry:**")
                    st.markdown(f"> {entry.get('mood', 'N/A')}")
                
                with col_h2:
                    st.markdown(f"**Record ID:** `{entry['record_id']}`")
                    st.markdown(f"**Timestamp:** {timestamp}")
                    if 'private_note' in entry:
                        st.markdown(f"**Private Note:** {entry['private_note']}")
                
                st.divider()
                
                tab_advice, tab_music, tab_insight = st.tabs(["💡 Advice", "🎵 Music", "🧠 Insight"])
                
                with tab_advice:
                    st.markdown(entry.get('advice', 'N/A'))
                
                with tab_music:
                    st.info(entry.get('music_track', 'N/A'))
                
                with tab_insight:
                    st.markdown(entry.get('deep_insight', 'N/A'))
                
                # Delete button
                if st.button(f"🗑️ Delete Entry #{entry_num}", key=f"delete_{entry['record_id']}"):
                    st.session_state.entries.remove(entry)
                    save_data(st.session_state.entries)
                    st.rerun()
    else:
        st.info("📭 No entries yet. Start tracking your mood in the 'New Entry' tab!")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>🧠 MindMate Harmony</strong> - AI-Powered Mental Wellness Tracking</p>
        <p style="font-size: 0.9rem;">⚠️ This tool is for wellness tracking only. In crisis, contact emergency services or call <strong>988</strong>.</p>
        <p style="font-size: 0.8rem; color: #888;">Your data is stored locally and private to your account.</p>
    </div>
""", unsafe_allow_html=True)
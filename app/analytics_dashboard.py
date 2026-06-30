import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import os

class AnalyticsDashboard:
    """Analytics dashboard for resume analysis trends"""
    
    def __init__(self):
        self.history_file = "analysis_history.json"
    
    def save_analysis(self, analysis_data):
        """Save analysis results to history"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            # Add timestamp
            analysis_data['timestamp'] = datetime.now().isoformat()
            history.append(analysis_data)
            
            # Keep only last 100 entries
            if len(history) > 100:
                history = history[-100:]
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving analysis: {str(e)}")
            return False
    
    def load_history(self):
        """Load analysis history"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            return []
        except:
            return []
    
    def display_dashboard(self):
        """Display analytics dashboard"""
        history = self.load_history()
        
        if not history:
            st.info("No analysis history available. Start analyzing resumes to see trends!")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(history)
        
        # Clean data
        if 'match_score' in df.columns:
            df['match_score'] = pd.to_numeric(df['match_score'], errors='coerce')
        if 'ats_score' in df.columns:
            df['ats_score'] = pd.to_numeric(df['ats_score'], errors='coerce')
        
        # Row 1: Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Analyses", len(history))
        with col2:
            avg_score = df['match_score'].mean() if 'match_score' in df.columns else 0
            st.metric("Average Match Score", f"{int(avg_score)}%")
        with col3:
            avg_ats = df['ats_score'].mean() if 'ats_score' in df.columns else 0
            st.metric("Average ATS Score", f"{int(avg_ats)}%")
        with col4:
            unique_roles = df['job_role'].nunique() if 'job_role' in df.columns else 0
            st.metric("Unique Roles Analyzed", unique_roles)
        
        # Row 2: Trend Chart
        if 'timestamp' in df.columns and 'match_score' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df_sorted = df.sort_values('timestamp')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_sorted['timestamp'],
                y=df_sorted['match_score'],
                mode='lines+markers',
                name='Match Score',
                line=dict(color='blue', width=2),
                marker=dict(size=6)
            ))
            fig.update_layout(
                title="Match Score Trends Over Time",
                xaxis_title="Date",
                yaxis_title="Score (%)",
                height=300,
                hovermode='x'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Row 3: Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            if 'match_score' in df.columns:
                fig = go.Figure(data=[go.Histogram(
                    x=df['match_score'],
                    nbinsx=20,
                    marker_color='blue'
                )])
                fig.update_layout(
                    title="Match Score Distribution",
                    xaxis_title="Score",
                    yaxis_title="Frequency",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'job_role' in df.columns:
                role_counts = df['job_role'].value_counts().head(10)
                fig = go.Figure(data=[go.Bar(
                    x=role_counts.values,
                    y=role_counts.index,
                    orientation='h',
                    marker_color='green'
                )])
                fig.update_layout(
                    title="Top Job Roles Analyzed",
                    xaxis_title="Count",
                    yaxis_title="Job Role",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Row 4: Recent History
        st.subheader("📋 Recent Analyses")
        recent = df.head(10) if not df.empty else df
        cols_to_display = ['timestamp', 'job_role', 'match_score', 'ats_score']
        if all(col in recent.columns for col in cols_to_display):
            st.dataframe(
                recent[cols_to_display],
                column_config={
                    "timestamp": "Date",
                    "job_role": "Job Role",
                    "match_score": "Match %",
                    "ats_score": "ATS %"
                },
                use_container_width=True
            )
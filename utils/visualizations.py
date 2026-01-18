import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_job_match_scores(matches):
    """
    Create a bar chart for top job matches
    """
    if not matches:
        return None
        
    df = pd.DataFrame(matches[:5])
    
    fig = px.bar(
        df, 
        x='score', 
        y='job_title', 
        orientation='h',
        title='Top Job Role Matches',
        labels={'score': 'Match Score (%)', 'job_title': 'Job Role'},
        color='score',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

def plot_skills_radar(extracted_skills, taxonomy):
    """
    Create a radar chart showing skill distribution across categories
    """
    # Count skills per category
    categories = []
    counts = []
    
    # Flatten skills for easy lookup
    flat_skills = [s.lower() for s in extracted_skills]
    
    for category, skills in taxonomy.items():
        cat_skills = [s.lower() for s in skills]
        # Count how many of user's skills fall into this category
        count = sum(1 for s in flat_skills if s in cat_skills)
        if count > 0:
            categories.append(category)
            counts.append(count)
            
    if not categories:
        return None
        
    fig = go.Figure(data=go.Scatterpolar(
        r=counts,
        theta=categories,
        fill='toself',
        name='Your Skills'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(counts) + 1],
                gridcolor='rgba(255,255,255,0.2)',
                linecolor='rgba(255,255,255,0.2)',
                tickfont=dict(color='white')
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        title="Skill Distribution by Category",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def plot_skill_gap(match_data):
    """
    Donut chart of Matched vs Missing skills for top role
    """
    matched = len(match_data['matched_skills'])
    missing = len(match_data['missing_skills'])
    
    labels = ['Matched Skills', 'Missing Skills']
    values = [matched, missing]
    colors = ['#00CC96', '#EF553B']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.6,
        marker=dict(colors=['#6366F1', '#F43F5E']) # Indigo, Rose
    )])
    
    fig.update_layout(
        title=f"Skill Gap Analysis: {match_data['job_title']}",
        annotations=[dict(text=f"{match_data['score']}%", x=0.5, y=0.5, font_size=20, showarrow=False)],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

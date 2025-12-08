#!/usr/bin/env python3
"""
AI-Powered Project Generator - Streamlit Dashboard
Interactive interface for discovering and planning tech projects
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from project_generator import ProjectGenerator
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Project Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .project-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .difficulty-beginner {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .difficulty-intermediate {
        background-color: #ffc107;
        color: black;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .difficulty-advanced {
        background-color: #dc3545;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .tech-badge {
        background-color: #17a2b8;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.85rem;
    }
    .skill-badge {
        background-color: #6c757d;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.85rem;
    }
    .feature-item {
        padding: 0.5rem 0;
        border-left: 3px solid #667eea;
        padding-left: 1rem;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = ProjectGenerator()
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None
if 'saved_projects' not in st.session_state:
    st.session_state.saved_projects = []

def display_difficulty_badge(difficulty):
    """Display colored difficulty badge"""
    difficulty_class = f"difficulty-{difficulty.lower()}"
    return f'<span class="{difficulty_class}">{difficulty.upper()}</span>'

def display_tech_badges(tech_stack):
    """Display technology badges"""
    badges = ''.join([f'<span class="tech-badge">{tech}</span>' for tech in tech_stack])
    return badges

def display_skill_badges(skills):
    """Display skill badges"""
    badges = ''.join([f'<span class="skill-badge">{skill}</span>' for skill in skills])
    return badges

def create_domain_distribution_chart(all_projects):
    """Create domain distribution chart"""
    domain_counts = {}
    for project in all_projects:
        domain = project.get('domain', 'Unknown')
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    fig = go.Figure(data=[go.Pie(
        labels=list(domain_counts.keys()),
        values=list(domain_counts.values()),
        hole=0.4,
        marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe'])
    )])
    
    fig.update_layout(
        title="Projects by Domain",
        showlegend=True,
        height=400
    )
    
    return fig

def create_difficulty_chart(all_projects):
    """Create difficulty distribution chart"""
    difficulty_counts = {}
    for project in all_projects:
        difficulty = project.get('difficulty', 'Unknown')
        difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
    
    colors = {
        'Beginner': '#28a745',
        'Intermediate': '#ffc107',
        'Advanced': '#dc3545'
    }
    
    fig = go.Figure(data=[go.Bar(
        x=list(difficulty_counts.keys()),
        y=list(difficulty_counts.values()),
        marker_color=[colors.get(d, '#6c757d') for d in difficulty_counts.keys()]
    )])
    
    fig.update_layout(
        title="Projects by Difficulty",
        xaxis_title="Difficulty Level",
        yaxis_title="Number of Projects",
        height=400
    )
    
    return fig

def create_tech_stack_chart(all_projects):
    """Create technology stack popularity chart"""
    tech_counts = {}
    for project in all_projects:
        for tech in project.get('tech_stack', []):
            tech_counts[tech] = tech_counts.get(tech, 0) + 1
    
    # Get top 15 technologies
    sorted_tech = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:15]
    
    fig = go.Figure(data=[go.Bar(
        x=[t[1] for t in sorted_tech],
        y=[t[0] for t in sorted_tech],
        orientation='h',
        marker_color='#667eea'
    )])
    
    fig.update_layout(
        title="Top 15 Technologies",
        xaxis_title="Number of Projects",
        yaxis_title="Technology",
        height=500
    )
    
    return fig

# Main Dashboard
st.markdown('<div class="main-header">🚀 AI-Powered Project Generator</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Discover your next tech project in Cybersecurity, Data Analytics, AI/ML, and Cloud Security</p>', unsafe_allow_html=True)

# Sidebar - Project Filters
with st.sidebar:
    st.header("🎯 Project Finder")
    
    domain = st.selectbox(
        "Select Domain",
        options=["All", "Cybersecurity", "Data Analytics", "Artificial Intelligence", "Cloud Security"],
        index=0
    )
    
    experience_level = st.selectbox(
        "Experience Level",
        options=["All", "Beginner", "Intermediate", "Advanced"],
        index=0
    )
    
    st.subheader("⏱️ Time Commitment")
    duration_filter = st.slider(
        "Maximum Duration (weeks)",
        min_value=1,
        max_value=12,
        value=12,
        step=1
    )
    
    st.subheader("💻 Tech Preferences")
    all_techs = ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "Docker", 
                 "Kubernetes", "AWS", "Azure", "React", "Flask", "FastAPI",
                 "Streamlit", "Pandas", "Elasticsearch", "Machine Learning"]
    
    tech_preferences = st.multiselect(
        "Select Technologies",
        options=all_techs,
        default=[]
    )
    
    st.divider()
    
    if st.button("🎲 Generate Random Project", type="primary", use_container_width=True):
        domain_map = {
            "All": None,
            "Cybersecurity": "cybersecurity",
            "Data Analytics": "data_analytics",
            "Artificial Intelligence": "artificial_intelligence",
            "Cloud Security": "cloud_security"
        }
        
        level_map = {
            "All": None,
            "Beginner": "beginner",
            "Intermediate": "intermediate",
            "Advanced": "advanced"
        }
        
        selected_domain = domain_map[domain]
        selected_level = level_map[experience_level]
        
        # Get all projects matching criteria
        all_projects = st.session_state.generator.get_all_projects(
            domain=selected_domain,
            experience_level=selected_level
        )
        
        # Filter by tech preferences
        if tech_preferences:
            filtered = []
            for project in all_projects:
                tech_match = any(tech in project['tech_stack'] for tech in tech_preferences)
                if tech_match:
                    filtered.append(project)
            all_projects = filtered if filtered else all_projects
        
        # Filter by duration
        filtered_by_duration = []
        for project in all_projects:
            duration_str = project['duration']
            max_weeks = int(duration_str.split('-')[-1].split()[0])
            if max_weeks <= duration_filter:
                filtered_by_duration.append(project)
        
        all_projects = filtered_by_duration if filtered_by_duration else all_projects
        
        if all_projects:
            import random
            st.session_state.selected_project = random.choice(all_projects)
            st.success("✅ Project generated!")
            st.rerun()
        else:
            st.error("No projects match your criteria. Try adjusting filters.")
    
    st.divider()
    
    # Saved Projects
    st.subheader("💾 Saved Projects")
    if st.session_state.saved_projects:
        for idx, proj in enumerate(st.session_state.saved_projects):
            if st.button(f"📌 {proj['title'][:30]}...", key=f"saved_{idx}"):
                st.session_state.selected_project = proj
                st.rerun()
    else:
        st.info("No saved projects yet")

# Main Content Area
if st.session_state.selected_project:
    project = st.session_state.selected_project
    
    # Project Header
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.markdown(f"## {project['title']}")
    
    with col2:
        st.markdown(display_difficulty_badge(project['difficulty']), unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"**⏱️ {project['duration']}**")
    
    with col4:
        if st.button("💾 Save Project"):
            if project not in st.session_state.saved_projects:
                st.session_state.saved_projects.append(project)
                st.success("Project saved!")
    
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "🎯 Features", "📚 Learning", "🔧 Tech Stack", "📄 Export"])
    
    with tab1:
        st.markdown("### Project Description")
        st.markdown(f"<div style='font-size: 1.1rem; line-height: 1.8;'>{project['description']}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Skills You'll Develop")
            for skill in project['skills']:
                st.markdown(f"- **{skill}**")
        
        with col2:
            st.markdown("### ⏱️ Project Timeline")
            st.info(f"**Duration:** {project['duration']}")
            st.info(f"**Difficulty:** {project['difficulty']}")
            st.info(f"**Domain:** {project.get('domain', 'N/A').replace('_', ' ').title()}")
    
    with tab2:
        st.markdown("### 🚀 Core Features")
        
        for idx, feature in enumerate(project['features'], 1):
            st.markdown(f"""
            <div class="feature-item">
                <strong>{idx}.</strong> {feature}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 💡 Extension Ideas")
        st.markdown("Take your project to the next level with these advanced features:")
        
        for idx, extension in enumerate(project['extensions'], 1):
            st.markdown(f"**{idx}.** {extension}")
    
    with tab3:
        st.markdown("### 📚 Learning Outcomes")
        st.markdown("By completing this project, you will:")
        
        for idx, outcome in enumerate(project['learning_outcomes'], 1):
            st.markdown(f"""
            <div style='background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #667eea;'>
                <strong>{idx}.</strong> {outcome}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Learning Resources
        st.markdown("### 📖 Recommended Learning Path")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎓 Prerequisites")
            st.markdown("""
            - Basic programming knowledge
            - Understanding of software development
            - Familiarity with version control (Git)
            - Problem-solving mindset
            """)
        
        with col2:
            st.markdown("#### 🛠️ Development Approach")
            st.markdown("""
            1. **Plan**: Break down features into tasks
            2. **Build**: Implement core functionality first
            3. **Test**: Write tests as you develop
            4. **Iterate**: Add features incrementally
            5. **Document**: Keep README updated
            """)
    
    with tab4:
        st.markdown("### 💻 Technology Stack")
        
        st.markdown(display_tech_badges(project['tech_stack']), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Tech stack details
        st.markdown("### 📦 Setup Instructions")
        
        st.code(f"""
# Create project directory
mkdir {project['title'].lower().replace(' ', '-')}
cd {project['title'].lower().replace(' ', '-')}

# Initialize git repository
git init

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Create requirements.txt
touch requirements.txt

# Install dependencies (add to requirements.txt first)
pip install -r requirements.txt

# Create project structure
mkdir src tests docs
touch README.md .gitignore
        """, language="bash")
        
        st.markdown("### 📚 Documentation Links")
        
        # Generate documentation links for tech stack
        tech_docs = {
            "Python": "https://docs.python.org/3/",
            "TensorFlow": "https://www.tensorflow.org/api_docs",
            "PyTorch": "https://pytorch.org/docs/stable/index.html",
            "Scikit-learn": "https://scikit-learn.org/stable/documentation.html",
            "Docker": "https://docs.docker.com/",
            "Kubernetes": "https://kubernetes.io/docs/",
            "AWS": "https://docs.aws.amazon.com/",
            "Azure": "https://docs.microsoft.com/azure/",
            "React": "https://react.dev/",
            "Flask": "https://flask.palletsprojects.com/",
            "FastAPI": "https://fastapi.tiangolo.com/",
            "Streamlit": "https://docs.streamlit.io/"
        }
        
        for tech in project['tech_stack']:
            if tech in tech_docs:
                st.markdown(f"- [{tech} Documentation]({tech_docs[tech]})")
    
    with tab5:
        st.markdown("### 📄 Export Project Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Markdown Format")
            markdown_plan = st.session_state.generator.export_project_plan(project, "markdown")
            st.download_button(
                label="Download Markdown",
                data=markdown_plan,
                file_name=f"{project['title'].lower().replace(' ', '_')}_plan.md",
                mime="text/markdown"
            )
        
        with col2:
            st.markdown("#### 📊 JSON Format")
            json_plan = st.session_state.generator.export_project_plan(project, "json")
            st.download_button(
                label="Download JSON",
                data=json_plan,
                file_name=f"{project['title'].lower().replace(' ', '_')}_plan.json",
                mime="application/json"
            )
        
        st.markdown("---")
        
        st.markdown("### 👁️ Preview")
        
        with st.expander("📝 Markdown Preview"):
            st.markdown(markdown_plan)
        
        with st.expander("📊 JSON Preview"):
            st.json(json.loads(json_plan))

else:
    # Welcome screen with analytics
    st.markdown("""
    ## 👋 Welcome to the AI-Powered Project Generator!
    
    Discover your next tech project tailored to your experience level and interests. Our database contains **40+ curated projects** across four cutting-edge domains.
    
    ### 🎯 How It Works
    
    1. **Select your domain** - Choose from Cybersecurity, Data Analytics, AI/ML, or Cloud Security
    2. **Set your experience level** - Beginner, Intermediate, or Advanced
    3. **Add preferences** - Filter by technologies and time commitment
    4. **Generate project** - Get a detailed project plan with features, tech stack, and learning outcomes
    5. **Export & Build** - Download your project plan and start building!
    
    ### 📊 Project Database Overview
    """)
    
    # Get all projects for analytics
    all_projects = st.session_state.generator.get_all_projects()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>40+</h2>
            <p>Total Projects</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>4</h2>
            <p>Tech Domains</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>3</h2>
            <p>Difficulty Levels</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2>50+</h2>
            <p>Technologies</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_domain_distribution_chart(all_projects), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_difficulty_chart(all_projects), use_container_width=True)
    
    st.plotly_chart(create_tech_stack_chart(all_projects), use_container_width=True)
    
    st.markdown("---")
    
    # Featured Projects
    st.markdown("### ⭐ Featured Projects")
    
    featured = [
        st.session_state.generator.get_all_projects("cybersecurity", "intermediate")[0],
        st.session_state.generator.get_all_projects("data_analytics", "intermediate")[0],
        st.session_state.generator.get_all_projects("artificial_intelligence", "intermediate")[0],
        st.session_state.generator.get_all_projects("cloud_security", "intermediate")[0]
    ]
    
    cols = st.columns(2)
    
    for idx, proj in enumerate(featured):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"#### {proj['title']}")
                st.markdown(f"**Domain:** {proj['domain'].replace('_', ' ').title()}")
                st.markdown(f"**Difficulty:** {proj['difficulty']}")
                st.markdown(f"{proj['description'][:150]}...")
                
                if st.button(f"View Details", key=f"featured_{idx}"):
                    st.session_state.selected_project = proj
                    st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    ### 🚀 Ready to Start?
    
    Use the sidebar to configure your preferences and click **"Generate Random Project"** to discover your next challenge!
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>AI-Powered Project Generator v1.0 | Built with Streamlit | 
    <a href='https://github.com/Mangesh-Bhattacharya/ai-powered-project-generator' target='_blank'>GitHub</a></p>
    <p>💡 <strong>Tip:</strong> Save interesting projects to your sidebar for quick access!</p>
</div>
""", unsafe_allow_html=True)

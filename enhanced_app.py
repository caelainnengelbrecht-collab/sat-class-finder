import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
from datetime import date, datetime, timedelta
import plotly.express as px

# =============================================
#  Enhanced SAT Class Finder 
#  Matches students with ideal SAT prep classes based on test dates and schedule
# =============================================

st.set_page_config(page_title="Live+AI SAT Prep Platform", page_icon="🤖", layout="wide")

# Header with Nerdy.com-inspired styling
st.markdown("""
<style>
/* Main app background matching Nerdy's clean aesthetic */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Main header matching Nerdy's hero section */
.main-header {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    padding: 40px 30px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Metric cards with Nerdy's clean card style */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(226, 232, 240, 0.8);
    color: #0f172a;
}

/* Practice section card matching Nerdy's content blocks */
.practice-card {
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
    padding: 32px;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(226, 232, 240, 0.8);
    margin: 24px 0;
    color: #0f172a;
}

/* AI feature cards with tech-focused styling */
.ai-feature-card {
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin: 12px 0;
    box-shadow: 0 4px 16px rgba(14, 165, 233, 0.3);
    border: none;
    transition: transform 0.2s ease;
}
.ai-feature-card:hover {
    transform: translateY(-2px);
}

/* Success metrics with clean, modern styling */
.success-metric {
    background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.2);
    color: #0f172a;
}

/* Buttons matching Nerdy's CTA style */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 14px 28px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(14, 165, 233, 0.3);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0284c7, #2563eb);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
}

/* Secondary buttons */
.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #64748b 0%, #475569 100%);
    box-shadow: 0 4px 16px rgba(100, 116, 139, 0.3);
}

/* Content styling matching Nerdy's clean typography */
.stMarkdown {
    color: #f8fafc;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
}

/* Dataframe styling */
.stDataFrame {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* Expander styling */
.streamlit-expander {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    border: 1px solid rgba(226, 232, 240, 0.8);
    margin: 8px 0;
}

/* Info/warning/error boxes */
.stInfo, .stWarning, .stError, .stSuccess {
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

/* Text input styling */
.stTextInput input {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 8px;
}

/* Select box styling */
.stSelectbox select {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(226, 232, 240, 0.8);
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'test_date' not in st.session_state:
    st.session_state.test_date = None
if 'selected_class_types' not in st.session_state:
    st.session_state.selected_class_types = []
if 'selected_services' not in st.session_state:
    st.session_state.selected_services = []

# SAT Test Dates
SAT_DATES = {
    "August 23, 2025": date(2025, 8, 23),
    "September 13, 2025": date(2025, 9, 13), 
    "October 4, 2025": date(2025, 10, 4),
    "November 8, 2025": date(2025, 11, 8),
    "December 6, 2025": date(2025, 12, 6),
    "March 14, 2026": date(2026, 3, 14),
    "May 2, 2026": date(2026, 5, 2),
    "June 6, 2026": date(2026, 6, 6)
}

CA_BASE = "https://www.varsitytutors.com/ca"
CA_SAT_SEARCH = f"{CA_BASE}/classes/search?f_grades=9th-grade&f_grades=10th-grade&f_grades=11th-grade&f_grades=12th-grade&f_subjects=test-prep&q=sat"
CA_SAT_PAGE = f"{CA_BASE}/classes/test-prep/sat"

# Course mappings - actual Varsity Tutors courses
COURSE_CATALOG = {
    "SAT 2-Week Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-two-week-bootcamp/dp/e34ad454-d5a7-4851-9694-cdd64675b3d8",
        "description": "Streamlined, strategy-focused prep designed to hack the SAT without time-draining academic review",
        "duration": "2 weeks, 4x per week",
        "format": "8 sessions, 1hr 30min each",
        "best_for": "Final review, fast-track prep, or busy schedules"
    },
    "SAT 4-Week Prep Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-four-week-prep-course/dp/e3a6e856-31db-429d-a52f-dfbbc93c2edd", 
        "description": "Comprehensive 4-week SAT preparation covering all sections",
        "duration": "4 weeks",
        "format": "Multiple sessions per week",
        "best_for": "Intensive preparation with moderate timeline"
    },
    "SAT Prep Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-prep-course/dp/c85c2298-bd6a-4cd4-be0d-8f4f35d3f7eb",
        "description": "Comprehensive SAT preparation course covering all test sections",
        "duration": "Extended timeline",
        "format": "Regular sessions",
        "best_for": "Thorough, comprehensive preparation"
    },
    "Proctored Practice SAT": {
        "url": "https://www.varsitytutors.com/courses/vtp-proctored-practiced-sat-9-12/dp/2298ff50-8011-48e7-acc0-c81cb25eeae1",
        "description": "Real SAT practice tests under proctored conditions",
        "duration": "Ongoing",
        "format": "Practice test sessions",
        "best_for": "Test-taking practice and timing"
    },
    "Ultimate SAT Review Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-ultimate-sat-review-session/dp/2a08c912-0a50-4639-b097-dfcaa2f591de",
        "description": "Comprehensive review of key SAT concepts and strategies",
        "duration": "Single session",
        "format": "Extended review session",
        "best_for": "Last-minute review and strategy reinforcement"
    },
    "SAT Math Cram Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-math-cram-session/dp/33f2fab0-1908-4b5c-9d36-966e467af942",
        "description": "Intensive focus on SAT Math section concepts and strategies",
        "duration": "Cram session",
        "format": "Math-focused intensive",
        "best_for": "Math section improvement"
    },
    "SAT Reading/Writing Cram Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-reading-writing-cram-session/dp/03ea8fe7-ff75-4b07-b69e-f3558c1ed44e",
        "description": "Intensive focus on SAT Reading and Writing sections",
        "duration": "Cram session", 
        "format": "ELA-focused intensive",
        "best_for": "Reading and Writing section improvement"
    },
    "1-Week SAT Math Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-one-week-bootcamp-sat-math-9-12/dp/255ad018-d421-46fb-9e54-210e4045a491",
        "description": "One week intensive bootcamp focused on SAT Math",
        "duration": "1 week",
        "format": "Daily math sessions",
        "best_for": "Math-focused intensive preparation"
    },
    "1-Week SAT ELA Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-one-week-bootcamp-sat-ela-9-12/dp/a4621f0a-e935-46ad-beda-de37624b05ba",
        "description": "One week intensive bootcamp focused on SAT Reading and Writing",
        "duration": "1 week",
        "format": "Daily ELA sessions", 
        "best_for": "Reading and Writing intensive preparation"
    },
    "2-Week SAT Math Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-math-sat-9-12/dp/2f67b5be-e283-406f-b4d2-fe3fc17e52aa",
        "description": "Two week intensive course focused on SAT Math",
        "duration": "2 weeks",
        "format": "Math-focused sessions",
        "best_for": "Extended math preparation"
    },
    "2-Week SAT ELA Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-ela-sat-9-12/dp/81b322ee-93b3-4389-88af-bf11f7d0240f",
        "description": "Two week intensive course focused on SAT Reading and Writing",
        "duration": "2 weeks", 
        "format": "ELA-focused sessions",
        "best_for": "Extended reading and writing preparation"
    }
}

# Progress indicator
progress_labels = ["Choose Test Date", "Select Classes", "Add AI Practice", "Your Pathway"]
progress = st.session_state.step / len(progress_labels)
st.progress(progress, text=f"Step {st.session_state.step} of {len(progress_labels)}: {progress_labels[st.session_state.step-1]}")

# Step 1: Test Date Selection
if st.session_state.step == 1:
    st.markdown('<div class="main-header"><h1>🎯 Choose Your SAT Test Date</h1><p>Let\'s start by selecting when you plan to take the SAT</p></div>', unsafe_allow_html=True)
    
    st.markdown("## 📅 Available SAT Test Dates")
    
    # Create columns for test dates
    cols = st.columns(2)
    for i, (date_str, date_obj) in enumerate(SAT_DATES.items()):
        col = cols[i % 2]
        days_until = (date_obj - date.today()).days
        
        with col:
            if days_until > 0:
                st.markdown(f"### {date_str}")
                st.markdown(f"**{days_until} days from now**")
                
                if days_until > 56:
                    st.success("✅ Plenty of time for comprehensive prep")
                elif days_until > 28:
                    st.warning("⚡ Intensive prep recommended")
                else:
                    st.error("🚨 Last-minute prep needed")
                
                if st.button(f"Choose {date_str}", key=f"date_{i}", use_container_width=True):
                    st.session_state.test_date = date_str
                    st.session_state.step = 2
                    st.rerun()
            else:
                st.markdown(f"### {date_str}")
                st.markdown("**Past date**")
                st.markdown("❌ Date has passed")

# Step 2: Multiple Class Selection  
elif st.session_state.step == 2:
    st.markdown('<div class="main-header"><h1>📚 Select Your SAT Classes</h1><p>Choose one or more classes that fit your timeline and goals</p></div>', unsafe_allow_html=True)
    
    target_date_obj = SAT_DATES[st.session_state.test_date]
    days_until = (target_date_obj - date.today()).days
    
    st.markdown(f"## Your Test Date: **{st.session_state.test_date}**")
    st.markdown(f"**{days_until} days to prepare**")
    
    # Show timeline status
    if days_until > 56:
        st.success("✅ Excellent timeline - All class types recommended")
        recommended_classes = list(COURSE_CATALOG.keys())
        timeline_status = "excellent"
    elif days_until > 28:
        st.warning("⚡ Good timeline - Focus on intensive options")
        recommended_classes = [
            "SAT 4-Week Prep Course", "SAT 2-Week Bootcamp", "2-Week SAT Math Course", 
            "2-Week SAT ELA Course", "SAT Math Cram Session", "SAT Reading/Writing Cram Session",
            "Ultimate SAT Review Session", "Proctored Practice SAT"
        ]
        timeline_status = "good"
    else:
        st.error("🚨 Limited timeline - Focus on intensive/cram options")
        recommended_classes = [
            "SAT 2-Week Bootcamp", "1-Week SAT Math Bootcamp", "1-Week SAT ELA Bootcamp",
            "SAT Math Cram Session", "SAT Reading/Writing Cram Session", "Ultimate SAT Review Session"
        ]
        timeline_status = "urgent"
    
    # Smart Recommendations Section
    st.markdown("## 🎯 Your Personalized Recommendation")
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    
    if timeline_status == "excellent":
        st.markdown("### 📚 **Comprehensive Success Plan** (56+ days)")
        st.markdown("**Perfect! You have time for thorough preparation. Here's your optimal path:**")
        st.markdown("#### **🎯 Recommended Classes:**")
        st.markdown("• **SAT Prep Course** (8+ weeks) - Your foundation for comprehensive review")
        st.markdown("• **Proctored Practice SAT** (ongoing) - Regular practice tests under real conditions")
        st.markdown("• **SAT Math Cram Session** (final 2 weeks) - Targeted improvement in your weak areas")
        
        st.markdown("#### **📅 Study Schedule:**")
        st.markdown("• **Weeks 1-6:** 6-8 hours/week with live classes + daily practice")
        st.markdown("• **Weeks 7-8:** 10+ hours/week with intensive review and practice tests")
        st.markdown("• **Study frequency:** Consistent daily practice (30-60 mins) using Nerdy Practice Hub plus live class time")
        
        st.markdown("#### **🎯 Success Strategy:**")
        st.markdown("• Take regular practice tests using [Nerdy Practice Hub SAT](https://practice.nerdy.com/subjects/sat)")
        st.markdown("• Use AI Diagnostics to create personalized practice sessions")
        st.markdown("• Focus on weak areas identified through AI-powered analysis")
        
    elif timeline_status == "good":
        st.markdown("### ⚡ **Focused Intensive Plan** (28-56 days)")
        st.markdown("**Good timeline! Focus on high-impact preparation with strategic course selection:**")
        st.markdown("#### **🎯 Recommended Classes:**")
        st.markdown("• **SAT 4-Week Prep Course** - Concentrated comprehensive review")
        st.markdown("• **2-Week SAT Math Course** OR **2-Week SAT ELA Course** - Target your weaker subject")
        st.markdown("• **Ultimate SAT Review Session** - Final strategy and confidence boost")
        
        st.markdown("#### **📅 Study Schedule:**")
        st.markdown("• **Weeks 1-4:** 8-10 hours/week with intensive classes + focused practice")
        st.markdown("• **Final 2 weeks:** 12+ hours/week with review and practice tests")
        st.markdown("• **Study frequency:** Daily practice (45-90 mins) using Nerdy's AI-powered learning tools")
        
        st.markdown("#### **🎯 Success Strategy:**")
        st.markdown("• Take 3-4 full practice tests using [Nerdy Practice Hub](https://practice.nerdy.com/subjects/sat)")
        st.markdown("• Use AI Worksheets and AI Diagnostics for targeted practice")
        st.markdown("• Prioritize your weaker subject with subject-specific courses")
        
    else:  # urgent timeline
        st.markdown("### 🚨 **Emergency Action Plan** (<28 days)")
        st.markdown("**Limited time requires strategic focus. Here's your high-impact approach:**")
        st.markdown("#### **🎯 Recommended Classes:**")
        st.markdown("• **SAT 2-Week Bootcamp** - Intensive comprehensive review with key strategies")
        st.markdown("• **1-Week SAT Math Bootcamp** AND **SAT Reading/Writing Cram Session** - Target both sections")
        st.markdown("• **Skip comprehensive courses** - Focus on strategy and weak area improvement")
        
        st.markdown("#### **📅 Study Schedule:**")
        st.markdown("• **Week 1-2:** 15+ hours/week with bootcamp + daily intensive practice")
        st.markdown("• **Final week:** 20+ hours/week with practice tests and review")
        st.markdown("• **Study frequency:** Multiple daily sessions using Nerdy's intensive AI practice tools")
        
        st.markdown("#### **🎯 Success Strategy:**")
        st.markdown("• Take 2-3 full practice tests using [Nerdy Practice Hub](https://practice.nerdy.com/subjects/sat)")
        st.markdown("• Focus on AI-powered test-taking strategies and quick skill building")
        st.markdown("• **Consider:** Moving to the next test date for better preparation time")
        
        st.warning("💡 **Alternative Recommendation:** Consider registering for the next SAT date to allow 8+ weeks of thorough preparation")
    
    st.markdown("#### **📖 Additional Resources:**")
    st.markdown("• **[Nerdy Practice Hub SAT](https://practice.nerdy.com/subjects/sat)** - AI-powered practice tests and diagnostics")
    st.markdown("• **[AI Learning Assistant](https://practice.nerdy.com/subjects/sat/ai-tutor)** - Personalized tutoring aligned with your needs")
    st.markdown("• **[AI Worksheets](https://practice.nerdy.com/worksheets)** - Custom practice problems and targeted skill building")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Select Your Classes")
    st.markdown("**Choose multiple classes to create your personalized prep plan:**")
    
    # Create checkbox grid for course selection
    selected_classes = []
    
    # Organize courses into categories for better display
    comprehensive_courses = ["SAT Prep Course", "SAT 4-Week Prep Course", "SAT 2-Week Bootcamp"]
    specialized_courses = ["2-Week SAT Math Course", "2-Week SAT ELA Course", "1-Week SAT Math Bootcamp", "1-Week SAT ELA Bootcamp"]
    cram_courses = ["SAT Math Cram Session", "SAT Reading/Writing Cram Session", "Ultimate SAT Review Session"]
    practice_courses = ["Proctored Practice SAT"]
    
    # Display courses by category
    st.markdown("#### 📖 Comprehensive Courses")
    for course_name in comprehensive_courses:
        if course_name in recommended_classes:
            course_info = COURSE_CATALOG[course_name]
            selected = st.checkbox(
                f"**{course_name}**", 
                key=f"course_{course_name}",
                help=f"{course_info['description']} | Duration: {course_info['duration']}"
            )
            st.markdown(f"*{course_info['description']}*")
            st.markdown(f"**Duration:** {course_info['duration']} | **Best for:** {course_info['best_for']}")
            if selected:
                selected_classes.append(course_name)
            st.markdown("---")
    
    st.markdown("#### 🎯 Subject-Focused Courses")
    for course_name in specialized_courses:
        if course_name in recommended_classes:
            course_info = COURSE_CATALOG[course_name]
            selected = st.checkbox(
                f"**{course_name}**", 
                key=f"course_{course_name}",
                help=f"{course_info['description']} | Duration: {course_info['duration']}"
            )
            st.markdown(f"*{course_info['description']}*")
            st.markdown(f"**Duration:** {course_info['duration']} | **Best for:** {course_info['best_for']}")
            if selected:
                selected_classes.append(course_name)
            st.markdown("---")
    
    st.markdown("#### ⚡ Intensive & Cram Sessions")
    for course_name in cram_courses:
        if course_name in recommended_classes:
            course_info = COURSE_CATALOG[course_name]
            selected = st.checkbox(
                f"**{course_name}**", 
                key=f"course_{course_name}",
                help=f"{course_info['description']} | Duration: {course_info['duration']}"
            )
            st.markdown(f"*{course_info['description']}*")
            st.markdown(f"**Duration:** {course_info['duration']} | **Best for:** {course_info['best_for']}")
            if selected:
                selected_classes.append(course_name)
            st.markdown("---")
    
    st.markdown("#### 📝 Practice & Review")
    for course_name in practice_courses:
        if course_name in recommended_classes:
            course_info = COURSE_CATALOG[course_name]
            selected = st.checkbox(
                f"**{course_name}**", 
                key=f"course_{course_name}",
                help=f"{course_info['description']} | Duration: {course_info['duration']}"
            )
            st.markdown(f"*{course_info['description']}*")
            st.markdown(f"**Duration:** {course_info['duration']} | **Best for:** {course_info['best_for']}")
            if selected:
                selected_classes.append(course_name)
    
    # Update session state with selections
    st.session_state.selected_class_types = selected_classes
    
    # Show selection summary
    if selected_classes:
        st.markdown("### ✅ Your Selected Classes:")
        for class_name in selected_classes:
            st.markdown(f"• **{class_name}**")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Test Date", key="back_to_step1"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Continue to AI Services →", key="continue_to_step3", disabled=(len(selected_classes) == 0)):
            st.session_state.step = 3
            st.rerun()
    
    if len(selected_classes) == 0:
        st.info("💡 **Please select at least one class to continue**")

# Step 3: AI Practice Services Selection
elif st.session_state.step == 3:
    st.markdown('<div class="main-header"><h1>🤖 Add AI Practice Services</h1><p>Enhance your live classes with AI-powered practice and support</p></div>', unsafe_allow_html=True)
    
    st.markdown(f"## Your Selections So Far:")
    st.markdown(f"**Test Date:** {st.session_state.test_date}")
    if st.session_state.selected_class_types:
        st.markdown("**Selected Classes:**")
        for class_name in st.session_state.selected_class_types:
            st.markdown(f"• {class_name}")
    
    st.markdown("### 🚀 Available AI Services")
    st.markdown("**Select the AI-powered services you'd like to add to your prep plan:**")
    
    # AI Services from Nerdy Practice Hub with specific URLs
    services = [
        {
            "name": "AI Learning Assistant",
            "description": "Get personalized help with SAT questions and concepts",
            "icon": "🎯",
            "stats": "Available 24/7",
            "url": "https://practice.nerdy.com/subjects/sat/ai-tutor"
        },
        {
            "name": "Quiz of the Day", 
            "description": "Test your knowledge with AI-generated multiple choice questions",
            "icon": "📊",
            "stats": "Daily practice quizzes",
            "url": "https://practice.nerdy.com/subjects/sat/quiz"
        },
        {
            "name": "AI Worksheets",
            "description": "Generate custom worksheets with AI-powered content creation",
            "icon": "📝", 
            "stats": "Ready-to-study collections",
            "url": "https://practice.nerdy.com/worksheets"
        },
        {
            "name": "Learning Games",
            "description": "Make learning fun with interactive games and challenges",
            "icon": "🎮",
            "stats": "Number Cards, Speed Challenge, Crossmath",
            "url": "https://practice.nerdy.com/games"
        }
    ]
    
    selected_services = []
    
    # Create checkboxes for each service
    cols = st.columns(2)
    for i, service in enumerate(services):
        col = cols[i % 2]
        with col:
            st.markdown('<div class="ai-feature-card">', unsafe_allow_html=True)
            selected = st.checkbox(
                f"{service['icon']} **{service['name']}**", 
                key=f"service_{i}",
                help=service['description']
            )
            st.markdown(f"{service['description']}")
            st.markdown(f"*{service['stats']}*")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if selected:
                selected_services.append(service['name'])
    
    st.session_state.selected_services = selected_services
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Class Format", key="back_to_step2"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Continue to Pathway →", key="continue_to_step4"):
            st.session_state.step = 4
            st.rerun()

# Step 4: Complete Pathway Timeline
elif st.session_state.step == 4:
    st.markdown('<div class="main-header"><h1>🗓️ Your SAT Success Timeline</h1><p>Follow this roadmap to achieve your goals!</p></div>', unsafe_allow_html=True)
    
    target_date_obj = SAT_DATES[st.session_state.test_date]
    days_until = (target_date_obj - date.today()).days
    
    # Timeline Overview
    st.markdown("## 📊 Your Plan Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f"**🎯 Target Date**")
        st.markdown(f"## {st.session_state.test_date}")
        st.markdown(f"**{days_until} days to go**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f"**📚 Live Classes**")
        st.markdown(f"## {len(st.session_state.selected_class_types)} courses")
        st.markdown("**Direct enrollment ready**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f"**🤖 AI Practice**")
        if st.session_state.selected_services:
            st.markdown(f"## {len(st.session_state.selected_services)} tools")
            st.markdown("**Daily practice plan**")
        else:
            st.markdown("## 0 selected")
            st.markdown("**Consider adding AI support**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Success Timeline - Phase by Phase
    st.markdown("## 🗓️ Your Success Timeline")
    st.markdown("**Follow these phases in order to maximize your SAT score:**")
    
    # Phase 1: Immediate Actions (Today)
    st.markdown("### 🚀 Phase 1: Get Started Today")
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    
    if st.session_state.selected_class_types:
        st.markdown("#### ✅ **Action Required: Enroll in Your Selected Classes**")
        st.markdown("**🎯 Do this TODAY - Popular classes fill up fast!**")
        
        # Quick enrollment table
        enrollment_data = []
        for course_name in st.session_state.selected_class_types:
            course_info = COURSE_CATALOG[course_name]
            enrollment_data.append({
                "Course": course_name,
                "Duration": course_info['duration'],
                "🎯 Enroll Now": f"[Click to Enroll]({course_info['url']})"
            })
        
        enrollment_df = pd.DataFrame(enrollment_data)
        st.dataframe(enrollment_df, use_container_width=True, hide_index=True, column_config={
            "🎯 Enroll Now": st.column_config.LinkColumn(
                "🎯 Enroll Now",
                help="Click to enroll in this course immediately"
            )
        })
        
        st.markdown("**📞 Need help enrolling?** Call **(800) 803-4058** - they can help you find the perfect schedule!")
    else:
        st.warning("⚠️ **No classes selected.** Go back to Step 2 to select your courses!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Phase 2: Daily AI Practice Schedule
    if st.session_state.selected_services:
        st.markdown("### 🤖 Phase 2: Daily AI Practice Schedule")
        st.markdown('<div class="ai-feature-card">', unsafe_allow_html=True)
        st.markdown("#### **Start These Practice Routines Immediately:**")
        
        # Service mapping with frequencies
        service_info = {
            "AI Learning Assistant": {
                "url": "https://practice.nerdy.com/subjects/sat/ai-tutor",
                "frequency": "Daily (15-30 mins)",
                "when": "When you have questions or need concept explanations",
                "goal": "Get immediate help and understanding"
            },
            "Quiz of the Day": {
                "url": "https://practice.nerdy.com/subjects/sat/quiz", 
                "frequency": "Daily (10-15 mins)",
                "when": "Every morning or after dinner",
                "goal": "Keep skills sharp with regular practice"
            },
            "AI Worksheets": {
                "url": "https://practice.nerdy.com/worksheets",
                "frequency": "3x per week (20-30 mins)",
                "when": "Monday, Wednesday, Friday",
                "goal": "Targeted skill building and reinforcement"
            },
            "Learning Games": {
                "url": "https://practice.nerdy.com/games",
                "frequency": "2x per week (10-20 mins)", 
                "when": "Weekend fun sessions",
                "goal": "Make learning enjoyable and stress-free"
            }
        }
        
        for service in st.session_state.selected_services:
            if service in service_info:
                info = service_info[service]
                st.markdown(f"**🎯 {service}** - [{info['frequency']}]({info['url']})")
                st.markdown(f"• **When:** {info['when']}")
                st.markdown(f"• **Goal:** {info['goal']}")
                st.markdown("---")
        
        st.markdown("**💡 Pro Tip:** Set phone reminders for your daily practice sessions!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("### 🤖 Phase 2: Add AI Practice Support")
        st.info("💡 **Recommendation:** Go back to Step 3 to add AI services for daily practice support!")
        if st.button("← Go Back to Add AI Services"):
            st.session_state.step = 3
            st.rerun()
    
    # Phase 3: Live Class Schedule  
    if st.session_state.selected_class_types:
        st.markdown("### 👨‍🏫 Phase 3: Live Class Schedule")
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### **Your Live Learning Plan:**")
        
        # Categorize classes by type
        comprehensive_classes = [c for c in st.session_state.selected_class_types if "Prep Course" in c or "Bootcamp" in c]
        subject_classes = [c for c in st.session_state.selected_class_types if "Math" in c or "ELA" in c or "Reading" in c]
        practice_classes = [c for c in st.session_state.selected_class_types if "Practice" in c or "Review" in c]
        
        if comprehensive_classes:
            st.markdown("**📚 Your Core Preparation:**")
            for class_name in comprehensive_classes:
                course_info = COURSE_CATALOG[class_name]
                st.markdown(f"• **{class_name}** ({course_info['duration']}) - {course_info['best_for']}")
        
        if subject_classes:
            st.markdown("**🎯 Subject-Focused Improvement:**")
            for class_name in subject_classes:
                course_info = COURSE_CATALOG[class_name]
                st.markdown(f"• **{class_name}** ({course_info['duration']}) - {course_info['best_for']}")
        
        if practice_classes:
            st.markdown("**📝 Practice & Review:**")
            for class_name in practice_classes:
                course_info = COURSE_CATALOG[class_name]
                st.markdown(f"• **{class_name}** ({course_info['duration']}) - {course_info['best_for']}")
        
        st.markdown("**📅 After enrolling:** Check your class schedule and add all sessions to your calendar!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Phase 4: 1:1 Tutoring Timeline
    st.markdown("### 👥 Phase 4: 1:1 Tutoring Timeline")
    st.markdown('<div class="practice-card">', unsafe_allow_html=True)
    
    if days_until > 56:
        st.markdown("#### **Excellent Timeline - Strategic Tutoring Plan:**")
        st.markdown("• **Week 2-3:** Initial diagnostic and weak area identification")
        st.markdown("• **Week 5-6:** Mid-course check-in and strategy refinement")
        st.markdown("• **Week 7-8:** Final prep and test-day confidence building")
        st.markdown("**📞 Call (800) 803-4058** to schedule your first session")
    elif days_until > 28:
        st.markdown("#### **Good Timeline - Focused Tutoring Plan:**")
        st.markdown("• **This week:** Immediate diagnostic and personalized study plan")
        st.markdown("• **Week 2-3:** Focus on your most challenging sections")
        st.markdown("• **Final week:** Test strategies and confidence building")
        st.markdown("**📞 Call (800) 803-4058** - mention you need intensive help!")
    else:
        st.markdown("#### **Urgent Timeline - Emergency Tutoring Plan:**")
        st.markdown("• **Immediately:** Book intensive diagnostic session")
        st.markdown("• **This week:** Daily tutoring if possible")
        st.markdown("• **2 days before test:** Final strategy and confidence session")
        st.markdown("**📞 Call (800) 803-4058 ASAP** - explain your urgent timeline!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Phase 5: Final Prep
    st.markdown("### 🎯 Phase 5: Final Week Preparation")
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### **Week Before Test Day:**")
    st.markdown("• **Take final practice test** to confirm readiness")
    st.markdown("• **Review test-day strategies** from your classes")
    st.markdown("• **Prepare test materials** (ID, calculators, snacks)")
    st.markdown("• **Get good sleep** (8+ hours each night)")
    st.markdown("• **Stay positive** - you've prepared well!")
    
    st.markdown("#### **Test Day Morning:**")
    st.markdown("• **Eat a good breakfast** with protein")
    st.markdown("• **Arrive 30 minutes early** to the test center")
    st.markdown("• **Take deep breaths** and trust your preparation")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Success Probability Assessment
    if days_until > 56:
        st.success("📈 **Success Probability: Very High** - You have an excellent timeline!")
    elif days_until > 28:
        st.warning("📈 **Success Probability: High** - Stay focused and consistent!")
    else:
        st.error("📈 **Success Probability: Moderate** - Consider intensive preparation or next test date!")
    
    # Quick Action Summary
    st.markdown("## 💡 Your Next 3 Actions")
    st.markdown("**Do these today to start your success journey:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1️⃣ Enroll")
        if st.session_state.selected_class_types:
            st.markdown("Click enrollment links above")
        else:
            st.markdown("Go back to select classes")
    
    with col2:
        st.markdown("### 2️⃣ Practice")
        if st.session_state.selected_services:
            st.markdown("Start your daily AI routine")
        else:
            st.markdown("Add AI practice tools")
    
    with col3:
        st.markdown("### 3️⃣ Schedule")
        st.markdown("Call (800) 803-4058 for tutoring")
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to AI Services", key="back_to_step3"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🔄 Start Over", key="restart"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

# Clean wizard flow - no sidebar needed

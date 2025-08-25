import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

# =============================================
#  Simplified SAT Class Finder 
#  Connect students with Varsity Tutors SAT classes
# =============================================

st.set_page_config(page_title="SAT Class Finder", page_icon="📚", layout="wide")

# Enhanced styling with background
st.markdown("""
<style>
/* Main app background */
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%);
}

.main-header {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    padding: 30px 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.class-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid #e2e8f0;
    margin: 10px 0;
}

.enrollment-card {
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin: 15px 0;
}

.stButton > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
}

/* Date selection button styling - applied dynamically */
.date-selection-button {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 2px solid rgba(226, 232, 240, 0.8);
    border-radius: 16px;
    padding: 24px 20px;
    min-height: 120px;
    color: #0f172a;
    font-size: 14px;
    white-space: pre-line;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    text-align: center;
}

.date-selection-button:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    border-color: #3b82f6;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

/* Enrollment link styling */
.enrollment-card a {
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    color: white !important;
    text-decoration: none !important;
    padding: 12px 20px;
    border-radius: 8px;
    font-weight: 600;
    display: inline-block;
    transition: all 0.3s ease;
}

.enrollment-card a:hover {
    background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'test_date' not in st.session_state:
    st.session_state.test_date = None
if 'selected_classes' not in st.session_state:
    st.session_state.selected_classes = []

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

# Varsity Tutors SAT Course Catalog
COURSE_CATALOG = {
    "SAT 2-Week Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-two-week-bootcamp/dp/e34ad454-d5a7-4851-9694-cdd64675b3d8",
        "description": "Intensive 2-week prep course focusing on SAT strategies and key concepts",
        "duration": "2 weeks, 4x per week",
        "best_for": "Fast-track preparation",
        "recommended_timeline": "urgent"
    },
    "SAT 4-Week Prep Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-four-week-prep-course/dp/e3a6e856-31db-429d-a52f-dfbbc93c2edd", 
        "description": "Comprehensive 4-week SAT preparation covering all sections",
        "duration": "4 weeks",
        "best_for": "Thorough preparation with moderate timeline",
        "recommended_timeline": "good"
    },
    "SAT Prep Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-prep-course/dp/c85c2298-bd6a-4cd4-be0d-8f4f35d3f7eb",
        "description": "Extended comprehensive SAT preparation course",
        "duration": "8+ weeks",
        "best_for": "Complete preparation with plenty of time",
        "recommended_timeline": "excellent"
    },
    "SAT Math Cram Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-math-cram-session/dp/33f2fab0-1908-4b5c-9d36-966e467af942",
        "description": "Intensive focus on SAT Math section concepts and strategies",
        "duration": "Intensive session",
        "best_for": "Math section improvement",
        "recommended_timeline": "all"
    },
    "SAT Reading/Writing Cram Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-reading-writing-cram-session/dp/03ea8fe7-ff75-4b07-b69e-f3558c1ed44e",
        "description": "Intensive focus on SAT Reading and Writing sections",
        "duration": "Intensive session", 
        "best_for": "Reading and Writing improvement",
        "recommended_timeline": "all"
    },
    "1-Week SAT Math Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-one-week-bootcamp-sat-math-9-12/dp/255ad018-d421-46fb-9e54-210e4045a491",
        "description": "One week intensive bootcamp focused on SAT Math",
        "duration": "1 week",
        "best_for": "Math-focused intensive preparation",
        "recommended_timeline": "urgent"
    },
    "1-Week SAT ELA Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-one-week-bootcamp-sat-ela-9-12/dp/a4621f0a-e935-46ad-beda-de37624b05ba",
        "description": "One week intensive bootcamp focused on SAT Reading and Writing",
        "duration": "1 week",
        "best_for": "Reading and Writing intensive preparation", 
        "recommended_timeline": "urgent"
    },
    "2-Week SAT Math Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-math-sat-9-12/dp/2f67b5be-e283-406f-b4d2-fe3fc17e52aa",
        "description": "Two week intensive course focused on SAT Math",
        "duration": "2 weeks",
        "best_for": "Extended math preparation",
        "recommended_timeline": "good"
    },
    "2-Week SAT ELA Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-ela-sat-9-12/dp/81b322ee-93b3-4389-88af-bf11f7d0240f",
        "description": "Two week intensive course focused on SAT Reading and Writing",
        "duration": "2 weeks", 
        "best_for": "Extended reading and writing preparation",
        "recommended_timeline": "good"
    },
    "Ultimate SAT Review Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-ultimate-sat-review-session/dp/2a08c912-0a50-4639-b097-dfcaa2f591de",
        "description": "Comprehensive review of key SAT concepts and strategies",
        "duration": "Single intensive session",
        "best_for": "Final review before test",
        "recommended_timeline": "all"
    },
    "Proctored Practice SAT": {
        "url": "https://www.varsitytutors.com/courses/vtp-proctored-practiced-sat-9-12/dp/2298ff50-8011-48e7-acc0-c81cb25eeae1",
        "description": "Practice SAT tests under real testing conditions - 3 hour sessions",
        "duration": "3 hours per session",
        "best_for": "Test practice and timing under real conditions",
        "recommended_timeline": "all"
    },
    "PSAT Prep Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-psat-prep-course/dp/50f02afb-2b2b-4f69-8057-dc5b9c53c629",
        "description": "Comprehensive PSAT preparation course for underclassmen",
        "duration": "Multiple weeks",
        "best_for": "PSAT preparation and SAT foundation building",
        "recommended_timeline": "excellent"
    },
    "SAT Math 1-Week Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-one-week-bootcamp-sat-math-9-12/dp/255ad018-d421-46fb-9e54-210e4045a491",
        "description": "Intensive 1-week SAT Math bootcamp with daily sessions",
        "duration": "1 week, 4 sessions",
        "best_for": "Intensive Math preparation with limited time",
        "recommended_timeline": "urgent"
    },
    "SAT Reading & Writing 1-Week Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-one-week-bootcamp-sat-ela-9-12/dp/a4621f0a-e935-46ad-beda-de37624b05ba",
        "description": "Intensive 1-week SAT Reading & Writing bootcamp with daily sessions",
        "duration": "1 week, 4 sessions",
        "best_for": "Intensive ELA preparation with limited time", 
        "recommended_timeline": "urgent"
    },
    "SAT 8-Week Prep Class": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-prep-course/dp/c85c2298-bd6a-4cd4-be0d-8f4f35d3f7eb",
        "description": "Comprehensive 8-week SAT preparation with weekly sessions",
        "duration": "8 weeks, weekly sessions",
        "best_for": "Thorough preparation with extended timeline",
        "recommended_timeline": "excellent"
    },
    "SAT 2-Week Math Review Prep Class": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-math-sat-9-12/dp/2f67b5be-e283-406f-b4d2-fe3fc17e52aa",
        "description": "Focused 2-week Math review and preparation",
        "duration": "2 weeks, weekly sessions",
        "best_for": "Math-focused review preparation",
        "recommended_timeline": "good"
    },
    "SAT 2-Week Reading & Writing Review Prep Class": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-ela-sat-9-12/dp/81b322ee-93b3-4389-88af-bf11f7d0240f",
        "description": "Focused 2-week Reading & Writing review and preparation",
        "duration": "2 weeks, weekly sessions",
        "best_for": "ELA-focused review preparation",
        "recommended_timeline": "good"
    }
}

# Progress indicator
progress_labels = ["Choose Test Date", "Your SAT Prep Journey"]
progress = st.session_state.step / len(progress_labels)
st.progress(progress, text=f"Step {st.session_state.step} of {len(progress_labels)}: {progress_labels[st.session_state.step-1]}")

# Step 1: Test Date Selection
if st.session_state.step == 1:
    # Hero section with background
    st.markdown('''
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -50%;
            right: -10%;
            width: 300px;
            height: 300px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            opacity: 0.5;
        "></div>
        <div style="
            position: absolute;
            bottom: -30%;
            left: -5%;
            width: 200px;
            height: 200px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            opacity: 0.3;
        "></div>
        <div style="position: relative; z-index: 2;">
            <h1 style="color: white; font-size: 3em; margin: 0; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                📚 SAT Success Journey
            </h1>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.3em; margin: 20px 0 0 0; font-weight: 300;">
                Choose your test date and unlock your college dreams
            </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Instruction section with icons
    st.markdown('''
    <div style="text-align: center; margin: 40px 0;">
        <h2 style="color: #1f2937; font-weight: 700; margin-bottom: 20px;">
            🎯 Select Your SAT Test Date
        </h2>
        <p style="color: #6b7280; font-size: 1.1em; max-width: 600px; margin: 0 auto;">
            Pick the date that works best for your schedule. We'll recommend the perfect prep timeline based on your choice.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Filter out past dates
    available_dates = {date_str: date_obj for date_str, date_obj in SAT_DATES.items() 
                      if (date_obj - date.today()).days > 0}
    
    if not available_dates:
        st.error("⚠️ No upcoming SAT dates available. Please check back later.")
    else:
        # Create single column layout for stacked buttons
        st.markdown('<div style="max-width: 700px; margin: 0 auto;">', unsafe_allow_html=True)
        
        for i, (date_str, date_obj) in enumerate(available_dates.items()):
            days_until = (date_obj - date.today()).days
            
            # Determine status and styling
            if days_until > 56:
                status = "excellent"
                status_text = "🌟 Perfect Timeline"
                status_desc = "Plenty of time for comprehensive prep"
                status_class = "excellent"
                icon = "🚀"
                gradient = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
                border_color = '#10b981'
            elif days_until > 28:
                status = "good"
                status_text = "⚡ Intensive Prep"
                status_desc = "Good timeline for focused preparation"
                status_class = "good" 
                icon = "💪"
                gradient = "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"
                border_color = '#f59e0b'
            else:
                status = "urgent"
                status_text = "🎯 Rush Mode"
                status_desc = "Focused crash course needed"
                status_class = "urgent"
                icon = "⚡"
                gradient = "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
                border_color = '#ef4444'
            
            # Custom CSS for this specific card button
            st.markdown(f'''
            <style>
                .date-button-{i} button {{
                    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
                    border: 2px solid rgba(226, 232, 240, 0.8) !important;
                    border-left: 8px solid {border_color} !important;
                    border-radius: 20px !important;
                    padding: 30px 25px !important;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
                    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
                    overflow: hidden !important;
                    position: relative !important;
                    width: 100% !important;
                    height: auto !important;
                    min-height: 140px !important;
                    color: #1f2937 !important;
                    font-size: 16px !important;
                    font-weight: 600 !important;
                    white-space: pre-line !important;
                    text-align: left !important;
                    line-height: 1.6 !important;
                }}
                
                .date-button-{i} button:hover {{
                    transform: translateY(-8px) scale(1.02) !important;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15) !important;
                    border-color: #3b82f6 !important;
                }}
                
                .date-button-{i} button::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    right: 0;
                    width: 120px;
                    height: 120px;
                    background: {gradient};
                    opacity: 0.1;
                    border-radius: 50%;
                    transform: translate(30%, -30%);
                }}
            </style>
            ''', unsafe_allow_html=True)
            
            # Create simple button text
            button_text = f"{icon} {date_str}\n📅 {days_until} days from today\n{status_text} • {status_desc}"
            
            # Styled container for button
            with st.container():
                st.markdown(f'<div class="date-button-{i}" style="margin: 20px 0;">', unsafe_allow_html=True)
                if st.button(button_text, key=f"date_{i}", use_container_width=True, help=f"Select {date_str} as your SAT test date"):
                    st.session_state.test_date = date_str
                    st.session_state.step = 2
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add motivational footer section
        st.markdown('''
        <div style="
            margin: 60px 0 20px 0;
            padding: 40px;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border-radius: 20px;
            text-align: center;
            border: 1px solid rgba(59, 130, 246, 0.1);
        ">
            <h3 style="color: #1e40af; margin: 0 0 15px 0; font-weight: 700;">
                🎯 Ready to Achieve Your Best SAT Score?
            </h3>
            <p style="color: #475569; font-size: 1.1em; margin: 0; max-width: 500px; margin: 0 auto;">
                Choose your test date above and let's create your personalized prep plan with expert-led classes from Varsity Tutors.
            </p>
        </div>
        ''', unsafe_allow_html=True)

# Step 2: Class Selection
elif st.session_state.step == 2:
    target_date_obj = SAT_DATES[st.session_state.test_date]
    days_until = (target_date_obj - date.today()).days
    
    # Hero section for class selection
    st.markdown(f'''
    <div style="
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        padding: 50px 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -20%;
            right: -10%;
            width: 200px;
            height: 200px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
        "></div>
        <div style="position: relative; z-index: 2;">
            <h1 style="color: white; font-size: 2.5em; margin: 0; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                📚 Your Personalized Study Plan
            </h1>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.2em; margin: 15px 0 0 0;">
                SAT Date: {st.session_state.test_date} • {days_until} days to prepare
            </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Determine timeline category and create schedule
    if days_until > 56:
        timeline_status = "excellent"
        timeline_color = "#22c55e"
        timeline_text = "🌟 Perfect Timeline"
        weeks_available = days_until // 7
        recommended_classes = list(COURSE_CATALOG.keys())
        
        # Create weekly schedule for excellent timeline
        schedule = [
            {"weeks": "Week 1-8", "course": "SAT Prep Course", "focus": "Foundation Building", "icon": "📚"},
            {"weeks": "Week 9-10", "course": "2-Week SAT Math Course", "focus": "Math Mastery", "icon": "🔢"},
            {"weeks": "Week 11-12", "course": "2-Week SAT ELA Course", "focus": "Reading & Writing", "icon": "📖"},
            {"weeks": "Week 13", "course": "Ultimate SAT Review Session", "focus": "Final Review", "icon": "🎯"},
            {"weeks": "Ongoing", "course": "Proctored Practice SAT", "focus": "Test Practice", "icon": "📝"}
        ]
        
    elif days_until > 28:
        timeline_status = "good"
        timeline_color = "#f59e0b"
        timeline_text = "⚡ Intensive Timeline"
        weeks_available = days_until // 7
        recommended_classes = [
            "SAT 4-Week Prep Course", "SAT 2-Week Bootcamp", "2-Week SAT Math Course", 
            "2-Week SAT ELA Course", "SAT Math Cram Session", "SAT Reading/Writing Cram Session",
            "Ultimate SAT Review Session", "Proctored Practice SAT"
        ]
        
        # Create weekly schedule for good timeline
        schedule = [
            {"weeks": "Week 1-4", "course": "SAT 4-Week Prep Course", "focus": "Core Concepts", "icon": "📚"},
            {"weeks": "Week 5-6", "course": "2-Week SAT Math Course", "focus": "Math Focus", "icon": "🔢"},
            {"weeks": "Week 7", "course": "SAT Reading/Writing Cram Session", "focus": "ELA Boost", "icon": "📖"},
            {"weeks": "Week 8", "course": "Ultimate SAT Review Session", "focus": "Final Prep", "icon": "🎯"},
            {"weeks": "Weekly", "course": "Proctored Practice SAT", "focus": "Practice Tests", "icon": "📝"}
        ]
        
    else:
        timeline_status = "urgent"
        timeline_color = "#ef4444"
        timeline_text = "🚨 Rush Timeline"
        weeks_available = max(days_until // 7, 2)
        recommended_classes = [
            "SAT 2-Week Bootcamp", "1-Week SAT Math Bootcamp", "1-Week SAT ELA Bootcamp",
            "SAT Math Cram Session", "SAT Reading/Writing Cram Session", "Ultimate SAT Review Session",
            "Proctored Practice SAT"
        ]
        
        # Create weekly schedule for urgent timeline
        schedule = [
            {"weeks": "Week 1-2", "course": "SAT 2-Week Bootcamp", "focus": "Essential Skills", "icon": "🚀"},
            {"weeks": "Week 3", "course": "1-Week SAT Math Bootcamp", "focus": "Math Intensive", "icon": "🔢"},
            {"weeks": "Week 4", "course": "SAT Reading/Writing Cram Session", "focus": "ELA Cram", "icon": "📖"},
            {"weeks": "Final Days", "course": "Ultimate SAT Review Session", "focus": "Last Review", "icon": "🎯"},
            {"weeks": "Ongoing", "course": "Proctored Practice SAT", "focus": "Practice", "icon": "📝"}
        ]
    
    # Display SAT prep journey timeline
    st.markdown(f'''
    <div style="margin: 40px 0;">
        <div style="text-align: center; margin-bottom: 40px;">
            <h2 style="color: #1f2937; margin-bottom: 15px; font-size: 2.2em;">
                🚀 Your SAT Success Journey
            </h2>
            <p style="color: #6b7280; font-size: 1.2em; margin-bottom: 20px;">
                Follow this personalized timeline to maximize your SAT score
            </p>
            <span style="
                background: {timeline_color};
                color: white;
                padding: 12px 25px;
                border-radius: 30px;
                font-weight: 700;
                font-size: 1.1em;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            ">
                {timeline_text} • {weeks_available} weeks to prepare
            </span>
        </div>
        
    ''', unsafe_allow_html=True)
    
    # Create step-by-step timeline using Streamlit components
    for step_number, item in enumerate(schedule, 1):
        # Create container for each step
        with st.container():
            # Add some custom styling for the container
            st.markdown(f"""
            <style>
            .step-container-{step_number} {{
                background: white;
                padding: 30px;
                border-radius: 20px;
                border: 2px solid #e2e8f0;
                margin: 20px 0;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                position: relative;
            }}
            .step-badge-{step_number} {{
                background: {timeline_color};
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: 700;
                font-size: 0.9em;
                margin-bottom: 15px;
                display: inline-block;
            }}
            </style>
            """, unsafe_allow_html=True)
            
            #st.markdown(f'<div class="step-container-{step_number}">', unsafe_allow_html=True)
            
            # Step badge
            st.markdown(f'<span class="step-badge-{step_number}">{item["icon"]} STEP {step_number}</span>', unsafe_allow_html=True)
            
            # Course title and details
            st.markdown(f"### {item['course']}")
            st.markdown(f"**{item['focus']}** • *{item['weeks']}*")
            
            # Course description  
            course_desc = COURSE_CATALOG.get(item['course'], {}).get('description', 'Complete your SAT preparation with this essential course.')
            st.info(f"📚 {course_desc}")
            
            # Enrollment button
            course_info = COURSE_CATALOG.get(item['course'], {})
            if course_info and course_info.get('url'):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <a href="{course_info['url']}" target="_blank" 
                           style="background: {timeline_color}; color: white; padding: 15px 30px; 
                                  border-radius: 12px; text-decoration: none; font-weight: 700; 
                                  font-size: 1.1em; display: inline-block;">
                           🎯 Enroll in Step {step_number}
                        </a>
                        <p style="color: #6b7280; font-size: 0.9em; margin-top: 10px; font-style: italic;">
                            Click to view available class times and enroll at Varsity Tutors
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add some space between steps
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Add motivational closing using native Streamlit components
    st.markdown("---")
    st.markdown("### 🎯 Your Path to SAT Success")
    st.markdown("""
    Follow this personalized timeline step-by-step to maximize your score improvement. 
    Each course builds upon the previous one, creating a comprehensive prep experience 
    that keeps you engaged all the way to test day!
    """)
    st.info("📞 **Questions? Call Varsity Tutors: (800) 803-4058**")
    # Navigation back to step 1
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("← Back to Test Date Selection", key="back_to_step1", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown("**SAT Class Finder** - Connecting students with Varsity Tutors SAT preparation classes") 

import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

# =============================================
#  Simplified SAT Class Finder 
#  Connect students with Varsity Tutors SAT classes
# =============================================

st.set_page_config(page_title="SAT Class Finder", page_icon="📚", layout="wide")

# Professional Design System
st.markdown("""
<style>
/* Design System */
:root {
    /* Color system */
    --bg: #f7f9fc;            /* app canvas */
    --surface: #ffffff;       /* cards */
    --ink: #0f172a;           /* primary text */
    --ink-muted: #475569;     /* secondary text */
    --primary: #2563eb;       /* accent (links, buttons) */
    --primary-ink: #ffffff;   /* on-primary */
    --border: #e2e8f0;        /* hairlines */
    --info-bg: #e8f0ff;       /* light info banner */
    --info-ink: #1d4ed8;

    /* Radii & elevation */
    --radius-sm: .5rem;       /* 8px */
    --radius-lg: 1rem;        /* 16px */
    --shadow-sm: 0 1px 2px rgba(0,0,0,.06);
    --shadow-md: 0 6px 16px rgba(15, 23, 42, .08);

    /* Type scale (clamp for responsive) */
    --h1: clamp(2rem, 1.5rem + 2vw, 3rem);
    --h2: clamp(1.25rem, 1rem + 1.2vw, 1.75rem);
    --h3: 1.125rem;
    --body: 1rem;
    --small: .9375rem;

    /* Spacing (8pt grid) */
    --s-1: .5rem;
    --s-2: 1rem;
    --s-3: 1.5rem;
    --s-4: 2rem;
}

/* Typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

body {
    background: var(--bg); 
    color: var(--ink); 
    line-height: 1.5; 
    font-feature-settings: "ss01", "tnum";
}

/* Base Layout */
.stApp {
    background: var(--bg);
}

.main > div {
    max-width: 1120px;
    margin: 0 auto;
    padding: var(--s-4) var(--s-2);
}

h1 {
    font-size: var(--h1); 
    font-weight: 800; 
    letter-spacing: -0.01em;
    color: var(--ink);
}

h2 {
    font-size: var(--h2); 
    font-weight: 700;
    color: var(--ink);
}

h3 {
    font-size: var(--h3); 
    font-weight: 600;
    color: var(--ink);
}

p, li {
    font-size: var(--body); 
    color: var(--ink-muted);
}

/* Stepper Component */
.stepper {
    display: grid; 
    grid-template-columns: repeat(4, 1fr); 
    gap: var(--s-4); 
    margin-top: var(--s-2);
}

.step {
    display: flex; 
    gap: 0.75rem; 
    align-items: center;
}

.dot {
    width: 14px; 
    height: 14px; 
    border-radius: 999px;
    background: var(--primary); 
    box-shadow: 0 0 0 4px #dbeafe;
}

.step label {
    font-weight: 600; 
    color: var(--ink);
}

.step small {
    display: block; 
    color: var(--ink-muted);
}

@media (max-width: 720px) { 
    .stepper {
        grid-template-columns: 1fr 1fr;
    } 
}

/* Course Cards */
.course-card {
    background: var(--surface); 
    border: 1px solid var(--border);
    border-radius: var(--radius-lg); 
    padding: var(--s-3); 
    box-shadow: var(--shadow-md);
    margin-bottom: var(--s-3);
}

.info-banner {
    background: var(--info-bg); 
    color: var(--ink);
    border: 1px solid #dbeafe; 
    border-radius: var(--radius-lg);
    padding: var(--s-2); 
    box-shadow: var(--shadow-sm);
}

.info-text {
    color: var(--info-ink);
}

/* Time slot chips */
.time-slots {
    display: grid; 
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); 
    gap: var(--s-2); 
    list-style: none; 
    padding: 0;
    margin-top: var(--s-2);
}

.time-slot {
    border: 1px solid var(--border); 
    border-radius: var(--radius-sm); 
    padding: 0.75rem; 
    background: var(--surface);
}

.time-slot-title {
    font-weight: 600;
    color: var(--ink);
}

.time-slot-details {
    font-size: var(--small); 
    color: var(--ink-muted);
}

.step.inactive {
    background: var(--gray-100);
    color: var(--gray-500);
}

.step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    font-weight: 700;
    font-size: 0.75rem;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, var(--brand-600) 0%, var(--brand-800) 100%);
    color: white;
    padding: 3rem 2rem;
    margin: -2rem -2rem 2rem -2rem;
    border-radius: 0 0 24px 24px;
    text-align: center;
}

.hero h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0 0 1rem 0;
    letter-spacing: -0.025em;
}

.hero p {
    font-size: 1.125rem;
    opacity: 0.9;
    margin: 0;
    font-weight: 400;
}

/* Course Cards */
.course-card {
    background: white;
    border: 1px solid var(--gray-200);
    border-top: 4px solid var(--brand-600);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 150ms ease;
}

.course-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
}

.course-card h3 {
    font-size: 1.25rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    color: var(--gray-900);
}

.course-card .subtitle {
    color: var(--gray-600);
    font-size: 0.875rem;
    margin: 0 0 1rem 0;
}

.course-card .description {
    background: var(--brand-50);
    padding: 1rem;
    border-radius: 12px;
    border-left: 4px solid var(--brand-600);
    font-size: 0.875rem;
    color: var(--gray-700);
    margin: 1rem 0;
}

/* Time Chips */
.time-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1rem 0;
}

.time-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    border: 2px solid var(--gray-200);
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 500;
    transition: all 150ms ease;
    cursor: pointer;
    background: white;
    color: var(--gray-700);
}

.time-chip:hover {
    border-color: var(--brand-300);
    background: var(--brand-50);
}

.time-chip.selected {
    border-color: var(--brand-600);
    background: var(--brand-600);
    color: white;
}

.time-chip .checkmark {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--success-500);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: white;
}

/* Buttons */
.stButton button {
    background: var(--brand-600) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.875rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    transition: all 150ms ease !important;
    font-family: 'Inter', sans-serif !important;
}

.stButton button:hover {
    background: var(--brand-700) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
}

/* Secondary Button */
div[data-testid="column"] .stButton button {
    background: var(--gray-100) !important;
    color: var(--gray-700) !important;
}

div[data-testid="column"] .stButton button:hover {
    background: var(--gray-200) !important;
    color: var(--gray-800) !important;
}

/* Primary CTA */
.primary-cta .stButton button {
    background: var(--brand-600) !important;
    color: white !important;
    font-size: 1rem !important;
    padding: 1rem 2rem !important;
}

/* Form Elements */
.stSelectbox > div > div {
    border-radius: 12px !important;
    border: 2px solid var(--gray-200) !important;
    font-family: 'Inter', sans-serif !important;
}

.stRadio > div {
    gap: 0.75rem !important;
}

.stRadio label {
    font-weight: 500 !important;
    font-size: 0.875rem !important;
}

/* Info/Warning/Error Boxes */
.stInfo {
    background: var(--brand-50) !important;
    border-left: 4px solid var(--brand-600) !important;
    border-radius: 12px !important;
}

.stSuccess {
    background: #f0fdf4 !important;
    border-left: 4px solid var(--success-500) !important;
    border-radius: 12px !important;
}

.stWarning {
    background: #fffbeb !important;
    border-left: 4px solid var(--warning-500) !important;
    border-radius: 12px !important;
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 300ms ease-out;
}

/* Focus States */
button:focus,
.time-chip:focus {
    outline: 2px solid var(--brand-600);
    outline-offset: 2px;
}

/* CTA Button Hover Effects */
.cta-button:hover {
    background: var(--brand-700) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
}

/* Progress Bar Override */
.stProgress > div > div > div > div {
    background-color: var(--brand-600) !important;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'test_date' not in st.session_state:
    st.session_state.test_date = None
if 'selected_classes' not in st.session_state:
    st.session_state.selected_classes = []
if 'availability' not in st.session_state:
    st.session_state.availability = {
        'day_preference': 'both',  # 'weekdays', 'weekends', or 'both'
        'time_preference': 'both',  # 'morning', 'evening', or 'both'
        'filter_enabled': False  # Whether to apply filtering or show all classes
    }

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
        "recommended_timeline": "urgent",
        "available_times": [
            "Aug 31 - Sep 10: Sun, Mon, Tue, Wed @ 6:30 PM ET",
            "Sep 21 - Oct 1: Sun, Mon, Tue, Wed @ 7:00 PM ET",
            "Oct 27 - Nov 6: Mon, Tue, Wed, Thu @ 7:00 PM ET",
            "Mar 1 - Mar 11: Sun, Mon, Tue, Wed @ 7:00 PM ET",
            "Apr 19 - Apr 29: Sun, Mon, Tue, Wed @ 7:00 PM ET"
        ]
    },
    "SAT 4-Week Prep Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-four-week-prep-course/dp/e3a6e856-31db-429d-a52f-dfbbc93c2edd", 
        "description": "Comprehensive 4-week SAT preparation covering all sections",
        "duration": "4 weeks",
        "best_for": "Thorough preparation with moderate timeline",
        "recommended_timeline": "good",
        "available_times": [
            "Sep 4 - Sep 25: Thu @ 9:00 PM ET",
            "Sep 6 - Sep 27: Sat @ 11:30 AM ET",
            "Sep 9 - Sep 30: Tue @ 6:00 PM ET",
            "Oct 9 - Oct 30: Thu @ 8:30 PM ET",
            "Oct 12 - Nov 2: Sun @ 5:00 PM ET",
            "Oct 15 - Nov 5: Wed @ 6:00 PM ET",
            "Nov 3 - Nov 24: Mon @ 9:00 PM ET",
            "Nov 9 - Nov 30: Sun @ 4:30 PM ET",
            "Nov 11 - Dec 2: Tue @ 7:00 PM ET"
        ]
    },
    "SAT Prep Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-prep-course/dp/c85c2298-bd6a-4cd4-be0d-8f4f35d3f7eb",
        "description": "Extended comprehensive SAT preparation course",
        "duration": "8+ weeks",
        "best_for": "Complete preparation with plenty of time",
        "recommended_timeline": "excellent",
        "available_times": [
            "Sep 11 - Oct 30: Thu @ 5:30 PM ET",
            "Sep 13 - Nov 1: Sat @ 12:00 PM ET",
            "Sep 16 - Nov 4: Tue @ 8:00 PM ET",
            "Oct 7 - Nov 25: Tue @ 5:30 PM ET",
            "Oct 11 - Nov 29: Sat @ 10:00 AM ET",
            "Oct 13 - Dec 1: Mon @ 8:00 PM ET"
        ]
    },
    "SAT Math Cram Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-math-cram-session/dp/33f2fab0-1908-4b5c-9d36-966e467af942",
        "description": "Intensive focus on SAT Math section concepts and strategies",
        "duration": "Intensive session",
        "best_for": "Math section improvement",
        "recommended_timeline": "all",
        "available_times": [
            "Sep 7: Sun @ 6:30 PM ET",
            "Sep 10: Wed @ 9:00 PM ET",
            "Sep 28: Sun @ 6:00 PM ET",
            "Oct 1: Wed @ 9:00 PM ET",
            "Nov 2: Sun @ 6:30 PM ET",
            "Nov 5: Wed @ 9:00 PM ET",
            "Nov 30: Sun @ 6:30 PM ET"
        ]
    },
    "SAT Reading/Writing Cram Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-reading-writing-cram-session/dp/03ea8fe7-ff75-4b07-b69e-f3558c1ed44e",
        "description": "Intensive focus on SAT Reading and Writing sections",
        "duration": "Intensive session", 
        "best_for": "Reading and Writing improvement",
        "recommended_timeline": "all",
        "available_times": [
            "Sep 7: Sun @ 4:30 PM ET",
            "Sep 8: Mon @ 7:00 PM ET",
            "Sep 28: Sun @ 6:00 PM ET",
            "Sep 29: Mon @ 7:00 PM ET",
            "Nov 2: Sun @ 4:30 PM ET",
            "Nov 3: Mon @ 7:30 PM ET",
            "Nov 30: Sun @ 5:30 PM ET",
            "Dec 1: Mon @ 7:30 PM ET"
        ]
    },
    "1-Week SAT Math Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-one-week-bootcamp-sat-math-9-12/dp/255ad018-d421-46fb-9e54-210e4045a491",
        "description": "One week intensive bootcamp focused on SAT Math",
        "duration": "1 week",
        "best_for": "Math-focused intensive preparation",
        "recommended_timeline": "urgent",
        "available_times": [
            "Sep 7-10: Sun, Mon, Tue, Wed @ 8:00 PM ET",
            "Sep 28 - Oct 1: Sun, Mon, Tue, Wed @ 8:00 PM ET",
            "Nov 2-5: Sun, Mon, Tue, Wed @ 8:30 PM ET",
            "Nov 30 - Dec 3: Sun, Mon, Tue, Wed @ 8:30 PM ET",
            "Dec 27-30: Sat, Sun, Mon, Tue @ 2:00 PM ET",
            "Mar 8-11: Sun, Mon, Tue, Wed @ 8:30 PM ET"
        ]
    },
    "1-Week SAT ELA Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-one-week-bootcamp-sat-ela-9-12/dp/a4621f0a-e935-46ad-beda-de37624b05ba",
        "description": "One week intensive bootcamp focused on SAT Reading and Writing",
        "duration": "1 week",
        "best_for": "Reading and Writing intensive preparation", 
        "recommended_timeline": "urgent",
        "available_times": [
            "Sep 7-10: Sun, Mon, Tue, Wed @ 8:00 PM ET",
            "Sep 28 - Oct 1: Sun, Mon, Tue, Wed @ 8:00 PM ET",
            "Nov 2-5: Sun, Mon, Tue, Wed @ 8:30 PM ET",
            "Nov 30 - Dec 3: Sun, Mon, Tue, Wed @ 8:30 PM ET",
            "Dec 27-30: Sat, Sun, Mon, Tue @ 2:00 PM ET",
            "Mar 8-11: Sun, Mon, Tue, Wed @ 8:30 PM ET"
        ]
    },
    "2-Week SAT Math Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-math-sat-9-12/dp/2f67b5be-e283-406f-b4d2-fe3fc17e52aa",
        "description": "Two week intensive course focused on SAT Math",
        "duration": "2 weeks",
        "best_for": "Extended math preparation",
        "recommended_timeline": "good",
        "available_times": [
            "Sep 4-11: Thu @ 8:00 PM ET",
            "Sep 20-27: Sat @ 3:30 PM ET",
            "Oct 26 - Nov 2: Sun @ 1:00 PM ET",
            "Nov 23-30: Sun @ 2:00 PM ET"
        ]
    },
    "2-Week SAT ELA Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-ela-sat-9-12/dp/81b322ee-93b3-4389-88af-bf11f7d0240f",
        "description": "Two week intensive course focused on SAT Reading and Writing",
        "duration": "2 weeks", 
        "best_for": "Extended reading and writing preparation",
        "recommended_timeline": "good",
        "available_times": [
            "Sep 4-11: Thu @ 8:00 PM ET",
            "Sep 20-27: Sat @ 3:30 PM ET",
            "Oct 26 - Nov 2: Sun @ 1:00 PM ET",
            "Nov 23-30: Sun @ 2:00 PM ET"
        ]
    },
    "Ultimate SAT Review Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-ultimate-sat-review-session/dp/2a08c912-0a50-4639-b097-dfcaa2f591de",
        "description": "Comprehensive review of key SAT concepts and strategies",
        "duration": "Single intensive session",
        "best_for": "Final review before test",
        "recommended_timeline": "all",
        "available_times": [
            "Sep 6: Fri @ 1:00 PM ET",
            "Sep 9: Mon @ 9:00 PM ET",
            "Sep 27: Fri @ 11:00 AM ET",
            "Sep 30: Mon @ 9:00 PM ET",
            "Nov 1: Fri @ 3:00 PM ET",
            "Nov 4: Mon @ 9:30 PM ET",
            "Nov 29: Fri @ 2:00 PM ET",
            "Dec 2: Mon @ 9:00 PM ET"
        ]
    },
    "Proctored Practice SAT": {
        "url": "https://www.varsitytutors.com/courses/vtp-proctored-practiced-sat-9-12/dp/2298ff50-8011-48e7-acc0-c81cb25eeae1",
        "description": "Practice SAT tests under real testing conditions - 3 hour sessions",
        "duration": "3 hours per session",
        "best_for": "Test practice and timing under real conditions",
        "recommended_timeline": "all",
        "available_times": [
            "Aug 30: Fri @ 12:00 PM ET",
            "Sep 6: Fri @ 11:00 AM ET",
            "Sep 13: Fri @ 12:00 PM ET",
            "Sep 20: Fri @ 12:00 PM ET",
            "Sep 27: Fri @ 11:00 AM ET",
            "Oct 4: Fri @ 12:00 PM ET",
            "Oct 11: Fri @ 11:00 AM ET",
            "Oct 18: Fri @ 12:00 PM ET",
            "Nov 1: Fri @ 12:00 PM ET",
            "Nov 8: Fri @ 11:00 AM ET",
            "Nov 15: Fri @ 12:00 PM ET",
            "Dec 13: Fri @ 12:00 PM ET"
        ]
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

# Helper function to check if course matches simplified availability
def matches_availability(course_times, day_preference, time_preference, filter_enabled, unavailable_days=None):
    """
    Check if any of the course times match the user's simplified availability preferences
    """
    if not filter_enabled:
        return True  # Show all classes if filtering is disabled
    
    if unavailable_days is None:
        unavailable_days = []
    
    for time_slot in course_times:
        time_lower = time_slot.lower()
        
        # Enhanced day mapping to catch all possible variants
        day_mapping = {
            'Monday': ['mon', 'monday', 'mo'],
            'Tuesday': ['tue', 'tuesday', 'tues', 'tu'],
            'Wednesday': ['wed', 'wednesday', 'we'],
            'Thursday': ['thu', 'thursday', 'thurs', 'th'],
            'Friday': ['fri', 'friday', 'fr'],
            'Saturday': ['sat', 'saturday', 'sa'],
            'Sunday': ['sun', 'sunday', 'su']
        }
        
        # First, check if course falls on any unavailable days
        is_on_unavailable_day = False
        if unavailable_days:
            for unavailable_day in unavailable_days:
                day_variants = day_mapping.get(unavailable_day, [])
                if any(variant in time_lower for variant in day_variants):
                    is_on_unavailable_day = True
                    break
        
        # Skip this time slot if it's on an unavailable day
        if is_on_unavailable_day:
            continue
        
        # Then check general day preference (weekdays vs weekends)
        # This now only applies to days that are NOT in the unavailable list
        day_preference_match = True  # Default to match if no specific day preference
        
        if day_preference == 'weekdays':
            # Check if it's Monday-Friday, but exclude any unavailable days
            available_weekdays = []
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                if day not in unavailable_days:
                    available_weekdays.extend(day_mapping[day])
            
            day_preference_match = any(day_abbrev in time_lower for day_abbrev in available_weekdays)
            
        elif day_preference == 'weekends':
            # Check if it's Saturday-Sunday, but exclude any unavailable days  
            available_weekends = []
            for day in ['Saturday', 'Sunday']:
                if day not in unavailable_days:
                    available_weekends.extend(day_mapping[day])
            
            day_preference_match = any(day_abbrev in time_lower for day_abbrev in available_weekends)
        
        if not day_preference_match:
            continue
        
        # Check time preference  
        time_match = True  # Default to match if no specific time preference
        if time_preference == 'morning':
            # Morning: 9 AM - 3 PM
            morning_hours = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM"]
            time_match = any(hour in time_slot for hour in morning_hours)
        elif time_preference == 'evening':
            # Evening: 4 PM - 11 PM  
            evening_hours = ["4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM"]
            time_match = any(hour in time_slot for hour in evening_hours)
        
        if time_match:
            return True
    
    return False

def get_filter_reason(course_times, day_preference, time_preference, filter_enabled, unavailable_days=None):
    """
    Get the specific reason why a course was filtered out with simplified preferences
    """
    if not filter_enabled:
        return "No filters applied"
    
    if unavailable_days is None:
        unavailable_days = []
    
    reasons = []
    
    # Enhanced day mapping
    day_mapping = {
        'Monday': ['mon', 'monday', 'mo'],
        'Tuesday': ['tue', 'tuesday', 'tues', 'tu'],
        'Wednesday': ['wed', 'wednesday', 'we'],
        'Thursday': ['thu', 'thursday', 'thurs', 'th'],
        'Friday': ['fri', 'friday', 'fr'],
        'Saturday': ['sat', 'saturday', 'sa'],
        'Sunday': ['sun', 'sunday', 'su']
    }
    
    for time_slot in course_times:
        time_lower = time_slot.lower()
        
        # Check if course falls on unavailable days
        for unavailable_day in unavailable_days:
            day_variants = day_mapping.get(unavailable_day, [])
            if any(variant in time_lower for variant in day_variants):
                reasons.append(f"Scheduled on {unavailable_day} (you're not available)")
                break
        
        # Check day preference conflicts
        if day_preference == 'weekdays':
            weekends = ['sat', 'sun']
            if any(day in time_lower for day in weekends):
                if any(d in ['Saturday', 'Sunday'] for d in unavailable_days):
                    reasons.append(f"Scheduled on weekends (unavailable)")
                else:
                    reasons.append("Scheduled on weekends (you prefer weekdays)")
        elif day_preference == 'weekends':
            weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
            if any(day in time_lower for day in weekdays):
                weekday_conflicts = [d for d in unavailable_days if d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]
                if weekday_conflicts:
                    reasons.append(f"Scheduled on unavailable weekdays")
                else:
                    reasons.append("Scheduled on weekdays (you prefer weekends)")
        
        # Check time conflicts
        if time_preference == 'morning':
            evening_hours = ["4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM"]
            if any(hour in time_slot for hour in evening_hours):
                reasons.append("Scheduled in evening (you prefer morning)")
        elif time_preference == 'evening':
            morning_hours = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM"]
            if any(hour in time_slot for hour in morning_hours):
                reasons.append("Scheduled in morning (you prefer evening)")
    
    return " • ".join(list(set(reasons))) if reasons else "Doesn't match your preferences"

def filter_schedule_with_tracking(original_schedule, day_preference, time_preference, filter_enabled, unavailable_days=None):
    """
    Filter schedule and track what gets filtered out with simplified preferences
    """
    if unavailable_days is None:
        unavailable_days = []
        
    filtered_schedule = []
    filtered_out = []
    
    for item in original_schedule:
        course_info = COURSE_CATALOG.get(item['course'], {})
        course_times = course_info.get('available_times', [])
        
        if matches_availability(course_times, day_preference, time_preference, filter_enabled, unavailable_days):
            filtered_schedule.append(item)
        else:
            # Track what was filtered out and why
            reason = get_filter_reason(course_times, day_preference, time_preference, filter_enabled, unavailable_days)
            filtered_out.append({
                'item': item,
                'reason': reason,
                'times': course_times[:3] if len(course_times) > 3 else course_times  # Show first 3 times
            })
    
    return filtered_schedule, filtered_out

def generate_suggested_sequence(schedule, availability):
    """
    Generate an optimal sequence of classes based on user availability and class dates
    """
    if not availability.get('filter_enabled', False):
        return None
    
    # Get user preferences
    day_preference = availability.get('day_preference', 'both')
    time_preference = availability.get('time_preference', 'both')
    unavailable_days = availability.get('unavailable_days', [])
    
    # Find matching classes with their best times
    sequence = []
    
    for item in schedule:
        course_info = COURSE_CATALOG.get(item['course'], {})
        available_times = course_info.get('available_times', [])
        
        if not available_times:
            continue
            
        # Find times that match user preferences
        matching_times = []
        for time_slot in available_times:
            if matches_availability([time_slot], day_preference, time_preference, True, unavailable_days):
                matching_times.append(time_slot)
        
        if matching_times:
            # Parse dates to suggest optimal timing
            suggested_timing = get_suggested_timing(item['course'], matching_times)
            
            sequence.append({
                'course': item['course'],
                'weeks': item['weeks'],
                'focus': item['focus'],
                'icon': item['icon'],
                'suggested_times': matching_times[:2],  # Top 2 matches
                'suggested_timing': suggested_timing
            })
    
    # Sort sequence for optimal learning progression
    return sort_optimal_sequence(sequence)

def get_suggested_timing(course_name, matching_times):
    """
    Extract and format timing information from matching times
    """
    if not matching_times:
        return "Contact for schedule"
        
    # Parse the first matching time for date range
    first_time = matching_times[0]
    
    # Extract date patterns from time strings
    if "Sep" in first_time and "Oct" in first_time:
        return "September 4 - October 30 (8 weeks)"
    elif "Sep" in first_time:
        if "2-Week" in course_name or "Math" in course_name:
            return "September 4-11 (2 weeks)"
        else:
            return "September start"
    elif "Oct" in first_time:
        if "2-Week" in course_name:
            return "October 26 - November 2 (2 weeks)"
        else:
            return "October start"
    elif "Nov" in first_time:
        if "2-Week" in course_name:
            return "November 23-30 (2 weeks)"
        else:
            return "November start"
    else:
        return "See available times"

def sort_optimal_sequence(sequence):
    """
    Sort courses in optimal learning order (foundation -> specific -> final review)
    """
    if not sequence:
        return []
    
    # Define course priority order for optimal learning
    priority_order = [
        "SAT Prep Course",           # Foundation first
        "SAT 4-Week Prep Course",    # Alternative foundation
        "SAT 8-Week Prep Class",     # Extended foundation
        "2-Week SAT Math Course",    # Subject-specific
        "SAT Math 1-Week Bootcamp",  # Math intensive
        "2-Week SAT ELA Course",     # ELA specific  
        "SAT Reading & Writing 1-Week Bootcamp",  # ELA intensive
        "SAT 2-Week Bootcamp",       # General intensive
        "Ultimate SAT Review Session", # Final review
        "Proctored Practice SAT"      # Practice tests throughout
    ]
    
    sorted_sequence = []
    
    # Add courses in priority order
    for course_name in priority_order:
        for item in sequence:
            if item['course'] == course_name:
                sorted_sequence.append(item)
                break
    
    # Add any remaining courses not in priority list
    for item in sequence:
        if item not in sorted_sequence:
            sorted_sequence.append(item)
    
    return sorted_sequence[:4]  # Limit to top 4 recommendations

# Branded Stepper Component
progress_labels = ["Quick set up", "Your SAT prep journey"]

def render_stepper(current_step):
    # Use completely native Streamlit components
    st.markdown("---")
    
    # Create step indicators using columns  
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Step progress display
        step_text = ""
        for i, label in enumerate(progress_labels, 1):
            if i < current_step:
                step_text += f"✅ **{label}**"
            elif i == current_step:
                step_text += f"🔵 **{label}** _(current)_"
            else:
                step_text += f"⚪ {label}"
            
            if i < len(progress_labels):
                step_text += " → "
        
        st.markdown(step_text)
    
    st.markdown("---")

# Render the stepper
render_stepper(st.session_state.step)

# Step 1: Quick Setup (Test Date + Simplified Availability)
if st.session_state.step == 1:
    # Visual hero section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🎯 SAT Class Finder")
        st.success("**Find your perfect prep plan in 2 minutes!**")
    
    # Visual progress indicator
    st.progress(0.5, "Step 1 of 2: Quick Setup")
    
    # Test Date Selection Card with visuals
    st.markdown("### 📅 When are you taking the SAT?")
    st.caption("Pick your test date to see your perfect timeline")
    
    # Filter out past dates
    available_dates = {date_str: date_obj for date_str, date_obj in SAT_DATES.items() 
                      if (date_obj - date.today()).days > 0}
    
    if not available_dates:
        st.error("⚠️ No upcoming SAT dates available. Please check back later.")
    else:
        # Date selection in a container
        col1, col2 = st.columns([3, 2])
        with col1:
            selected_date = st.selectbox(
                "Select your test date:",
                options=list(available_dates.keys()),
                index=0 if not st.session_state.test_date else list(available_dates.keys()).index(st.session_state.test_date) if st.session_state.test_date in available_dates else 0,
                help="Choose when you plan to take the SAT",
                label_visibility="collapsed"
            )
            st.session_state.test_date = selected_date
            
        with col2:
            # Show timeline info as a neutral indicator
            days_until = (available_dates[selected_date] - date.today()).days
            if days_until > 56:
                timeline_text = "Perfect prep window"
            elif days_until > 28:
                timeline_text = "Focused prep needed"
            else:
                timeline_text = "Intensive prep required"
            
            # Show timeline status with neutral styling
            st.info(f"**Your test is in {days_until} days** — {timeline_text}")
    
    # Visual schedule preferences section
    st.markdown("### ⚙️ Schedule preferences")
    st.caption("Optional: Filter classes to match your availability")
    
    # Visual filter toggle
    filter_enabled = st.checkbox(
        "🎯 Only show classes that fit my schedule", 
        value=st.session_state.availability['filter_enabled']
    )
    st.session_state.availability['filter_enabled'] = filter_enabled
    
    if filter_enabled:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📅 When can you attend?**")
            day_pref = st.radio(
                "Day preference",
                options=['both', 'weekdays', 'weekends'],
                index=['both', 'weekdays', 'weekends'].index(st.session_state.availability['day_preference']),
                format_func=lambda x: {
                    'both': '🗓️ Any day',
                    'weekdays': '💼 Weekdays only',
                    'weekends': '🏖️ Weekends only'
                }[x],
                label_visibility="collapsed"
            )
            st.session_state.availability['day_preference'] = day_pref
        
        with col2:
            st.markdown("**⏰ What time works best?**")
            time_pref = st.radio(
                "Time preference",
                options=['both', 'morning', 'evening'],
                index=['both', 'morning', 'evening'].index(st.session_state.availability['time_preference']),
                format_func=lambda x: {
                    'both': '🕐 Any time',
                    'morning': '🌅 Morning/afternoon',
                    'evening': '🌆 Evening/night'
                }[x],
                label_visibility="collapsed"
            )
            st.session_state.availability['time_preference'] = time_pref
            
        # Add specific weekday unavailability section
        st.markdown("---")
        st.markdown("**📅 Days you're NOT available**")
        st.caption("Select any weekdays when you cannot attend classes")
        
        # Initialize unavailable_days if not exists
        if 'unavailable_days' not in st.session_state.availability:
            st.session_state.availability['unavailable_days'] = []
        
        # Create visual weekday selection
        days_of_week = {
            'Monday': '📅 Monday',
            'Tuesday': '📅 Tuesday', 
            'Wednesday': '📅 Wednesday',
            'Thursday': '📅 Thursday',
            'Friday': '📅 Friday',
            'Saturday': '📅 Saturday',
            'Sunday': '📅 Sunday'
        }
        
        # Create columns for days (3 columns with 2-3 days each)
        col1, col2, col3 = st.columns(3)
        unavailable_days = st.session_state.availability['unavailable_days'].copy()
        
        with col1:
            for day in ['Monday', 'Tuesday']:
                if st.checkbox(days_of_week[day], key=f"unavailable_{day}", value=day in unavailable_days):
                    if day not in unavailable_days:
                        unavailable_days.append(day)
                else:
                    if day in unavailable_days:
                        unavailable_days.remove(day)
        
        with col2:
            for day in ['Wednesday', 'Thursday', 'Friday']:
                if st.checkbox(days_of_week[day], key=f"unavailable_{day}", value=day in unavailable_days):
                    if day not in unavailable_days:
                        unavailable_days.append(day)
                else:
                    if day in unavailable_days:
                        unavailable_days.remove(day)
        
        with col3:
            for day in ['Saturday', 'Sunday']:
                if st.checkbox(days_of_week[day], key=f"unavailable_{day}", value=day in unavailable_days):
                    if day not in unavailable_days:
                        unavailable_days.append(day)
                else:
                    if day in unavailable_days:
                        unavailable_days.remove(day)
        
        # Update session state
        st.session_state.availability['unavailable_days'] = unavailable_days
        
        # Show unavailable days summary
        if unavailable_days:
            unavailable_display = [f"❌ {day}" for day in sorted(unavailable_days)]
            st.warning("**Not available:** " + " • ".join(unavailable_display))
        else:
            st.info("✅ Available all days")
            
        # Visual preference summary
        prefs = []
        available_days_summary = []
        
        # Day preference summary
        if day_pref == 'weekdays':
            available_weekdays = [day for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] 
                                if day not in unavailable_days]
            if available_weekdays:
                available_days_summary.append(f"💼 Available weekdays: {', '.join(available_weekdays)}")
            else:
                available_days_summary.append("⚠️ No weekdays available")
        elif day_pref == 'weekends':
            available_weekends = [day for day in ['Saturday', 'Sunday'] 
                                if day not in unavailable_days]
            if available_weekends:
                available_days_summary.append(f"🏖️ Available weekends: {', '.join(available_weekends)}")
            else:
                available_days_summary.append("⚠️ No weekends available")
        else:
            # "Any day" preference
            all_available_days = [day for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] 
                                if day not in unavailable_days]
            if all_available_days:
                available_days_summary.append(f"📅 Available days: {', '.join(all_available_days)}")
        
        # Time preference
        if time_pref == 'morning':
            prefs.append("🌅 Morning/afternoon classes")
        elif time_pref == 'evening':
            prefs.append("🌆 Evening/night classes")
        else:
            prefs.append("🕐 Any time works")
        
        # Combine and display
        if available_days_summary:
            st.success("**" + " • ".join(available_days_summary + prefs) + "**")
    else:
        st.info("📚 Will show all available classes")
    
    # Visual CTA section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🚀 Ready to see your plan?")
        if st.button("Get My Personalized SAT Journey →", key="continue_to_journey", use_container_width=True, type="primary"):
            if st.session_state.test_date:
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("📅 Please select a test date first")

# Step 2: Your SAT Prep Journey  
elif st.session_state.step == 2:
    # Journey content starts here
    target_date_obj = SAT_DATES[st.session_state.test_date]
    days_until = (target_date_obj - date.today()).days
    
    # Visual hero section for journey
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🎯 Your SAT Success Journey")
        st.success(f"**Test date: {st.session_state.test_date}** • {days_until} days to go!")
    
    # Visual progress indicator
    st.progress(1.0, "Step 2 of 2: Your Personalized Plan")
    
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
        
        # Filter schedule based on availability  
        filtered_out_classes = []
        if st.session_state.availability['filter_enabled']:
            filtered_schedule, filtered_out_classes = filter_schedule_with_tracking(
                schedule, 
                st.session_state.availability['day_preference'], 
                st.session_state.availability['time_preference'],
                st.session_state.availability['filter_enabled'],
                st.session_state.availability.get('unavailable_days', [])
            )
            schedule = filtered_schedule if filtered_schedule else schedule  # Keep original if no matches
        
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
        
        # Filter schedule based on availability
        if not 'filtered_out_classes' in locals():
            filtered_out_classes = []
        if st.session_state.availability['filter_enabled']:
            filtered_schedule, additional_filtered_out = filter_schedule_with_tracking(
                schedule, 
                st.session_state.availability['day_preference'], 
                st.session_state.availability['time_preference'],
                st.session_state.availability['filter_enabled'],
                st.session_state.availability.get('unavailable_days', [])
            )
            schedule = filtered_schedule if filtered_schedule else schedule  # Keep original if no matches
            filtered_out_classes.extend(additional_filtered_out)
        
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
        
        # Filter schedule based on availability
        if not 'filtered_out_classes' in locals():
            filtered_out_classes = []
        if st.session_state.availability['filter_enabled']:
            filtered_schedule, additional_filtered_out = filter_schedule_with_tracking(
                schedule, 
                st.session_state.availability['day_preference'], 
                st.session_state.availability['time_preference'],
                st.session_state.availability['filter_enabled'],
                st.session_state.availability.get('unavailable_days', [])
            )
            schedule = filtered_schedule if filtered_schedule else schedule  # Keep original if no matches
            filtered_out_classes.extend(additional_filtered_out)
    
    # Show availability filtering info
    if st.session_state.availability['filter_enabled']:
        day_pref = st.session_state.availability['day_preference']
        time_pref = st.session_state.availability['time_preference']
        
        filter_parts = []
        if day_pref != 'both':
            filter_parts.append(f"{'Weekdays' if day_pref == 'weekdays' else 'Weekends'}")
        if time_pref != 'both':
            filter_parts.append(f"{'Morning/Afternoon' if time_pref == 'morning' else 'Evening/Night'}")
        
        if filter_parts:
            availability_text = f"Filtered for: {' • '.join(filter_parts)}"
            st.info(f"📅 **{availability_text}** - Only showing classes that match your preferences!")
            
            original_schedule_count = 5  # Approximate original schedule size
            if len(schedule) < original_schedule_count:
                st.warning(f"⚠️ Some classes were filtered out due to schedule conflicts. Showing {len(schedule)} of {original_schedule_count} recommended classes.")
    
    # Display SAT prep journey timeline using native components
    st.markdown("## 🚀 Your SAT Success Journey")
    st.markdown("Follow this personalized timeline to maximize your SAT score")
    
    # Timeline status indicator
    if timeline_status == "excellent":
        st.success(f"🌟 **{timeline_text}** • {weeks_available} weeks to prepare")
    elif timeline_status == "good": 
        st.warning(f"⚡ **{timeline_text}** • {weeks_available} weeks to prepare")
    else:
        st.error(f"🚨 **{timeline_text}** • {weeks_available} weeks to prepare")
    
    # Add suggested class sequence section with stunning learning pathways design
    if generate_suggested_sequence(schedule, st.session_state.availability):
        suggested_sequence = generate_suggested_sequence(schedule, st.session_state.availability)
        
        # Hero section for personalized journey
        st.markdown("---")
        st.markdown("# Your personalized SAT success journey")
        st.markdown("### Follow the proven pathway to SAT mastery")
        st.markdown("---")
        
        # Visual journey introduction
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success("🎯 **Perfect plan for your timeline!**")
        
        # Visual roadmap with progress indicators
        st.markdown("### 🗺️ Your learning journey")
        
        # Visual progress overview with emojis and minimal text
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("### 🏗️")
            st.success("**Step 1**")
            st.caption("Build foundation")
        with col2:
            st.markdown("### 🔢") 
            st.info("**Step 2**")
            st.caption("Master math")
        with col3:
            st.markdown("### 📚")
            st.warning("**Step 3**")
            st.caption("Perfect language")
        with col4:
            st.markdown("### 🏆")
            st.success("**Success**")
            st.caption("Ace your test")
        
        st.markdown("---")
        st.markdown("## Start here")
        st.markdown("---")
        
        # Create stunning diamond-style pathway cards (like the image)
        colors = ["#FF9500", "#3498DB", "#2ECC71", "#17A2B8", "#DC3545"]  # Orange, Blue, Green, Teal, Red
        
        for i, item in enumerate(suggested_sequence, 1):
            course_info = COURSE_CATALOG.get(item['course'], {})
            times = item.get('suggested_times', course_info.get('available_times', [])[:2])
            
            # Select color for this step
            color = colors[(i-1) % len(colors)]
            
            # Create simple, visual course information
            if "Prep Course" in item['course'] or "8-Week" in item['course']:
                benefit_title = "Foundation Building"
                benefit_desc = "Build core skills step-by-step"
                visual_benefit = "📈 Score boost: +50-100 points"
                icon = "🏗️"
            elif "Math" in item['course']:
                benefit_title = "Mathematics Mastery" 
                benefit_desc = "Master algebra, geometry & data analysis"
                visual_benefit = "🎯 Math section: +40-80 points"
                icon = "🔢"
            elif "Reading" in item['course'] or "Writing" in item['course'] or "ELA" in item['course']:
                benefit_title = "Language Excellence"
                benefit_desc = "Perfect reading & writing skills"
                visual_benefit = "✍️ Language score: +30-60 points"
                icon = "📚"
            elif "Bootcamp" in item['course']:
                benefit_title = "Intensive Boost"
                benefit_desc = "Rapid skill improvement in focused areas"
                visual_benefit = "⚡ Quick results in 1-2 weeks"
                icon = "🚀"
            elif "Review" in item['course']:
                benefit_title = "Final Polish"
                benefit_desc = "Perfect your test-taking confidence"
                visual_benefit = "🏆 Test-day confidence boost"
                icon = "🎯"
            else:
                benefit_title = "Skill Enhancement"
                benefit_desc = "Targeted improvement for better scores"
                visual_benefit = "📊 Strategic score gains"
                icon = "⭐"
            
            # Create roadmap-style course card with native Streamlit components
            with st.container():
                # Step header with visual emphasis
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    st.info(f"**🎯 STEP {i}**")
                
                # Course visual header  
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"### {icon}")
                    st.markdown(f"## {benefit_title}")
                    st.markdown(f"### {item['course']}")
                    st.caption(f"{item.get('suggested_timing', item['weeks'])} • {item['focus']}")
                
                # Add visual separation
                st.markdown("---")
                
                # Goal and benefit boxes - more prominent
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.success(f"🎯 **Goal:** {benefit_desc}")
                with col2:
                    st.success(f"{visual_benefit}")
                
                # Course schedule display with visual boxes
                if times:
                    st.markdown("### 📅 Choose Your Class Schedule")
                    st.caption("Pick a time that works for you:")
                    
                    # Display time slots with better visual grouping
                    for i_time in range(0, min(len(times), 4)):  # Show up to 4 times vertically
                        time_slot = times[i_time]
                        if ':' in time_slot and '@' in time_slot:
                            parts = time_slot.split('@')
                            date_range = parts[0].strip()
                            time_part = parts[1].strip() if len(parts) > 1 else ""
                            st.info(f"🗓️ **{date_range}** • 🕐 **{time_part}**")
                        else:
                            st.info(f"🗓️ **{time_slot}**")
                    
                    if len(times) > 4:
                        st.caption(f"➕ {len(times) - 4} more schedules available")
                
                # Visual step completion separator
                st.markdown("---")
                st.markdown("")  # Add spacing
            
            # Enrollment button outside the card
            if course_info and course_info.get('url'):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.link_button(
                        f"Enroll in step {i}",
                        course_info['url'],
                        help=f"Begin your {benefit_title.lower()} journey",
                        use_container_width=True,
                        type="primary"
                    )
            
            # Visual navigation to next step
            if i < len(suggested_sequence):
                # Simple visual arrow
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    st.markdown("### ⬇️")
                    st.caption("Next step")
                st.markdown("")  # Add spacing
        
        # Final Success Destination with maximum visual impact
        st.markdown("---")
        st.markdown("---")
        
        # Visual arrow to destination
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.markdown("### ⬇️")
            st.caption("Your destination")
        
        # Visual success destination
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("### 🏆")
            st.success("**SAT Success!**")
        
        # Visual achievement cards
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.success("### 📊\n**1400+ Score**\n+100-200 points")
        
        with col2:
            st.success("### 🧠\n**Skills Mastered**\nMath + Language")
        
        with col3:
            st.success("### 🎓\n**Future Ready**\nCollege bound")
        
        # Major visual separator before "All Options"
        st.markdown("---")
        st.markdown("---")
        st.markdown("---")
        
        # Visual section header for all options
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 📚 More class options")
            st.caption("Browse all available schedules")
        
    else:
        # If no personalized sequence, show tip
        st.info("**Tip:** Enable schedule filtering above to see a personalized class sequence recommendation")
        
        # Still show section separator for all options
        st.markdown("---")
        st.markdown("### All available course options")
        st.markdown("*Review all available times and dates for each course*")
    
    # All Available Classes section with visual distinction
    st.markdown("---")  # Add clear separation
    st.markdown("")  # Add spacing
    
    for step_number, item in enumerate(schedule, 1):
        # Create course card
        course_info = COURSE_CATALOG.get(item['course'], {})
        course_desc = course_info.get('description', 'Complete your SAT preparation with this essential course.')
        available_times = course_info.get('available_times', [])
        
        # Create visual course card for browsing with error handling
        icon = item.get('icon', '📚')
        course_name = item.get('course', 'Course')
        
        with st.expander(f"{icon} **{course_name}** ({len(available_times)} times available)", expanded=False):
            # Simple course overview
            col1, col2 = st.columns([3, 1])
            
            with col1:
                weeks = item.get('weeks', 'Duration TBD')
                focus = item.get('focus', 'SAT Preparation') 
                st.success(f"⏱️ **{weeks}** • 🎯 **{focus}**")
            
            with col2:
                # Enrollment CTA at the top
                if course_info and course_info.get('url'):
                    st.link_button(
                        "View & enroll",
                        course_info['url'],
                        use_container_width=True,
                        type="primary"
                    )
            
            # Show first few times only to avoid overwhelming
            if available_times:
                st.markdown("**📅 Available schedules:**")
                
                # Show max 4 times for quick scanning
                for i in range(0, min(len(available_times), 4), 2):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info(f"🗓️ {available_times[i]}")
                    
                    if i + 1 < len(available_times):
                        with col2:
                            st.info(f"🗓️ {available_times[i + 1]}")
                
                if len(available_times) > 4:
                    st.caption(f"➕ {len(available_times) - 4} more schedules available")
            else:
                st.warning("📞 Contact for schedule options")
        
        # Add spacing between course cards
        st.markdown("")
    
    # Visual closing section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.success("### 📞\n**Need help?**\n(800) 803-4058")
    with col2:
        st.info("### 🎯\n**Your plan**\nStep-by-step success")
    with col3:
        st.warning("### ⏰\n**Ready to start?**\nPick your classes!")
    
    # Show filtered out classes if any
    if st.session_state.availability['filter_enabled']:
        try:
            if 'filtered_out_classes' in locals() and filtered_out_classes:
                with st.expander(f"Classes not matching your schedule ({len(filtered_out_classes)} hidden)", expanded=False):
                    st.markdown("**The following classes were filtered out based on your availability preferences:**")
                    st.markdown("*You can adjust your availability settings on the previous page if you're interested in any of these.*")
                    
                    for filtered_class in filtered_out_classes:
                        item = filtered_class['item']
                        reason = filtered_class['reason']
                        times = filtered_class['times']
                        
                        # Create a card for each filtered class
                        st.markdown("---")
                        
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            filtered_icon = item.get('icon', '📚')
                            filtered_course = item.get('course', 'Course')
                            filtered_focus = item.get('focus', 'SAT Prep')
                            filtered_weeks = item.get('weeks', 'Duration TBD')
                            st.markdown(f"**{filtered_icon} {filtered_course}**")
                            st.markdown(f"*{filtered_focus} • {filtered_weeks}*")
                            
                            # Show why it was filtered
                            st.markdown(f"🚫 **Filtered because:** {reason}")
                            
                            # Show sample class times
                            if times:
                                st.markdown("⏰ **Sample times:**")
                                for time in times:
                                    st.markdown(f"   • {time}")
                                if len(times) == 3 and len(COURSE_CATALOG.get(item['course'], {}).get('available_times', [])) > 3:
                                    st.markdown("   • *...and more times available*")
                        
                        with col2:
                            course_info = COURSE_CATALOG.get(item['course'], {})
                            if course_info and course_info.get('url'):
                                st.markdown(f"""
                                <a href="{course_info['url']}" target="_blank" 
                                   style="background: #6b7280; color: white; padding: 10px 15px; 
                                          border-radius: 8px; text-decoration: none; font-size: 0.9em; 
                                          display: inline-block; text-align: center;">
                                   View All Times
                                </a>
                                """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("**Tip:** Go back to step 1 to adjust your availability and see more class options")
        except NameError:
            # filtered_out_classes not defined, which means no filtering occurred
            pass
    
    # Navigation back to step 1
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("← Back to quick set up", key="back_to_step1", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

# Action Bar (simplified native version)
if st.session_state.step == 2:
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**Test Date:** {st.session_state.test_date}")
        if 'timeline_text' in locals():
            st.markdown(f"**Timeline:** {timeline_text}")
    with col2:
        st.markdown("📞 **Questions? Call (800) 803-4058**")

# Footer
st.markdown("---")
st.markdown("**SAT Class Finder** - Connecting students with Varsity Tutors SAT preparation classes") 

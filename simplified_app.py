import streamlit as st
from datetime import date

# =============================================
#  SAT Class Finder — UX v4
#  Clear navigation, accessible visuals, safe CSS
# =============================================

st.set_page_config(page_title="SAT Class Finder", page_icon="📚", layout="wide")

# ==========================
# Design System (CSS)
# ==========================
st.markdown(
    """
<style>
:root {
  /* Base */
  --bg:#f8fafc; --surface:#ffffff; --ink:#0f172a; --ink-muted:#475569; --border:#e2e8f0;
  /* Brand */
  --brand-50:#eff6ff; --brand-100:#dbeafe; --brand-200:#bfdbfe; --brand-300:#93c5fd; --brand-400:#60a5fa;
  --brand-500:#3b82f6; --brand-600:#2563eb; --brand-700:#1d4ed8; --brand-800:#1e40af; --brand-900:#1e3a8a;
  /* Semantic */
  --success-50:#f0fdf4; --success-500:#22c55e; --warning-50:#fffbeb; --warning-500:#f59e0b; --danger-50:#fef2f2; --danger-500:#ef4444;
  /* Tokens */
  --radius-sm:.5rem; --radius-lg:1rem; --shadow-sm:0 1px 2px rgba(0,0,0,.06); --shadow-md:0 6px 16px rgba(15,23,42,.08);
  --h1:clamp(2rem,1.5rem+2vw,2.75rem); --h2:clamp(1.25rem,1rem+1.2vw,1.6rem); --h3:1.125rem; --body:1rem;
}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif!important}
body{background:var(--bg);color:var(--ink);line-height:1.55}
.stApp{background:var(--bg)}
.main>div{max-width:1120px;margin:0 auto;padding:2rem 1rem}

h1{font-size:var(--h1);font-weight:800;letter-spacing:-.01em;color:var(--ink)}
h2{font-size:var(--h2);font-weight:700;color:var(--ink)}
h3{font-size:var(--h3);font-weight:600;color:var(--ink)}
p,li{font-size:var(--body);color:var(--ink-muted)}

/* Hero */
.hero{background:linear-gradient(135deg,var(--brand-600),var(--brand-800));color:#fff;padding:2.25rem 1.5rem;margin:-1.25rem -1rem 1.5rem;border-radius:0 0 24px 24px;text-align:center}
.hero h1{margin:0 0 .5rem 0}
.hero p{opacity:.95;margin:0}

/* Stepper */
.stepper{display:flex;gap:1rem;justify-content:center;align-items:center;margin:.5rem 0}
.stepper .step{display:flex;align-items:center;gap:.5rem;padding:.5rem .9rem;border:1.5px solid var(--border);border-radius:999px;background:#fff}
.stepper .step.active{border-color:var(--brand-400);box-shadow:0 0 0 3px var(--brand-100)}
.stepper .dot{width:10px;height:10px;border-radius:999px;background:var(--brand-600)}

/* Buttons & Inputs */
.stButton button{background:var(--brand-600)!important;color:#fff!important;border:none!important;border-radius:12px!important;padding:.9rem 1.2rem!important;font-weight:600!important;font-size:.95rem!important;transition:transform .15s ease,box-shadow .15s ease}
.stButton button:hover{background:var(--brand-700)!important;transform:translateY(-1px)!important;box-shadow:0 4px 12px rgba(2,132,199,.3)!important}
.stSelectbox > div > div, .stRadio > div, .stMultiSelect > div > div {border-radius:12px!important;border:2px solid var(--border)!important}

/* Info boxes */
.stInfo{background:var(--brand-50)!important;border-left:4px solid var(--brand-600)!important;border-radius:12px!important}
.stSuccess{background:var(--success-50)!important;border-left:4px solid var(--success-500)!important;border-radius:12px!important}
.stWarning{background:var(--warning-50)!important;border-left:4px solid var(--warning-500)!important;border-radius:12px!important}

/* Custom collapsible sections */




/* Custom button styling for collapsible sections */
.stButton > button {
  text-align: left !important;
  width: 100% !important;
}

/* Clean container spacing */
.stContainer {
  margin: 0.5rem 0 !important;
}

/* Additional spacing for all Streamlit containers */
.element-container {
  margin-bottom: 0.75rem !important;
}
/* Reasonable heading spacing */
h1, h2, h3, h4, h5, h6 {
  margin: 1rem 0 0.5rem 0 !important;
  clear: both !important;
}

/* Progress */
.stProgress > div > div > div > div{background-color:var(--brand-600)!important}

/* Footer/branding */
#MainMenu, header, footer{visibility:hidden}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================
# Session State
# ==========================
if "step" not in st.session_state:
    st.session_state.step = 1
if "test_date" not in st.session_state:
    st.session_state.test_date = None
if "availability" not in st.session_state:
    st.session_state.availability = {
        "day_preference": "both",
        "time_preference": "both",
        "filter_enabled": False,
        "unavailable_days": [],
    }

# ==========================
# Data
# ==========================
SAT_DATES = {
    "August 23, 2025": date(2025, 8, 23),
    "September 13, 2025": date(2025, 9, 13),
    "October 4, 2025": date(2025, 10, 4),
    "November 8, 2025": date(2025, 11, 8),
    "December 6, 2025": date(2025, 12, 6),
    "March 14, 2026": date(2026, 3, 14),
    "May 2, 2026": date(2026, 5, 2),
    "June 6, 2026": date(2026, 6, 6),
}

COURSE_CATALOG = {
    "SAT 2-Week Bootcamp": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-two-week-bootcamp/dp/e34ad454-d5a7-4851-9694-cdd64675b3d8",
        "description": "Intensive 2-week prep focusing on strategies and key concepts.",
        "available_times": [
            "Aug 31 - Sep 10: Sun, Mon, Tue, Wed @ 6:30 PM ET",
            "Sep 21 - Oct 1: Sun, Mon, Tue, Wed @ 7:00 PM ET",
            "Oct 27 - Nov 6: Mon, Tue, Wed, Thu @ 7:00 PM ET",
        ],
    },
    "SAT 4-Week Prep Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-four-week-prep-course/dp/e3a6e856-31db-429d-a52f-dfbbc93c2edd",
        "description": "Comprehensive 4-week SAT preparation covering all sections.",
        "available_times": [
            "Sep 4 - Sep 25: Thu @ 9:00 PM ET",
            "Sep 9 - Sep 30: Tue @ 6:00 PM ET",
            "Oct 9 - Oct 30: Thu @ 8:30 PM ET",
        ],
    },
    "SAT Prep Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-prep-course/dp/c85c2298-bd6a-4cd4-be0d-8f4f35d3f7eb",
        "description": "Extended comprehensive SAT preparation (8+ weeks).",
        "available_times": [
            "Sep 11 - Oct 30: Thu @ 5:30 PM ET",
            "Oct 7 - Nov 25: Tue @ 5:30 PM ET",
            "Oct 13 - Dec 1: Mon @ 8:00 PM ET",
        ],
    },
    "SAT Math Cram Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-math-cram-session/dp/33f2fab0-1908-4b5c-9d36-966e467af942",
        "description": "Focused strategies for the SAT Math section.",
        "available_times": [
            "Sep 7: Sun @ 6:30 PM ET",
            "Oct 1: Wed @ 9:00 PM ET",
            "Nov 30: Sun @ 6:30 PM ET",
        ],
    },
    "SAT Reading/Writing Cram Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-sat-reading-writing-cram-session/dp/03ea8fe7-ff75-4b07-b69e-f3558c1ed44e",
        "description": "Reading and Writing strategies for quick gains.",
        "available_times": [
            "Sep 7: Sun @ 4:30 PM ET",
            "Sep 29: Mon @ 7:00 PM ET",
            "Nov 30: Sun @ 5:30 PM ET",
        ],
    },
    "2-Week SAT Math Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-math-sat-9-12/dp/2f67b5be-e283-406f-b4d2-fe3fc17e52aa",
        "description": "Two-week intensive course focused on SAT Math.",
        "available_times": [
            "Sep 20-27: Sat @ 3:30 PM ET",
            "Oct 26 - Nov 2: Sun @ 1:00 PM ET",
        ],
    },
    "2-Week SAT ELA Course": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-two-week-ela-sat-9-12/dp/81b322ee-93b3-4389-88af-bf11f7d0240f",
        "description": "Two-week intensive course for Reading & Writing.",
        "available_times": [
            "Sep 20-27: Sat @ 3:30 PM ET",
            "Oct 26 - Nov 2: Sun @ 1:00 PM ET",
        ],
    },
    "Ultimate SAT Review Session": {
        "url": "https://www.varsitytutors.com/courses/vtpsg-ultimate-sat-review-session/dp/2a08c912-0a50-4639-b097-dfcaa2f591de",
        "description": "Final review of key concepts and test strategies.",
        "available_times": [
            "Sep 27: Fri @ 11:00 AM ET",
            "Nov 1: Fri @ 3:00 PM ET",
        ],
    },
    "Proctored Practice SAT": {
        "url": "https://www.varsitytutors.com/courses/vtp-proctored-practiced-sat-9-12/dp/2298ff50-8011-48e7-acc0-c81cb25eeae1",
        "description": "Practice test under realistic timing (3 hours).",
        "available_times": [
            "Sep 13: Fri @ 12:00 PM ET",
            "Oct 11: Fri @ 11:00 AM ET",
            "Nov 15: Fri @ 12:00 PM ET",
        ],
    },
}

# ==========================
# Helpers
# ==========================
DAY_MAP = {
    'Monday':['mon','monday','mo'], 'Tuesday':['tue','tuesday','tues','tu'], 'Wednesday':['wed','wednesday','we'],
    'Thursday':['thu','thursday','thurs','th'], 'Friday':['fri','friday','fr'], 'Saturday':['sat','saturday','sa'], 'Sunday':['sun','sunday','su'],
}

def matches_availability(course_times, day_preference, time_preference, filter_enabled, unavailable_days=None):
    if not filter_enabled: 
        return True
    unavailable_days = unavailable_days or []
    for slot in course_times:
        s = slot.lower()
        # exclude unavailable days
        if any(any(v in s for v in DAY_MAP.get(d, [])) for d in unavailable_days):
            continue
        # day pref
        if day_preference == 'weekdays':
            wk = any(any(v in s for v in DAY_MAP[d]) for d in ['Monday','Tuesday','Wednesday','Thursday','Friday'])
            if not wk: 
                continue
        elif day_preference == 'weekends':
            we = any(any(v in s for v in DAY_MAP[d]) for d in ['Saturday','Sunday'])
            if not we: 
                continue
        # time pref
        if time_preference == 'morning':
            if not any(h in slot for h in ["9:00 AM","10:00 AM","11:00 AM","12:00 PM","1:00 PM","2:00 PM","3:00 PM"]):
                continue
        elif time_preference == 'evening':
            if not any(h in slot for h in ["4:00 PM","5:00 PM","6:00 PM","7:00 PM","8:00 PM","9:00 PM","10:00 PM","11:00 PM"]):
                continue
        return True
    return False

def filter_schedule_with_tracking(original, day_pref, time_pref, enabled, unavailable_days=None):
    unavailable_days = unavailable_days or []
    keep, hidden = [], []
    for item in original:
        info = COURSE_CATALOG.get(item['course'], {})
        times = info.get('available_times', [])
        if matches_availability(times, day_pref, time_pref, enabled, unavailable_days):
            keep.append(item)
        else:
            hidden.append({"item": item, "reason": "Doesn't match your day/time preferences", "times": times[:3]})
    return keep, hidden

def generate_suggested_sequence(schedule, availability, days_until_test):
    if not availability.get('filter_enabled', False):
        return None
    day = availability.get('day_preference','both')
    time = availability.get('time_preference','both')
    blocked = availability.get('unavailable_days',[])
    
    # Get all available courses that match schedule
    available_courses = []
    for course_name, info in COURSE_CATALOG.items():
        times = info.get('available_times', [])
        matches = [t for t in times if matches_availability([t], day, time, True, blocked)]
        if matches:
            available_courses.append({
                'course': course_name,
                'available_times': matches,
                'type': classify_course_type(course_name),
                'duration_weeks': get_course_duration(course_name)
            })
    
    # Build comprehensive sequence based on timeline
    sequence = build_comprehensive_sequence(available_courses, days_until_test)
    return sequence

def classify_course_type(course_name):
    """Classify course into type categories"""
    if 'Bootcamp' in course_name:
        return 'intensive'
    elif 'Prep Course' in course_name:
        return 'comprehensive'
    elif 'Cram Session' in course_name:
        return 'focused'
    elif 'Practice' in course_name:
        return 'practice'
    elif 'Review' in course_name:
        return 'review'
    elif 'Math Course' in course_name or 'ELA Course' in course_name:
        return 'subject_focused'
    return 'general'

def get_course_duration(course_name):
    """Estimate course duration in weeks"""
    if '2-Week' in course_name or 'Bootcamp' in course_name:
        return 2
    elif '4-Week' in course_name:
        return 4
    elif 'Prep Course' in course_name and '4-Week' not in course_name:
        return 8
    elif 'Cram Session' in course_name or 'Review' in course_name:
        return 1
    elif 'Practice' in course_name:
        return 0.5  # Half week for practice sessions
    return 1

def build_comprehensive_sequence(available_courses, days_until_test):
    """Build a comprehensive, varied sequence with weekly practice"""
    weeks_available = max(days_until_test // 7, 1)
    sequence = []
    used_weeks = 0
    
    # Sort courses by type priority and availability
    course_types = {
        'comprehensive': [c for c in available_courses if c['type'] == 'comprehensive'],
        'intensive': [c for c in available_courses if c['type'] == 'intensive'],
        'subject_focused': [c for c in available_courses if c['type'] == 'subject_focused'],
        'focused': [c for c in available_courses if c['type'] == 'focused'],
        'review': [c for c in available_courses if c['type'] == 'review'],
        'practice': [c for c in available_courses if c['type'] == 'practice']
    }
    
    # Phase 1: Foundation Building (40% of time)
    foundation_weeks = max(int(weeks_available * 0.4), 1)
    if course_types['comprehensive'] and used_weeks < foundation_weeks:
        course = course_types['comprehensive'][0]
        sequence.append({
            'phase': 'Foundation',
            'week_range': f"Week {used_weeks + 1}-{min(used_weeks + int(course['duration_weeks']), foundation_weeks)}",
            'course': course['course'],
            'focus': 'Comprehensive SAT preparation and strategy building',
            'icon': '📚',
            'available_times': course['available_times'][:3],
            'type': 'Primary Course'
        })
        used_weeks += int(course['duration_weeks'])
    elif course_types['intensive'] and used_weeks < foundation_weeks:
        course = course_types['intensive'][0]
        sequence.append({
            'phase': 'Foundation',
            'week_range': f"Week {used_weeks + 1}-{used_weeks + int(course['duration_weeks'])}",
            'course': course['course'],
            'focus': 'Intensive skill building and concept mastery',
            'icon': '🚀',
            'available_times': course['available_times'][:3],
            'type': 'Primary Course'
        })
        used_weeks += int(course['duration_weeks'])
    
    # Add weekly practice during foundation
    if course_types['practice'] and weeks_available > 4:
        practice_course = course_types['practice'][0]
        sequence.append({
            'phase': 'Foundation',
            'week_range': f"Week {max(used_weeks-1, 1)} onwards",
            'course': practice_course['course'],
            'focus': 'Weekly practice tests to track progress',
            'icon': '📝',
            'available_times': practice_course['available_times'][:3],
            'type': 'Weekly Practice'
        })
    
    # Phase 2: Subject Mastery (30% of time)
    mastery_weeks = max(int(weeks_available * 0.3), 1)
    mastery_start = used_weeks + 1
    
    # Add Math focus
    if course_types['subject_focused']:
        math_courses = [c for c in course_types['subject_focused'] if 'Math' in c['course']]
        if math_courses and used_weeks < mastery_start + mastery_weeks:
            course = math_courses[0]
            sequence.append({
                'phase': 'Subject Mastery',
                'week_range': f"Week {used_weeks + 1}-{used_weeks + int(course['duration_weeks'])}",
                'course': course['course'],
                'focus': 'Advanced math strategies and problem-solving',
                'icon': '🔢',
                'available_times': course['available_times'][:3],
                'type': 'Subject Focus'
            })
            used_weeks += int(course['duration_weeks'])
    
    # Add ELA focus
    if course_types['subject_focused']:
        ela_courses = [c for c in course_types['subject_focused'] if 'ELA' in c['course']]
        if ela_courses and used_weeks < mastery_start + mastery_weeks:
            course = ela_courses[0]
            sequence.append({
                'phase': 'Subject Mastery',
                'week_range': f"Week {used_weeks + 1}-{used_weeks + int(course['duration_weeks'])}",
                'course': course['course'],
                'focus': 'Reading comprehension and writing excellence',
                'icon': '📖',
                'available_times': course['available_times'][:3],
                'type': 'Subject Focus'
            })
            used_weeks += int(course['duration_weeks'])
    
    # Phase 3: Targeted Improvement (20% of time)
    if course_types['focused'] and weeks_available > 6:
        improvement_weeks = max(int(weeks_available * 0.2), 1)
        
        # Math cram session
        math_cram = [c for c in course_types['focused'] if 'Math' in c['course']]
        if math_cram:
            course = math_cram[0]
            sequence.append({
                'phase': 'Targeted Improvement',
                'week_range': f"Week {used_weeks + 1}",
                'course': course['course'],
                'focus': 'Intensive math review and advanced techniques',
                'icon': '🎯',
                'available_times': course['available_times'][:3],
                'type': 'Intensive Session'
            })
            used_weeks += 1
        
        # Reading/Writing cram session
        ela_cram = [c for c in course_types['focused'] if 'Reading' in c['course'] or 'Writing' in c['course']]
        if ela_cram:
            course = ela_cram[0]
            sequence.append({
                'phase': 'Targeted Improvement',
                'week_range': f"Week {used_weeks + 1}",
                'course': course['course'],
                'focus': 'Reading strategies and writing optimization',
                'icon': '✍️',
                'available_times': course['available_times'][:3],
                'type': 'Intensive Session'
            })
            used_weeks += 1
    
    # Phase 4: Final Preparation (10% of time)
    if course_types['review']:
        review_course = course_types['review'][0]
        sequence.append({
            'phase': 'Final Preparation',
            'week_range': f"Week {min(used_weeks + 1, weeks_available)}",
            'course': review_course['course'],
            'focus': 'Last-minute review and test-day strategies',
            'icon': '🏁',
            'available_times': review_course['available_times'][:3],
            'type': 'Final Review'
        })
    
    # Add final practice sessions
    if course_types['practice'] and weeks_available > 2:
        practice_course = course_types['practice'][0]
        sequence.append({
            'phase': 'Final Preparation',
            'week_range': f"Final 2 weeks",
            'course': practice_course['course'],
            'focus': 'Full-length practice tests under timed conditions',
            'icon': '⏰',
            'available_times': practice_course['available_times'][:3],
            'type': 'Final Practice'
        })
    
    return sequence

# ==========================
# Top: Hero + Stepper
# ==========================
st.markdown('<div class="hero"><h1>🎯 SAT Class Finder</h1><p>See the right classes for your timeline and schedule. All times shown in ET.</p></div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    go_step1 = st.button("① Quick setup", type="primary" if st.session_state.step==1 else "secondary")
with c2:
    go_step2 = st.button("② Your plan", type="primary" if st.session_state.step==2 else "secondary")
if go_step1: st.session_state.step = 1
if go_step2: st.session_state.step = 2

# ==========================
# STEP 1 — Quick setup
# ==========================
if st.session_state.step == 1:
    st.progress(0.5, text="Step 1 of 2: Quick setup")

    st.markdown("### 📅 When are you taking the SAT?")
    st.caption("Pick your test date to tailor your prep timeline.")

    available_dates = {k:v for k,v in SAT_DATES.items() if (v - date.today()).days > 0}
    if not available_dates:
        st.error("No upcoming SAT dates available.")
    else:
        left, right = st.columns([3,2])
        with left:
            options = list(available_dates.keys())
            default_idx = options.index(st.session_state.test_date) if st.session_state.test_date in available_dates else 0
            selected = st.selectbox("Select your test date", options=options, index=default_idx, label_visibility="collapsed")
            st.session_state.test_date = selected
        with right:
            days_until = (available_dates[selected] - date.today()).days
            if days_until > 56:
                st.success(f"**Your test is in {days_until} days** — 🌟 Perfect prep window")
            elif days_until > 28:
                st.warning(f"**Your test is in {days_until} days** — ⚡ Focused prep needed")
            else:
                st.error(f"**Your test is in {days_until} days** — 🚨 Intensive prep required")

    st.markdown("### ⚙️ Schedule preferences (optional)")
    st.caption("Filter classes to match when you can attend.")

    # Toggle with fallback for older Streamlit
    if hasattr(st, "toggle"):
        toggle = st.toggle("Only show classes that fit my schedule", value=st.session_state.availability['filter_enabled'])
    else:
        toggle = st.checkbox("Only show classes that fit my schedule", value=st.session_state.availability['filter_enabled'])
    st.session_state.availability['filter_enabled'] = toggle

    if toggle:
        colA, colB = st.columns(2)
        with colA:
            day_pref = st.radio(
                "Day preference",
                options=['both','weekdays','weekends'],
                index=['both','weekdays','weekends'].index(st.session_state.availability['day_preference']),
                format_func=lambda x:{'both':'🗓️ Any day','weekdays':'💼 Weekdays only','weekends':'🏖️ Weekends only'}[x],
                label_visibility="collapsed",
                help="Choose which days generally work best.",
            )
            st.session_state.availability['day_preference'] = day_pref
        with colB:
            time_pref = st.radio(
                "Time preference",
                options=['both','morning','evening'],
                index=['both','morning','evening'].index(st.session_state.availability['time_preference']),
                format_func=lambda x:{'both':'🕐 Any time','morning':'🌅 Morning/afternoon (9a–3p ET)','evening':'🌆 Evening/night (4p–11p ET)'}[x],
                label_visibility="collapsed",
            )
            st.session_state.availability['time_preference'] = time_pref

        st.markdown("**📅 Days you're NOT available**")
        unavailable = st.multiselect(
            "Days you can't attend",
            options=list(DAY_MAP.keys()),
            default=st.session_state.availability.get('unavailable_days',[]),
            label_visibility="collapsed",
        )
        st.session_state.availability['unavailable_days'] = unavailable

        # Summary
        summary = []
        if day_pref == 'weekdays':
            days_ok = [d for d in ['Monday','Tuesday','Wednesday','Thursday','Friday'] if d not in unavailable]
            summary.append("💼 Available weekdays: " + (", ".join(days_ok) if days_ok else "None"))
        elif day_pref == 'weekends':
            days_ok = [d for d in ['Saturday','Sunday'] if d not in unavailable]
            summary.append("🏖️ Available weekends: " + (", ".join(days_ok) if days_ok else "None"))
        else:
            days_ok = [d for d in DAY_MAP.keys() if d not in unavailable]
            summary.append("📅 Available days: " + (", ".join(days_ok) if days_ok else "None"))
        summary.append({'both':'🕐 Any time works','morning':'🌅 Morning/afternoon','evening':'🌆 Evening/night'}[time_pref])
        st.success("**" + " • ".join(summary) + "**")

    st.markdown("---")
    center = st.columns([1,2,1])[1]
    with center:
        if st.button("Get my personalized SAT journey →", use_container_width=True, type="primary"):
            if st.session_state.test_date:
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Please select a test date first.")

# ==========================
# STEP 2 — Your plan
# ==========================
else:
    st.progress(1.0, text="Step 2 of 2: Your personalized plan")

    if not st.session_state.test_date:
        st.warning("Pick a test date on Step 1 to generate your plan.")
        st.stop()

    target = SAT_DATES[st.session_state.test_date]
    days_until = (target - date.today()).days

    st.markdown("## 🚀 Your SAT success journey")
    st.caption(f"Test date: {st.session_state.test_date} • {days_until} days to go")

    # Build schedule by timeline
    if days_until > 56:
        schedule = [
            {"weeks":"Week 1-8","course":"SAT Prep Course","focus":"Foundation Building","icon":"📚"},
            {"weeks":"Week 9-10","course":"2-Week SAT Math Course","focus":"Math Mastery","icon":"🔢"},
            {"weeks":"Week 11-12","course":"2-Week SAT ELA Course","focus":"Reading & Writing","icon":"📖"},
            {"weeks":"Week 13","course":"Ultimate SAT Review Session","focus":"Final Review","icon":"🎯"},
            {"weeks":"Ongoing","course":"Proctored Practice SAT","focus":"Test Practice","icon":"📝"},
        ]
        st.success(f"🌟 Perfect timeline • {max(days_until//7,1)} weeks to prepare")
    elif days_until > 28:
        schedule = [
            {"weeks":"Week 1-4","course":"SAT 4-Week Prep Course","focus":"Core Concepts","icon":"📚"},
            {"weeks":"Week 5-6","course":"2-Week SAT Math Course","focus":"Math Focus","icon":"🔢"},
            {"weeks":"Week 7","course":"SAT Reading/Writing Cram Session","focus":"ELA Boost","icon":"📖"},
            {"weeks":"Week 8","course":"Ultimate SAT Review Session","focus":"Final Prep","icon":"🎯"},
            {"weeks":"Weekly","course":"Proctored Practice SAT","focus":"Practice Tests","icon":"📝"},
        ]
        st.warning(f"⚡ Intensive timeline • {max(days_until//7,1)} weeks to prepare")
    else:
        schedule = [
            {"weeks":"Week 1-2","course":"SAT 2-Week Bootcamp","focus":"Essential Skills","icon":"🚀"},
            {"weeks":"Week 3","course":"SAT Math Cram Session","focus":"Math Intensive","icon":"🔢"},
            {"weeks":"Week 4","course":"SAT Reading/Writing Cram Session","focus":"ELA Cram","icon":"📖"},
            {"weeks":"Final Days","course":"Ultimate SAT Review Session","focus":"Last Review","icon":"🎯"},
            {"weeks":"Ongoing","course":"Proctored Practice SAT","focus":"Practice","icon":"📝"},
        ]
        st.error(f"🚨 Rush timeline • {max(days_until//7,1)} weeks to prepare")

    # Apply filters if enabled
    filtered_out = []
    av = st.session_state.availability
    if av['filter_enabled']:
        kept, hidden = filter_schedule_with_tracking(
            schedule,
            av['day_preference'],
            av['time_preference'],
            True,
            av.get('unavailable_days',[])
        )
        schedule = kept or schedule
        filtered_out = hidden
        labels = []
        if av['day_preference']!='both':
            labels.append('Weekdays' if av['day_preference']=='weekdays' else 'Weekends')
        if av['time_preference']!='both':
            labels.append('Morning/Afternoon' if av['time_preference']=='morning' else 'Evening/Night')
        if labels:
            st.info("📅 **Filtered for:** " + " • ".join(labels))

    # Comprehensive suggested sequence (if filters on)
    suggested = generate_suggested_sequence(schedule, av, days_until)
    if suggested:
        st.markdown("### 🗺️ Your personalized SAT prep schedule")
        weeks_available = max(days_until // 7, 1)
        st.caption(f"Optimized {weeks_available}-week preparation plan with weekly practice and varied course types")
        
        # Create timeline overview
        st.markdown("#### 📅 Your Prep Timeline")
        
        # Timeline visualization
        timeline_data = []
        practice_weeks = []
        
        for item in suggested:
            week_range = item.get('week_range', '')
            course_type = item.get('type', 'Course')
            
            if 'Weekly Practice' in course_type or 'Final Practice' in course_type:
                if 'onwards' in week_range or 'Final' in week_range:
                    practice_weeks.append(f"🏃‍♂️ Practice tests throughout")
                else:
                    practice_weeks.append(f"🏃‍♂️ {week_range}: Practice tests")
            else:
                timeline_data.append({
                    'weeks': week_range,
                    'course': item['course'],
                    'type': course_type,
                    'focus': item['focus'],
                    'icon': item['icon']
                })
        
        # Display timeline in a structured way
        if timeline_data:
            for i, item in enumerate(timeline_data, 1):
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"**Step {i}**")
                    st.caption(item['weeks'])
                with col2:
                    course_type_color = {
                        'Primary Course': '🟢',
                        'Subject Focus': '🔵', 
                        'Intensive Session': '🟡',
                        'Final Review': '🔴'
                    }.get(item['type'], '⚪')
                    
                    st.markdown(f"{course_type_color} **{item['icon']} {item['course']}**")
                    st.caption(f"Focus: {item['focus']} • Type: {item['type']}")
                
                if i < len(timeline_data):
                    st.markdown("↓")
        
        # Display practice schedule
        if practice_weeks:
            st.info("**🏃‍♂️ Practice Schedule:** " + " • ".join(practice_weeks))
        
        st.markdown("---")
        
        # Detailed course information
        st.markdown("#### 📚 Course Details & Enrollment")
        st.caption("Click any course below to see schedules and enroll")
        
        # Group courses by type for better organization
        course_types = {
            'Foundation Courses': [],
            'Subject-Focused Courses': [],
            'Intensive Sessions': [],
            'Practice & Review': []
        }
        
        for item in suggested:
            course_type = item.get('type', 'Course')
            if course_type == 'Primary Course':
                course_types['Foundation Courses'].append(item)
            elif course_type == 'Subject Focus':
                course_types['Subject-Focused Courses'].append(item)
            elif course_type == 'Intensive Session':
                course_types['Intensive Sessions'].append(item)
            else:
                course_types['Practice & Review'].append(item)
        
        for category, items in course_types.items():
            if items:
                st.markdown(f"**{category}**")
                for idx, item in enumerate(items):
                    info = COURSE_CATALOG.get(item['course'], {})
                    
                    # Create custom collapsible section with unique index
                    clean_category = category.replace(' ', '_').replace('&', 'and')
                    clean_course = item['course'].replace(' ', '_').replace('-', '_').replace('&', 'and')
                    course_key = f"details_{clean_category}_{clean_course}_{idx}"
                    if course_key not in st.session_state:
                        st.session_state[course_key] = False
                    
                    # Custom header button
                    button_text = f"{item['icon']} {item['course']} ({item['week_range']})"
                    if st.button(button_text, key=f"btn_{course_key}", use_container_width=True):
                        st.session_state[course_key] = not st.session_state[course_key]
                    
                    # Show content if expanded
                    if st.session_state[course_key]:
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f"**{item['focus']}**")
                                if info.get('description'):
                                    st.markdown(info['description'])
                                
                                if item.get('available_times'):
                                    st.markdown("**📅 Available times that match your schedule:**")
                                    for t in item['available_times'][:3]:
                                        if '@' in t:
                                            date_part, time_part = t.split('@', 1)
                                            st.success(f"🗓️ **{date_part.strip()}** at **{time_part.strip()}**")
                                        else:
                                            st.success(f"🗓️ **{t}**")
                                    
                                    if len(item['available_times']) > 3:
                                        st.caption(f"Plus {len(item['available_times']) - 3} more time options")
                            
                            with col2:
                                # Course timing info
                                course_type = item.get('type', 'Course')
                                if 'Practice' in course_type:
                                    st.warning("**Practice**\nOngoing")
                                elif 'Primary' in course_type:
                                    st.info("**Foundation**\nCore prep")
                                elif 'Subject' in course_type:
                                    st.success("**Subject Focus**\nSpecialized")
                                elif 'Intensive' in course_type:
                                    st.error("**Intensive**\nHigh impact")
                                else:
                                    st.info("**Review**\nFinal prep")
                            
                            if info.get('url'):
                                st.link_button("🎯 View details & enroll", info['url'], use_container_width=True, type="primary")
                
                st.markdown("")
        
        # Summary and next steps
        st.markdown("#### 🎯 Your Preparation Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        total_courses = len([s for s in suggested if 'Practice' not in s.get('type', '')])
        practice_sessions = len([s for s in suggested if 'Practice' in s.get('type', '')])
        foundation_courses = len([s for s in suggested if 'Primary' in s.get('type', '')])
        specialized_courses = len([s for s in suggested if 'Subject' in s.get('type', '') or 'Intensive' in s.get('type', '')])
        
        with col1:
            st.metric("📚 Main Courses", total_courses)
        with col2:
            st.metric("🏃‍♂️ Practice Sessions", practice_sessions)
        with col3:
            st.metric("🏗️ Foundation", foundation_courses)
        with col4:
            st.metric("🎯 Specialized", specialized_courses)
        
        # Action plan
        st.success(f"""
        **🚀 Your Action Plan:**
        1. **Start with foundation courses** ({foundation_courses} course{'s' if foundation_courses != 1 else ''}) for core skills
        2. **Add weekly practice tests** throughout your preparation
        3. **Focus on weak areas** with specialized courses ({specialized_courses} available)
        4. **Take practice tests** regularly to track progress
        5. **Complete final review** in the weeks before your test
        """)
        
        st.markdown("---")

    # All recommended classes
    st.markdown("### 📚 All recommended classes")
    st.caption("Expand a class to see schedules and enroll.")
    st.markdown("")

    for idx, item in enumerate(schedule):
        info = COURSE_CATALOG.get(item['course'], {})
        times = info.get('available_times', [])
        
        # Create explicit expander title
        course_icon = item.get('icon','📚')
        course_name = item['course']
        course_focus = item['focus']
        # Create custom collapsible section for all recommended classes
        clean_course_name = course_name.replace(' ', '_').replace('-', '_').replace('&', 'and')
        rec_course_key = f"all_recommended_{clean_course_name}_{idx}"
        if rec_course_key not in st.session_state:
            st.session_state[rec_course_key] = False
        
        # Custom header button
        button_text = f"{course_icon} {course_name} · {course_focus}"
        if st.button(button_text, key=f"btn_{rec_course_key}", use_container_width=True):
            st.session_state[rec_course_key] = not st.session_state[rec_course_key]
        
        # Show content if expanded
        if st.session_state[rec_course_key]:
            with st.container():
                st.success(f"⏱️ **{item['weeks']}** • 🎯 **{item['focus']}**")
                if info.get('description'):
                    st.markdown(info['description'])
                if times:
                    st.markdown("**📅 Available schedules:**")
                    for t in times[:4]:
                        st.info(f"🗓️ {t}")
                    remaining = max(len(times)-4, 0)
                    if remaining:
                        st.caption(f"➕ {remaining} more schedules available")
                else:
                    st.warning("Contact us for schedule options.")
                if info.get('url'):
                    st.link_button("View & enroll", info['url'], use_container_width=True, type="primary")
        st.markdown("")

    # Hidden by filters
    if av['filter_enabled'] and filtered_out:
        # Create custom collapsible section for filtered courses
        num_filtered = len(filtered_out)
        filtered_key = "show_filtered_courses"
        if filtered_key not in st.session_state:
            st.session_state[filtered_key] = False
        
        # Custom header button
        button_text = f"🚫 Hidden by your filters ({num_filtered})"
        if st.button(button_text, key="btn_filtered_courses_section", use_container_width=True):
            st.session_state[filtered_key] = not st.session_state[filtered_key]
        
        # Show content if expanded
        if st.session_state[filtered_key]:
            with st.container():
                st.caption("Adjust schedule preferences on Step 1 to include these.")
                for fc in filtered_out:
                    it = fc['item']; times = fc['times']
                    st.markdown(f"**{it.get('icon','📚')} {it['course']}** — {it.get('focus','')}")
                    st.markdown("🚫 **Reason:** Doesn't match your day/time preferences")
                    if times:
                        st.markdown("⏰ Sample times:")
                        for t in times:
                            st.markdown(f"• {t}")

    st.markdown("---")
    cols = st.columns([1,1,1])
    with cols[0]:
        if st.button("← Back to quick setup", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with cols[1]:
        st.info("### 📞\n**Questions?**\n(800) 803-4058")
    with cols[2]:
        st.success("### ✅\n**Next step**\nEnroll in a class")

st.markdown("---")
st.markdown("**SAT Class Finder** • Connecting students with Varsity Tutors SAT preparation classes")
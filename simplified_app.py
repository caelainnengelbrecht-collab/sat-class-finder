import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

# =============================================
#  Simplified SAT Class Finder 
#  Connect students with Varsity Tutors SAT classes
# =============================================

st.set_page_config(page_title="SAT Class Finder", page_icon="📚", layout="wide")

# Simple styling
st.markdown("""
<style>
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
    }
}

# Progress indicator
progress_labels = ["Choose Test Date", "Select Classes", "Get Enrollment Links"]
progress = st.session_state.step / len(progress_labels)
st.progress(progress, text=f"Step {st.session_state.step} of {len(progress_labels)}: {progress_labels[st.session_state.step-1]}")

# Step 1: Test Date Selection
if st.session_state.step == 1:
    st.markdown('<div class="main-header"><h1>📚 SAT Class Finder</h1><p>Find the perfect SAT prep classes for your test date</p></div>', unsafe_allow_html=True)
    
    st.markdown("## Select Your SAT Test Date")
    
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
                    st.error("🚨 Urgent prep needed")
                
                if st.button(f"Choose {date_str}", key=f"date_{i}", use_container_width=True):
                    st.session_state.test_date = date_str
                    st.session_state.step = 2
                    st.rerun()
            else:
                st.markdown(f"### {date_str}")
                st.markdown("**Past date**")

# Step 2: Class Selection
elif st.session_state.step == 2:
    st.markdown('<div class="main-header"><h1>📝 Select Your SAT Classes</h1><p>Choose the classes that match your timeline and goals</p></div>', unsafe_allow_html=True)
    
    target_date_obj = SAT_DATES[st.session_state.test_date]
    days_until = (target_date_obj - date.today()).days
    
    st.markdown(f"## Your Test Date: {st.session_state.test_date}")
    st.markdown(f"**{days_until} days to prepare**")
    
    # Determine timeline category and recommendations
    if days_until > 56:
        timeline_status = "excellent"
        st.success("✅ Excellent timeline - All class types recommended")
        recommended_classes = list(COURSE_CATALOG.keys())
    elif days_until > 28:
        timeline_status = "good" 
        st.warning("⚡ Good timeline - Focus on intensive options")
        recommended_classes = [
            "SAT 4-Week Prep Course", "SAT 2-Week Bootcamp", "2-Week SAT Math Course", 
            "2-Week SAT ELA Course", "SAT Math Cram Session", "SAT Reading/Writing Cram Session",
            "Ultimate SAT Review Session", "Proctored Practice SAT"
        ]
    else:
        timeline_status = "urgent"
        st.error("🚨 Urgent timeline - Focus on bootcamps and cram sessions")
        recommended_classes = [
            "SAT 2-Week Bootcamp", "1-Week SAT Math Bootcamp", "1-Week SAT ELA Bootcamp",
            "SAT Math Cram Session", "SAT Reading/Writing Cram Session", "Ultimate SAT Review Session",
            "Proctored Practice SAT"
        ]
    
    st.markdown("## Recommended Classes for Your Timeline")
    
    selected_classes = []
    
    # Display recommended classes
    for course_name in recommended_classes:
        course_info = COURSE_CATALOG[course_name]
        
        st.markdown('<div class="class-card">', unsafe_allow_html=True)
        selected = st.checkbox(
            f"**{course_name}**", 
            key=f"course_{course_name}",
            help=f"{course_info['description']} | Duration: {course_info['duration']}"
        )
        st.markdown(f"*{course_info['description']}*")
        st.markdown(f"**Duration:** {course_info['duration']}")
        st.markdown(f"**Best for:** {course_info['best_for']}")
        
        if selected:
            selected_classes.append(course_name)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Update session state
    st.session_state.selected_classes = selected_classes
    
    # Show selection summary
    if selected_classes:
        st.markdown("### ✅ Your Selected Classes:")
        for class_name in selected_classes:
            st.markdown(f"• {class_name}")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Test Date", key="back_to_step1"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Get Enrollment Links →", key="continue_to_step3", disabled=(len(selected_classes) == 0)):
            st.session_state.step = 3
            st.rerun()
    
    if len(selected_classes) == 0:
        st.info("💡 Please select at least one class to continue")

# Step 3: Enrollment Links
elif st.session_state.step == 3:
    st.markdown('<div class="main-header"><h1>🎯 Your SAT Class Enrollment</h1><p>Click the links below to enroll in your selected classes</p></div>', unsafe_allow_html=True)
    
    st.markdown(f"## Test Date: {st.session_state.test_date}")
    target_date_obj = SAT_DATES[st.session_state.test_date]
    days_until = (target_date_obj - date.today()).days
    st.markdown(f"**{days_until} days to prepare**")
    
    if st.session_state.selected_classes:
        st.markdown("## 🎓 Your Selected Classes")
        st.markdown("**Click the 'Enroll Now' buttons to register for your classes:**")
        
        # Create enrollment cards for each selected class
        for course_name in st.session_state.selected_classes:
            course_info = COURSE_CATALOG[course_name]
            
            st.markdown('<div class="enrollment-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {course_name}")
                st.markdown(f"{course_info['description']}")
                st.markdown(f"**Duration:** {course_info['duration']}")
                st.markdown(f"**Best for:** {course_info['best_for']}")
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"[**🎯 Enroll Now**]({course_info['url']})")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Create summary table
        st.markdown("## 📋 Enrollment Summary")
        enrollment_data = []
        for course_name in st.session_state.selected_classes:
            course_info = COURSE_CATALOG[course_name]
            enrollment_data.append({
                "Class Name": course_name,
                "Duration": course_info['duration'],
                "Best For": course_info['best_for'],
                "Enroll": f"[Click Here]({course_info['url']})"
            })
        
        enrollment_df = pd.DataFrame(enrollment_data)
        st.dataframe(
            enrollment_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Enroll": st.column_config.LinkColumn(
                    "🎯 Enroll Now",
                    help="Click to enroll in this course"
                )
            }
        )
        
        # Contact information
        st.markdown("## 📞 Need Help?")
        st.info("**Call Varsity Tutors at (800) 803-4058** for assistance with enrollment or to find the perfect class schedule!")
        
    else:
        st.warning("⚠️ No classes selected. Please go back to select your courses.")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Class Selection", key="back_to_step2"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🔄 Start Over", key="restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown("---")
st.markdown("**SAT Class Finder** - Connecting students with Varsity Tutors SAT preparation classes")

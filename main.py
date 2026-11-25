
import pandas as pd
import streamlit as st

from database import save_student, get_students, get_latest_student, clear_students
from data.careers import careers
from ai_engine import generate_ai_recommendations


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="PathPilot India",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------------
# HELPER FUNCTION
# -----------------------------------

def split_values(value):
    if value is None:
        return []

    values = []

    for item in value.split(","):
        if item.strip() != "":
            values.append(item.strip())

    return values


# -----------------------------------
# HEADER
# -----------------------------------

st.title("🎯 PathPilot India")

st.write("Your Personal AI Career Guidance Companion")

st.divider()


# -----------------------------------
# STUDENT REGISTRATION
# -----------------------------------

st.header("Student Registration")

with st.form("student_form"):

    name = st.text_input("Enter Your Name")

    education = st.selectbox(
        "Current Education Level",
        ["Diploma", "Undergraduate", "Postgraduate"]
    )

    college = st.text_input("College / Institution")

    year = st.selectbox(
        "Current Academic Year",
        [
            "first-year",
            "second-year",
            "third-year",
            "fourth-year",
            "fifth-year"
        ]
    )

    interests = st.multiselect(
        "What activities interest you?",
        [
            "Coding",
            "Robotics",
            "Designing",
            "Research",
            "Business",
            "Problem Solving",
            "Machines",
            "Artificial Intelligence",
            "Space and Astronomy"
        ]
    )

    subjects = st.multiselect(
        "Which subjects do you enjoy?",
        [
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "Computer Science",
            "Economics"
        ]
    )

    career = st.selectbox(
        "Which career interests you?",
        [
            "Software Developer",
            "Data Scientist",
            "Mechanical Engineer",
            "Aerospace Engineer"
        ]
    )

    skills = st.text_input(
        "Your Current Skills (comma separated)"
    )

    submitted = st.form_submit_button(
        "Create My Career Profile",
        use_container_width=True
    )


if submitted:

    if name.strip() == "":
        st.error("Please enter your name.")

    elif college.strip() == "":
        st.error("Please enter your college name.")

    elif len(interests) == 0:
        st.error("Please select at least one interest.")

    elif len(subjects) == 0:
        st.error("Please select at least one subject.")

    else:

        name = name.strip()
        college = college.strip()

        skills_list = []

        for skill in skills.split(","):

            if skill.strip() != "":
                skills_list.append(skill.strip())

        save_student(
            name,
            college,
            career,
            education,
            year,
            ", ".join(interests),
            ", ".join(subjects),
            ", ".join(skills_list)
        )

        st.success("Your profile has been registered successfully!")


st.divider()


# -----------------------------------
# REGISTERED STUDENTS
# -----------------------------------

st.header("Registered Students")

students = get_students()

students_df = pd.DataFrame(
    students,
    columns=[
        "Student ID",
        "Name",
        "College",
        "Career Interest",
        "Education",
        "Year",
        "Interests",
        "Subjects",
        "Skills"
    ]
)

st.dataframe(
    students_df,
    hide_index=True,
    use_container_width=True
)


st.divider()


# -----------------------------------
# CAREER EXPLORER
# -----------------------------------

st.header("Explore Careers")

career_names = []

for career_info in careers:
    career_names.append(career_info["name"])

selected_career = st.selectbox(
    "Choose a career to explore",
    career_names
)

for career_info in careers:

    if career_info["name"] == selected_career:

        st.subheader(career_info["name"])

        st.write(career_info["description"])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Required Skills**")

            for skill in career_info["skills"]:
                st.write("•", skill)

        with col2:
            st.markdown("**Important Subjects**")

            for subject in career_info["subjects"]:
                st.write("•", subject)


st.divider()


# -----------------------------------
# STUDENT PROFILE RETRIEVAL
# -----------------------------------

st.header("AI Career Recommendations")

latest_student = get_latest_student()


if latest_student is None:

    st.info("Please register a student profile to receive career recommendations.")

else:

    student = {
        "name": latest_student[0],
        "college": latest_student[1],
        "career": latest_student[2],
        "education": latest_student[3],
        "year": latest_student[4],
        "interests": split_values(latest_student[5]),
        "subjects": split_values(latest_student[6]),
        "skills": split_values(latest_student[7])
    }


    # -----------------------------------
    # CAREER MATCHING ENGINE
    # -----------------------------------

    career_matches = []

    for career_info in careers:

        matching_skills = []
        missing_skills = []
        matching_subjects = []

        # Compare skills

        for required_skill in career_info["skills"]:

            found = False

            for student_skill in student["skills"]:

                if student_skill.lower() == required_skill.strip().lower():

                    matching_skills.append(required_skill)
                    found = True
                    break

            if found == False:
                missing_skills.append(required_skill)


        # Compare subjects

        for required_subject in career_info["subjects"]:

            for student_subject in student["subjects"]:

                if student_subject.lower() == required_subject.strip().lower():

                    matching_subjects.append(required_subject)
                    break


        # Calculate scores

        if len(career_info["skills"]) > 0:

            skill_score = (
                len(matching_skills) /
                len(career_info["skills"])
            ) * 100

        else:
            skill_score = 0


        if len(career_info["subjects"]) > 0:

            subject_score = (
                len(matching_subjects) /
                len(career_info["subjects"])
            ) * 100

        else:
            subject_score = 0


        total_score = (
            skill_score * 0.6
            + subject_score * 0.4
        )


        # Save results

        career_result = {
            "name": career_info["name"],
            "description": career_info["description"],
            "score": round(total_score, 2),
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "matching_subjects": matching_subjects
        }

        career_matches.append(career_result)


    # -----------------------------------
    # RANK CAREERS
    # -----------------------------------

    career_matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # -----------------------------------
    # DISPLAY TOP 5 RECOMMENDATIONS
    # -----------------------------------

    st.write(
        "Here are five career options based on your current skills and subjects."
    )

    for index, career_result in enumerate(career_matches[:5]):

        with st.expander(
            str(index + 1) + ". "
            + career_result["name"]
            + " — "
            + str(career_result["score"])
            + "% Match"
        ):

            st.write(career_result["description"])

            st.markdown("**Skills You Already Have**")

            if career_result["matching_skills"]:
                st.write(", ".join(career_result["matching_skills"]))
            else:
                st.write("No matching skills found yet.")

            st.markdown("**Skills You Need to Develop**")

            if career_result["missing_skills"]:
                st.write(", ".join(career_result["missing_skills"]))
            else:
                st.write("All listed skills match!")

            st.markdown("**Matching Subjects**")

            if career_result["matching_subjects"]:
                st.write(", ".join(career_result["matching_subjects"]))
            else:
                st.write("No matching subjects found yet.")


    # -----------------------------------
    # GEMINI AI ANALYSIS
    # -----------------------------------

    st.divider()

    if st.button("Get AI Career Analysis", use_container_width=True):

        try:

            with st.spinner("Gemini is analysing your profile..."):

                ai_result = generate_ai_recommendations(
                    student,
                    career_matches
                )

            st.subheader("AI Career Analysis")

            st.markdown(ai_result)

        except Exception as error:

            st.error(f"AI request failed: {error}")


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption("PathPilot India | Discover your potential. Build your future.")


# -----------------------------------
# CLEAR STUDENTS
# -----------------------------------

if st.button("Clear All Students"):

    clear_students()

    st.rerun()




  

        
        
    
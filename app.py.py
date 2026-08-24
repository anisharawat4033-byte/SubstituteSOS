import streamlit as st
import substitutesos_backend as backend

# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------

st.set_page_config(
    page_title="SubstituteSOS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)
# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #071A2F;
}

/* MAIN TEXT */
.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp div {
    color: #FFFFFF;
}

/* HEADINGS */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #FFFFFF !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #0B2545;
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* SIDEBAR RADIO OPTIONS */
[data-testid="stSidebar"] label {
    color: #FFFFFF !important;
}

/* BUTTONS */
.stButton > button,
.stDownloadButton > button {
    width: 100%;
    background-color: #2F80ED !important;
    color: #FFFFFF !important;
    border-radius: 10px;
    border: none;
    padding: 12px;
    font-weight: bold;
}

/* BUTTON HOVER */
.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #38BDF8 !important;
    color: #071A2F !important;
}

/* SUCCESS / INFO / WARNING BOX TEXT */
[data-testid="stAlert"] {
    color: #FFFFFF !important;
}
/* Streamlit top header */
header[data-testid="stHeader"] {
    background-color: #071A2F !important;
}

/* Remove extra space at the top */
[data-testid="stAppViewContainer"] {
    margin-top: 0 !important;
}

.main .block-container {
    padding-top: 2rem !important;
}
/* HIDE DATAFRAME TOOLBAR BUTTONS */
[data-testid="stDataFrame"] [data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDataFrame"] button {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)
# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("⚡ SubstituteSOS")
st.sidebar.caption("Smart scheduling. Faster substitutions.")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Dashboard",
        "📅 Timetable",
        "🚨 SubstituteSOS",
        "📋 Records",
        "⚙️ Customize Schedule"
    ]
)


# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

if page == "🏠 Dashboard":

    st.caption("SCHOOL SCHEDULING SYSTEM")

    st.title("SubstituteSOS")

    st.subheader("When the timetable changes, clashes happen.")

    st.markdown("### But the school shouldn't stop.")

    st.success("● SYSTEM READY")

    st.divider()

    st.header("What can SubstituteSOS do?")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Dynamic Timetable")

        st.write(
            "Generate schedules using classes, subjects, "
            "teacher qualifications, availability, working "
            "days, periods and weekly requirements."
        )

        if st.button(
            "GENERATE TIMETABLE",
            key="generate_dashboard"
        ):

            backend.create_demo_data()

            success = backend.generate_timetable(
                verbose=False
            )

            if success:
                st.success(
                    "Timetable generated successfully!"
                )

    with col2:
        st.subheader("🚨 SubstituteSOS")

        st.write(
            "Report a teacher's absence and find a qualified, "
            "available and conflict-free substitute for the "
            "affected class."
        )

        if st.button(
            "REPORT ABSENCE",
            key="absence_dashboard"
        ):
            st.info(
                "Go to the SubstituteSOS page to report "
                "an absence."
            )

    st.divider()

    st.header("How it works")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown("### 01")
        st.subheader("Build the timetable")
        st.write(
            "The system considers school requirements "
            "before generating the schedule."
        )

    with step2:
        st.markdown("### 02")
        st.subheader("Report the change")
        st.write(
            "When a teacher is absent, the affected class "
            "and period are identified."
        )

    with step3:
        st.markdown("### 03")
        st.subheader("Find the right match")
        st.write(
            "Qualified and available teachers are checked "
            "for timetable conflicts."
        )


# -------------------------------------------------
# TIMETABLE PAGE
# -------------------------------------------------
elif page == "⚙️ Customize Schedule":

    st.caption("SCHEDULE MANAGEMENT")
    st.title("⚙️ Customize Schedule")

    st.write(
        "Customize classes, subjects, weekly requirements and teachers "
        "before generating your timetable."
    )
        # -------------------------------------------------
    # SCHEDULE OVERVIEW
    # -------------------------------------------------

    total_classes = len(backend.data["classes"])
    total_subjects = len(backend.data["subjects"])
    total_teachers = len(backend.data["teachers"])
    periods_per_day = backend.data["settings"].get(
        "periods_per_day",
        8
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🏫 Classes",
            total_classes
        )

    with col2:
        st.metric(
            "📚 Subjects",
            total_subjects
        )

    with col3:
        st.metric(
            "👩‍🏫 Teachers",
            total_teachers
        )

    with col4:
        st.metric(
            "📅 Periods / Day",
            periods_per_day
        )

    st.divider()

    # Make sure demo data exists
    if not backend.data.get("classes"):
        backend.create_demo_data()

    st.divider()

    # =================================================
    # CLASSES
    # =================================================
    if "class_added" in st.session_state:
        st.success(
            f"✅ Class {st.session_state['class_added']} added successfully!"
        )
        del st.session_state["class_added"]

    st.header("🏫 Classes")

    classes = list(backend.data["classes"].keys())

    st.write(
        f"**{len(classes)} class(es) currently configured**"
    )

    col1, col2 = st.columns(2)

    with col1:

        new_class = st.text_input(
            "➕ Add New Class",
            placeholder="Example: 11A"
        )

        if st.button(
            "ADD CLASS",
            key="add_class"
        ):

            new_class = new_class.strip()

            if not new_class:
                st.warning("Please enter a class name.")

            elif new_class in backend.data["classes"]:
                st.warning("That class already exists.")

            else:

                backend.data["classes"][new_class] = {
                    "periods_per_day": backend.data["settings"].get(
                        "periods_per_day",
                        8
                    ),
                    "subject_requirements": {}
                }

                st.session_state["class_added"] = new_class
                st.rerun()
    with col2:

        if classes:

            class_to_remove = st.selectbox(
                "🗑️ Remove Class",
                classes,
                key="remove_class_select"
            )

            if st.button(
                "REMOVE CLASS",
                key="remove_class"
            ):

                del backend.data["classes"][class_to_remove]

                st.success(
                    f"Class {class_to_remove} removed."
                )

                st.rerun()

    st.divider()

    # =================================================
    # SUBJECTS
    # =================================================
    st.header("📚 Subjects")

    subjects = list(backend.data["subjects"].keys())

    if "subject_added" in st.session_state:
        st.success(
            f"✅ {st.session_state['subject_added']} added successfully!"
        )
        del st.session_state["subject_added"]

    st.write(
        f"**{len(subjects)} subject(s) currently configured**"
    )

    col1, col2 = st.columns(2)
    with col1:

        st.subheader("➕ Add Subject")

        new_subject = st.text_input(
            "Subject Name",
            placeholder="Example: Psychology"
        )

        if st.button(
            "ADD SUBJECT",
            key="add_subject"
        ):

            new_subject = new_subject.strip()

            if not new_subject:
                st.warning("Please enter a subject name.")

            elif new_subject in backend.data["subjects"]:
                st.warning("That subject already exists.")

            else:

                backend.data["subjects"][new_subject] = {
                    "teachers": []
                }

                st.session_state["subject_added"] = new_subject
                st.rerun()

    with col2:

        if subjects:

            subject_to_remove = st.selectbox(
                "🗑️ Remove Subject",
                subjects,
                key="remove_subject_select"
            )

            if st.button(
                "REMOVE SUBJECT",
                key="remove_subject"
            ):

                del backend.data["subjects"][subject_to_remove]

                # Remove the subject from every class
                for class_info in backend.data["classes"].values():

                    class_info.get(
                        "subject_requirements",
                        {}
                    ).pop(
                        subject_to_remove,
                        None
                    )

                # Remove the subject from teacher qualifications
                for teacher_info in backend.data["teachers"].values():

                    teacher_info["subjects"] = [
                        s
                        for s in teacher_info.get(
                            "subjects",
                            []
                        )
                        if s != subject_to_remove
                    ]

                st.success(
                    f"Subject {subject_to_remove} removed from the schedule."
                )

                st.rerun()

        else:

            st.info("No subjects configured.")

    st.divider() 
    # =================================================
    # WEEKLY PERIOD REQUIREMENTS
    # =================================================

    st.header("🔢 Weekly Period Requirements")

    if classes and subjects:

        selected_class = st.selectbox(
            "Select Class",
            classes,
            key="requirements_class"
        )

        class_requirements = backend.data["classes"][
            selected_class
        ].setdefault(
            "subject_requirements",
            {}
        )

        st.write(
            f"Set the number of weekly periods for **{selected_class}**."
        )

        for subject in subjects:

            current_value = int(
                class_requirements.get(subject, 0)
            )

            periods_required = st.number_input(
                subject,
                min_value=0,
                max_value=40,
                value=current_value,
                step=1,
                key=f"{selected_class}_{subject}_periods"
            )

            class_requirements[subject] = periods_required

    else:

        st.info(
            "Add at least one class and one subject first."
        )

    st.divider()

    # =================================================
    # TEACHERS
    # =================================================
    st.header("👩‍🏫 Teacher Management")

    teachers = list(backend.data["teachers"].keys())

    if "teacher_added" in st.session_state:
        st.success(
            f"✅ Teacher {st.session_state['teacher_added']} added successfully!"
        )
        del st.session_state["teacher_added"]

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("➕ Add Teacher")

        new_teacher = st.text_input(
            "Teacher Name",
            placeholder="Example: Kapoor"
        )

        teacher_subjects = st.multiselect(
            "Subjects they can teach",
            subjects,
            key="new_teacher_subjects"
        )

        if st.button(
            "ADD TEACHER",
            key="add_teacher"
        ):

            new_teacher = new_teacher.strip()

            if not new_teacher:
                st.warning("Please enter a teacher name.")

            elif new_teacher in backend.data["teachers"]:
                st.warning("That teacher already exists.")

            elif not teacher_subjects:
                st.warning(
                    "Select at least one subject."
                )
            else:

                backend.data["teachers"][new_teacher] = {
                    "subjects": teacher_subjects,
                    "availability": {
                        d: [True] * backend.data["settings"].get(
                            "periods_per_day",
                            8
                        )
                        for d in backend.DAYS
                    },
                    "substitute_count": 0
                }

                # Add teacher to each subject
                for subject in teacher_subjects:

                    if subject in backend.data["subjects"]:

                        if new_teacher not in backend.data[
                            "subjects"
                        ][subject]["teachers"]:

                            backend.data["subjects"][
                                subject
                            ]["teachers"].append(
                                new_teacher
                            )

                st.session_state["teacher_added"] = new_teacher
                st.rerun()

    with col2:

        st.subheader("🗑️ Remove Teacher")

        if teachers:

            teacher_to_remove = st.selectbox(
                "Select Teacher",
                teachers,
                key="remove_teacher_select"
            )

            if st.button(
                "REMOVE TEACHER",
                key="remove_teacher"
            ):

                del backend.data["teachers"][
                    teacher_to_remove
                ]

                # Remove teacher from subject lists
                for subject_info in backend.data[
                    "subjects"
                ].values():

                    subject_info["teachers"] = [
                        teacher
                        for teacher in subject_info.get(
                            "teachers",
                            []
                        )
                        if teacher != teacher_to_remove
                    ]

                st.success(
                    f"Teacher {teacher_to_remove} removed."
                )

                st.rerun()

        else:

            st.info("No teachers configured.")

    st.divider()

    # =================================================
    # REGENERATE TIMETABLE
    # =================================================

    st.header("🔄 Apply Changes")

    st.write(
        "Save your customized schedule structure and "
        "generate a new timetable."
    )

    if st.button(
        "🚀 GENERATE UPDATED TIMETABLE",
        type="primary",
        use_container_width=True,
        key="generate_custom_timetable"
    ):

        success = backend.generate_timetable(
            verbose=False
        )

        if success:
            backend.save_data()
            st.success(
                "✅ Updated timetable generated successfully!"
            )
            st.info(
                "Your new classes, subjects, teachers and "
                "weekly requirements have been applied."
            )

        else:

            st.error(
                "The timetable could not be generated. "
                "Check your class requirements, subjects "
                "and teacher qualifications."
            )
elif page == "📅 Timetable":

    st.title("📅 Dynamic Timetable")

    st.write(
        "Generate and view the school timetable."
    )

    if st.button("Generate Demo Timetable"):

        backend.create_demo_data()

        success = backend.generate_timetable(
            verbose=False
        )

        if success:
            st.success(
                "Timetable generated successfully!"
            )

    if backend.data.get("timetable"):

        classes = list(
            backend.data["classes"].keys()
        )

        selected_class = st.selectbox(
            "Select Class",
            classes
        )

        timetable = backend.data["timetable"].get(
            selected_class,
            {}
        )

        table_data = []

        for day in backend.DAYS:

            row = {"Day": day}

            for p in range(
                1,
                backend.periods() + 1
            ):

                entry = timetable.get(
                    day,
                    {}
                ).get(str(p))

                if not entry:

                    row[f"P{p}"] = "FREE"

                elif entry.get("type") == "activity":

                    row[f"P{p}"] = entry.get(
                        "subject",
                        "Activity"
                    )

                else:

                    subject = entry.get(
                        "subject",
                        ""
                    )

                    teacher = entry.get(
                        "teacher",
                        ""
                    )

                    substitute = entry.get(
                        "substitute_teacher"
                    )

                    if substitute:

                        row[f"P{p}"] = (
                            f"{subject} | SUB: {substitute}"
                        )

                    else:

                        row[f"P{p}"] = (
                            f"{subject} | {teacher}"
                        )

            table_data.append(row)

        st.subheader(
            f"Timetable — {selected_class}"
        )

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )
        import pandas as pd

        export_df = pd.DataFrame(table_data)

        csv = export_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 DOWNLOAD TIMETABLE (CSV)",
            data=csv,
            file_name=f"{selected_class}_timetable.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:

        st.info(
            "Generate the timetable first."
        )
# -------------------------------------------------
# SUBSTITUTE SOS PAGE
# -------------------------------------------------

elif page == "🚨 SubstituteSOS":

    st.title("🚨 SubstituteSOS")

    st.write(
        "Report a teacher absence and find a suitable "
        "substitute."
    )

    if not backend.data.get("timetable"):

        st.warning(
            "Please generate the timetable first."
        )

    else:

        teachers = list(
            backend.data["teachers"].keys()
        )

        absent_teacher = st.selectbox(
            "Select Absent Teacher",
            teachers
        )

        day = st.selectbox(
            "Select Day",
            backend.DAYS
        )

        period = st.selectbox(
            "Select Period",
            list(
                range(
                    1,
                    backend.periods() + 1
                )
            )
        )

        if st.button("FIND SUBSTITUTE"):

            affected = backend.affected_classes(
                absent_teacher,
                day,
                period
            )

            if not affected:

                st.session_state.pop(
                    "substitution_result",
                    None
                )

                st.warning(
                    "This teacher has no scheduled class "
                    "during this period."
                )

            else:

                cls, entry = affected[0]

                subject = entry.get(
                    "subject",
                    ""
                )

                candidates = (
                    backend.substitute_candidates(
                        absent_teacher,
                        subject,
                        day,
                        period
                    )
                )

                if candidates:

                    recommended = candidates[0][1]

                    st.session_state[
                        "substitution_result"
                    ] = {
                        "absent_teacher": absent_teacher,
                        "day": day,
                        "period": period,
                        "class": cls,
                        "subject": subject,
                        "recommended": recommended
                    }

                else:

                    st.session_state.pop(
                        "substitution_result",
                        None
                    )

                    st.error(
                        "No qualified substitute "
                        "is currently available."
                    )


        # SHOW SAVED SEARCH RESULT

        if "substitution_result" in st.session_state:

            result = st.session_state[
                "substitution_result"
            ]

            st.subheader(
                f"Affected Class: {result['class']}"
            )

            st.write(
                f"Subject: {result['subject']}"
            )

            st.success(
                f"Recommended Substitute: "
                f"{result['recommended']}"
            )

            st.write(
                "✓ Qualified\n\n"
                "✓ Available\n\n"
                "✓ Conflict-Free"
            )

            if st.button(
                f"Assign {result['recommended']}",
                key="assign_substitute"
            ):

                cls = result["class"]
                selected_day = result["day"]
                selected_period = result["period"]
                recommended = result["recommended"]
                absent = result["absent_teacher"]

                entry = backend.data[
                    "timetable"
                ][cls][selected_day][
                    str(selected_period)
                ]

                entry[
                    "substitute_for"
                ] = absent

                entry[
                    "substitute_teacher"
                ] = recommended

                backend.data[
                    "substitutions"
                ][
                    f"{cls}|{selected_day}|{selected_period}"
                ] = recommended

                backend.data[
                    "teachers"
                ][recommended][
                    "substitute_count"
                ] += 1

                st.success(
                    f"🎉 {recommended} successfully "
                    f"assigned to {cls}!"
                )

                st.session_state.pop(
                    "substitution_result",
                    None
                )
# -------------------------------------------------
# RECORDS PAGE
# -------------------------------------------------

elif page == "📋 Records":

    st.title("📋 Substitution Records")

    if backend.data.get("substitutions"):

        records = []

        for slot, teacher in backend.data[
            "substitutions"
        ].items():

            cls, day, period = slot.split("|")

            records.append({
                "Class": cls,
                "Day": day,
                "Period": period,
                "Substitute Teacher": teacher
            })

        st.dataframe(
            records,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No substitutions have been recorded yet."
        )

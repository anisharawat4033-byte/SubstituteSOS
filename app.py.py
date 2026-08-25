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

/* ---------------------------------------------- */
/* CARD-STYLE CONTAINERS (bordered containers)     */
/* ---------------------------------------------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #0B2545;
    border: 1px solid #1B3A5C !important;
    border-radius: 14px !important;
    padding: 6px;
}

/* METRIC TILES */
[data-testid="stMetric"] {
    background-color: #0B2545;
    border: 1px solid #1B3A5C;
    border-radius: 14px;
    padding: 16px 12px;
}

[data-testid="stMetricLabel"] {
    color: #9FB6D0 !important;
}

[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
}

/* ---------------------------------------------- */
/* STATUS BADGES (used via st.markdown HTML)       */
/* ---------------------------------------------- */
.sos-badge {
    display: inline-block;
    padding: 6px 14px;
    margin: 4px 6px 4px 0;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.85rem;
}
.sos-badge-green {
    background-color: rgba(46, 204, 113, 0.15);
    color: #4ADE80 !important;
    border: 1px solid rgba(74, 222, 128, 0.4);
}
.sos-badge-red {
    background-color: rgba(231, 76, 60, 0.15);
    color: #F87171 !important;
    border: 1px solid rgba(248, 113, 113, 0.4);
}
.sos-badge-blue {
    background-color: rgba(56, 189, 248, 0.15);
    color: #38BDF8 !important;
    border: 1px solid rgba(56, 189, 248, 0.4);
}

/* ---------------------------------------------- */
/* FREE-PERIOD HIGHLIGHT inside styled dataframes  */
/* (applies to cells rendered with the .free-cell  */
/* class through pandas Styler)                    */
/* ---------------------------------------------- */
.free-cell {
    background-color: rgba(46, 204, 113, 0.18) !important;
    color: #4ADE80 !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


def badge(text, color="blue"):
    """Return HTML for a small colored pill badge."""
    return f'<span class="sos-badge sos-badge-{color}">{text}</span>'


def style_timetable_df(df):
    """Apply green highlighting to FREE cells in a timetable dataframe."""
    def highlight(val):
        if isinstance(val, str) and val.strip() == "FREE":
            return "background-color: rgba(46,204,113,0.18); color:#4ADE80; font-weight:600;"
        return ""
    return df.style.applymap(highlight)
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
        "🧑‍🏫 Teacher Schedule",
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

    st.markdown(badge("● SYSTEM READY", "green"), unsafe_allow_html=True)

    st.divider()

    st.header("What can SubstituteSOS do?")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
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
        with st.container(border=True):
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
        with st.container(border=True):
            st.markdown("### 01")
            st.subheader("Build the timetable")
            st.write(
                "The system considers school requirements "
                "before generating the schedule."
            )

    with step2:
        with st.container(border=True):
            st.markdown("### 02")
            st.subheader("Report the change")
            st.write(
                "When a teacher is absent, the affected class "
                "and period are identified."
            )

    with step3:
        with st.container(border=True):
            st.markdown("### 03")
            st.subheader("Find the right match")
            st.write(
                "Qualified and available teachers are checked "
                "for timetable conflicts."
            )

    st.divider()

    # -------------------------------------------------
    # WHO'S FREE RIGHT NOW — quick lookup widget
    # -------------------------------------------------
    st.header("🔎 Who's free right now?")

    if not backend.data.get("timetable"):
        st.info("Generate the timetable first to use this lookup.")
    else:
        col_day, col_period = st.columns(2)

        with col_day:
            free_day = st.selectbox(
                "Day",
                backend.DAYS,
                key="free_lookup_day"
            )

        with col_period:
            free_period = st.selectbox(
                "Period",
                list(range(1, backend.periods() + 1)),
                key="free_lookup_period"
            )

        free_teachers = []
        busy_teachers = []

        for teacher_name in backend.data["teachers"]:
            is_busy = False

            for cls, cls_timetable in backend.data["timetable"].items():
                entry = cls_timetable.get(free_day, {}).get(str(free_period))

                if entry and entry.get("type") != "activity":
                    active_teacher = entry.get("substitute_teacher") or entry.get("teacher")

                    if active_teacher == teacher_name:
                        is_busy = True
                        busy_teachers.append((teacher_name, cls, entry.get("subject", "")))
                        break

            if not is_busy:
                free_teachers.append(teacher_name)

        st.markdown(
            "".join(badge(name, "green") for name in free_teachers)
            or "*No teachers free this period.*",
            unsafe_allow_html=True
        )

        with st.expander("Show who's busy this period"):
            if busy_teachers:
                for name, cls, subject in busy_teachers:
                    st.write(f"🔴 **{name}** — {subject} in {cls}")
            else:
                st.write("Nobody is scheduled this period.")


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

        import pandas as pd

        display_df = pd.DataFrame(table_data)

        st.dataframe(
            style_timetable_df(display_df),
            use_container_width=True,
            hide_index=True
        )

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
# TEACHER SCHEDULE PAGE
# -------------------------------------------------

elif page == "🧑‍🏫 Teacher Schedule":

    st.title("🧑‍🏫 Teacher Schedule")

    st.write(
        "View any teacher's personal weekly timetable — see what "
        "they teach, in which class, and which periods they're "
        "free."
    )

    if not backend.data.get("timetable"):

        st.info(
            "Generate the timetable first to view teacher schedules."
        )

    else:

        teachers = list(backend.data["teachers"].keys())

        selected_teacher = st.selectbox(
            "Select Teacher",
            teachers
        )

        subjects_taught = backend.data["teachers"][selected_teacher].get(
            "subjects", []
        )

        st.markdown(
            "**Qualified to teach:** "
            + "".join(badge(s, "blue") for s in subjects_taught),
            unsafe_allow_html=True
        )

        table_data = []
        free_count = 0
        class_count = 0

        for day in backend.DAYS:

            row = {"Day": day}

            for p in range(1, backend.periods() + 1):

                found = None

                for cls, cls_timetable in backend.data["timetable"].items():

                    entry = cls_timetable.get(day, {}).get(str(p))

                    if not entry or entry.get("type") == "activity":
                        continue

                    active_teacher = (
                        entry.get("substitute_teacher")
                        or entry.get("teacher")
                    )

                    if active_teacher == selected_teacher:
                        found = (cls, entry)
                        break

                if not found:
                    row[f"P{p}"] = "FREE"
                    free_count += 1
                else:
                    cls, entry = found
                    subject = entry.get("subject", "")
                    is_sub = entry.get("substitute_teacher") == selected_teacher

                    row[f"P{p}"] = (
                        f"{subject} | {cls}" + (" (SUB)" if is_sub else "")
                    )
                    class_count += 1

            table_data.append(row)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("📚 Classes this week", class_count)

        with col2:
            st.metric("🟢 Free periods this week", free_count)

        st.divider()

        st.subheader(f"Weekly Schedule — {selected_teacher}")

        import pandas as pd

        schedule_df = pd.DataFrame(table_data)

        st.dataframe(
            style_timetable_df(schedule_df),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("Find a free period")

        lookup_day = st.selectbox(
            "Day",
            backend.DAYS,
            key="teacher_lookup_day"
        )

        lookup_period = st.selectbox(
            "Period",
            list(range(1, backend.periods() + 1)),
            key="teacher_lookup_period"
        )

        day_row = next(
            (r for r in table_data if r["Day"] == lookup_day), None
        )

        if day_row:
            status = day_row.get(f"P{lookup_period}", "FREE")

            if status == "FREE":
                st.markdown(
                    badge(f"✓ {selected_teacher} is FREE at {lookup_day} P{lookup_period}", "green"),
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    badge(f"✗ Busy: {status}", "red"),
                    unsafe_allow_html=True
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

            st.markdown(
                badge("✓ Qualified", "green")
                + badge("✓ Available", "green")
                + badge("✓ Conflict-Free", "green"),
                unsafe_allow_html=True
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

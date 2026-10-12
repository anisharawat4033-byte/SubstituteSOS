
import streamlit as st
import pandas as pd
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
.stApp {
    background-color: #071A2F;
}
.stApp, .stApp p, .stApp span, .stApp label, .stApp div {
    color: #FFFFFF;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] {
    background-color: #0B2545;
}
section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
header[data-testid="stHeader"] {
    background-color: #071A2F !important;
}
.main .block-container {
    padding-top: 2rem !important;
}
.stButton > button, .stDownloadButton > button {
    width: 100%;
    background-color: #2F80ED !important;
    color: #FFFFFF !important;
    border-radius: 10px;
    border: none;
    padding: 12px;
    font-weight: bold;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #38BDF8 !important;
    color: #071A2F !important;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #0B2545;
    border: 1px solid #1B3A5C !important;
    border-radius: 14px !important;
    padding: 6px;
}
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
.sos-badge {
    display: inline-block;
    padding: 6px 14px;
    margin: 4px 6px 4px 0;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.85rem;
}
.sos-badge-green {
    background-color: rgba(46,204,113,0.15);
    color: #4ADE80 !important;
    border: 1px solid rgba(74,222,128,0.4);
}
.sos-badge-red {
    background-color: rgba(231,76,60,0.15);
    color: #F87171 !important;
    border: 1px solid rgba(248,113,113,0.4);
}
.sos-badge-blue {
    background-color: rgba(56,189,248,0.15);
    color: #38BDF8 !important;
    border: 1px solid rgba(56,189,248,0.4);
}
</style>
""", unsafe_allow_html=True)


def badge(text, color="blue"):
    """Return HTML for a colored status badge."""
    return (
        f'<span class="sos-badge sos-badge-{color}">'
        f'{text}</span>'
    )


def style_timetable_df(df):
    """Highlight FREE periods."""
    def highlight(value):
        if isinstance(value, str) and value.strip() == "FREE":
            return (
                "background-color: rgba(46,204,113,0.18);"
                "color:#4ADE80;font-weight:600;"
            )
        return ""

    return df.style.map(highlight)


# -------------------------------------------------
# SIDEBAR NAVIGATION
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
    st.markdown(
        badge("● SYSTEM READY", "green"),
        unsafe_allow_html=True
    )

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
                success = backend.generate_timetable(verbose=False)

                if success:
                    backend.save_data()
                    st.success("Timetable generated successfully!")
                else:
                    st.error(
                        "Timetable generation failed. Check your "
                        "classes, subjects and teacher qualifications."
                    )

    with col2:
        with st.container(border=True):
            st.subheader("🚨 SubstituteSOS")
            st.write(
                "Report a teacher's absence and find a qualified, "
                "available and conflict-free substitute."
            )

            if st.button(
                "REPORT ABSENCE",
                key="absence_dashboard"
            ):
                st.info(
                    "Select the SubstituteSOS page in the sidebar "
                    "to report an absence."
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
                entry = cls_timetable.get(
                    free_day, {}
                ).get(str(free_period))

                if entry and entry.get("type") != "activity":
                    active_teacher = (
                        entry.get("substitute_teacher")
                        or entry.get("teacher")
                    )

                    if active_teacher == teacher_name:
                        is_busy = True
                        busy_teachers.append(
                            (
                                teacher_name,
                                cls,
                                entry.get("subject", "")
                            )
                        )
                        break

            if is_busy:
                continue

            free_teachers.append(teacher_name)

        st.markdown(
            "".join(
                badge(name, "green") for name in free_teachers
            ) or "*No teachers free this period.*",
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
# IMPORTANT: This elif starts at the LEFT EDGE.
# -------------------------------------------------

elif page == "📅 Timetable":

    st.title("📅 Dynamic Timetable")
    st.write("Generate and view the school timetable.")

    if st.button("Generate Demo Timetable"):
        backend.create_demo_data()
        success = backend.generate_timetable(verbose=False)

        if success:
            backend.save_data()
            st.success("Timetable generated successfully!")
        else:
            st.error(
                "Timetable generation failed. Check the schedule "
                "requirements and teacher qualifications."
            )

    if backend.data.get("timetable"):
        classes = list(backend.data["classes"].keys())

        if classes:
            selected_class = st.selectbox(
                "Select Class",
                classes,
                key="timetable_class"
            )

            timetable = backend.data["timetable"].get(
                selected_class, {}
            )

            table_data = []

            for day in backend.DAYS:
                row = {"Day": day}

                for p in range(1, backend.periods() + 1):
                    entry = timetable.get(day, {}).get(str(p))

                    if not entry:
                        row[f"P{p}"] = "FREE"

                    elif entry.get("type") == "activity":
                        row[f"P{p}"] = entry.get(
                            "subject", "Activity"
                        )

                    else:
                        subject = entry.get("subject", "")
                        teacher = entry.get("teacher", "")
                        substitute = entry.get("substitute_teacher")

                        if substitute:
                            row[f"P{p}"] = (
                                f"{subject} | SUB: {substitute}"
                            )
                        else:
                            row[f"P{p}"] = f"{subject} | {teacher}"

                table_data.append(row)

            st.subheader(f"Timetable — {selected_class}")

            display_df = pd.DataFrame(table_data)

            st.dataframe(
                style_timetable_df(display_df),
                use_container_width=True,
                hide_index=True
            )

            csv = display_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 DOWNLOAD TIMETABLE (CSV)",
                data=csv,
                file_name=f"{selected_class}_timetable.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Add a class before viewing the timetable.")

    else:
        st.info("Generate the timetable first.")


# -------------------------------------------------
# TEACHER SCHEDULE PAGE
# -------------------------------------------------

elif page == "🧑‍🏫 Teacher Schedule":

    st.title("🧑‍🏫 Teacher Schedule")
    st.write(
        "View a teacher's weekly timetable, including classes "
        "they teach and periods when they are free."
    )

    if not backend.data.get("timetable"):
        st.info(
            "Generate the timetable first to view teacher schedules."
        )

    else:
        teachers = list(backend.data["teachers"].keys())

        if not teachers:
            st.info("No teachers have been configured.")

        else:
            selected_teacher = st.selectbox(
                "Select Teacher",
                teachers,
                key="teacher_schedule_select"
            )

            subjects_taught = backend.data["teachers"][
                selected_teacher
            ].get("subjects", [])

            st.markdown(
                "**Qualified to teach:** "
                + "".join(
                    badge(subject, "blue")
                    for subject in subjects_taught
                ),
                unsafe_allow_html=True
            )

            table_data = []
            free_count = 0
            class_count = 0

            for day in backend.DAYS:
                row = {"Day": day}

                for p in range(1, backend.periods() + 1):
                    found = None

                    for cls, cls_timetable in (
                        backend.data["timetable"].items()
                    ):
                        entry = cls_timetable.get(
                            day, {}
                        ).get(str(p))

                        if (
                            not entry
                            or entry.get("type") == "activity"
                        ):
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
                        is_sub = (
                            entry.get("substitute_teacher")
                            == selected_teacher
                        )

                        row[f"P{p}"] = (
                            f"{subject} | {cls}"
                            + (" (SUB)" if is_sub else "")
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
                (
                    row for row in table_data
                    if row["Day"] == lookup_day
                ),
                None
            )

            if day_row:
                status = day_row.get(
                    f"P{lookup_period}", "FREE"
                )

                if status == "FREE":
                    st.markdown(
                        badge(
                            f"✓ {selected_teacher} is FREE at "
                            f"{lookup_day} P{lookup_period}",
                            "green"
                        ),
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
        "Report a teacher absence and find a suitable substitute."
    )

    if not backend.data.get("timetable"):
        st.warning("Please generate the timetable first.")

    else:
        teachers = list(backend.data["teachers"].keys())

        if not teachers:
            st.info("No teachers have been configured.")

        else:
            absent_teacher = st.selectbox(
                "Select Absent Teacher",
                teachers,
                key="absent_teacher_select"
            )

            day = st.selectbox(
                "Select Day",
                backend.DAYS,
                key="absence_day_select"
            )

            period = st.selectbox(
                "Select Period",
                list(range(1, backend.periods() + 1)),
                key="absence_period_select"
            )

            if st.button("FIND SUBSTITUTE"):
                affected = backend.affected_classes(
                    absent_teacher,
                    day,
                    period
                )

                if not affected:
                    st.session_state.pop(
                        "substitution_result", None
                    )
                    st.warning(
                        "This teacher has no scheduled class "
                        "during this period."
                    )

                else:
                    cls, entry = affected[0]
                    subject = entry.get("subject", "")

                    candidates = backend.substitute_candidates(
                        absent_teacher,
                        subject,
                        day,
                        period
                    )

                    if candidates:
                        recommended = candidates[0][1]

                        st.session_state["substitution_result"] = {
                            "absent_teacher": absent_teacher,
                            "day": day,
                            "period": period,
                            "class": cls,
                            "subject": subject,
                            "recommended": recommended
                        }
                    else:
                        st.session_state.pop(
                            "substitution_result", None
                        )
                        st.error(
                            "No qualified substitute is currently "
                            "available for this period."
                        )

            if "substitution_result" in st.session_state:
                result = st.session_state["substitution_result"]

                st.subheader(
                    f"Affected Class: {result['class']}"
                )
                st.write(f"Subject: {result['subject']}")

                st.success(
                    "Recommended Substitute: "
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
                    ][cls][selected_day][str(selected_period)]

                    entry["substitute_for"] = absent
                    entry["substitute_teacher"] = recommended

                    backend.data.setdefault(
                        "substitutions", {}
                    )[
                        f"{cls}|{selected_day}|{selected_period}"
                    ] = recommended

                    backend.data["teachers"][
                        recommended
                    ]["substitute_count"] = (
                        backend.data["teachers"][
                            recommended
                        ].get("substitute_count", 0) + 1
                    )

                    backend.save_data()

                    st.success(
                        f"🎉 {recommended} successfully assigned "
                        f"to {cls}!"
                    )

                    st.session_state.pop(
                        "substitution_result", None
                    )


# -------------------------------------------------
# RECORDS PAGE
# -------------------------------------------------

elif page == "📋 Records":

    st.title("📋 Substitution Records")

    substitutions = backend.data.get("substitutions", {})

    if substitutions:
        records = []

        for slot, teacher in substitutions.items():
            parts = slot.split("|")

            if len(parts) != 3:
                continue

            cls, day, period = parts

            records.append({
                "Class": cls,
                "Day": day,
                "Period": period,
                "Substitute Teacher": teacher
            })

        if records:
            st.dataframe(
                pd.DataFrame(records),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No valid substitution records found.")

    else:
        st.info("No substitutions have been recorded yet.")


# -------------------------------------------------
# CUSTOMIZE SCHEDULE PAGE
# -------------------------------------------------

elif page == "⚙️ Customize Schedule":

    st.caption("SCHEDULE MANAGEMENT")
    st.title("⚙️ Customize Schedule")

    st.write(
        "Customize classes, subjects, weekly requirements and "
        "teachers before generating your timetable."
    )

    # Create initial data only if classes are missing.
    if not backend.data.get("classes"):
        backend.create_demo_data()

    # ---------------------------------------------
    # SCHEDULE OVERVIEW
    # ---------------------------------------------

    total_classes = len(backend.data["classes"])
    total_subjects = len(backend.data["subjects"])
    total_teachers = len(backend.data["teachers"])

    periods_per_day = backend.data["settings"].get(
        "periods_per_day", 8
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🏫 Classes", total_classes)

    with col2:
        st.metric("📚 Subjects", total_subjects)

    with col3:
        st.metric("👩‍🏫 Teachers", total_teachers)

    with col4:
        st.metric("📅 Periods / Day", periods_per_day)

    st.divider()

    # ---------------------------------------------
    # CLASSES
    # ---------------------------------------------

    st.header("🏫 Classes")

    classes = list(backend.data["classes"].keys())

    st.write(f"**{len(classes)} class(es) currently configured**")

    col1, col2 = st.columns(2)

    with col1:
        new_class = st.text_input(
            "➕ Add New Class",
            placeholder="Example: 11A",
            key="new_class_name"
        )

        if st.button("ADD CLASS", key="add_class"):
            new_class = new_class.strip()

            if not new_class:
                st.warning("Please enter a class name.")

            elif new_class in backend.data["classes"]:
                st.warning("That class already exists.")

            else:
                backend.data["classes"][new_class] = {
                    "periods_per_day": periods_per_day,
                    "subject_requirements": {}
                }
                backend.save_data()
                st.success(f"Class {new_class} added.")
                st.rerun()

    with col2:
        if classes:
            class_to_remove = st.selectbox(
                "🗑️ Remove Class",
                classes,
                key="remove_class_select"
            )

            if st.button("REMOVE CLASS", key="remove_class"):
                del backend.data["classes"][class_to_remove]
                backend.save_data()
                st.success(f"Class {class_to_remove} removed.")
                st.rerun()

    st.divider()

    # ---------------------------------------------
    # SUBJECTS
    # ---------------------------------------------

    st.header("📚 Subjects")

    subjects = list(backend.data["subjects"].keys())

    st.write(
        f"**{len(subjects)} subject(s) currently configured**"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("➕ Add Subject")

        new_subject = st.text_input(
            "Subject Name",
            placeholder="Example: Psychology",
            key="new_subject_name"
        )

        if st.button("ADD SUBJECT", key="add_subject"):
            new_subject = new_subject.strip()

            if not new_subject:
                st.warning("Please enter a subject name.")

            elif new_subject in backend.data["subjects"]:
                st.warning("That subject already exists.")

            else:
                backend.data["subjects"][new_subject] = {
                    "teachers": []
                }
                backend.save_data()
                st.success(f"Subject {new_subject} added.")
                st.rerun()

    with col2:
        if subjects:
            subject_to_remove = st.selectbox(
                "🗑️ Remove Subject",
                subjects,
                key="remove_subject_select"
            )

            if st.button("REMOVE SUBJECT", key="remove_subject"):
                del backend.data["subjects"][subject_to_remove]

                for class_info in backend.data["classes"].values():
                    class_info.get(
                        "subject_requirements", {}
                    ).pop(subject_to_remove, None)

                for teacher_info in backend.data["teachers"].values():
                    teacher_info["subjects"] = [
                        subject
                        for subject in teacher_info.get("subjects", [])
                        if subject != subject_to_remove
                    ]

                backend.save_data()
                st.success(
                    f"Subject {subject_to_remove} removed."
                )
                st.rerun()
        else:
            st.info("No subjects configured.")

    st.divider()

    # ---------------------------------------------
    # WEEKLY PERIOD REQUIREMENTS
    # ---------------------------------------------

    st.header("🔢 Weekly Period Requirements")

    classes = list(backend.data["classes"].keys())
    subjects = list(backend.data["subjects"].keys())

    if classes and subjects:
        selected_class = st.selectbox(
            "Select Class",
            classes,
            key="requirements_class"
        )

        class_requirements = backend.data["classes"][
            selected_class
        ].setdefault("subject_requirements", {})

        st.write(
            f"Set the number of weekly periods for "
            f"**{selected_class}**."
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

        if st.button(
            "SAVE WEEKLY REQUIREMENTS",
            key="save_requirements"
        ):
            backend.save_data()
            st.success("Weekly requirements saved.")

    else:
        st.info("Add at least one class and one subject first.")

    st.divider()

    # ---------------------------------------------
    # TEACHER MANAGEMENT
    # ---------------------------------------------

    st.header("👩‍🏫 Teacher Management")

    teachers = list(backend.data["teachers"].keys())
    subjects = list(backend.data["subjects"].keys())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("➕ Add Teacher")

        new_teacher = st.text_input(
            "Teacher Name",
            placeholder="Example: Kapoor",
            key="new_teacher_name"
        )

        teacher_subjects = st.multiselect(
            "Subjects they can teach",
            subjects,
            key="new_teacher_subjects"
        )

        if st.button("ADD TEACHER", key="add_teacher"):
            new_teacher = new_teacher.strip()

            if not new_teacher:
                st.warning("Please enter a teacher name.")

            elif new_teacher in backend.data["teachers"]:
                st.warning("That teacher already exists.")

            elif not teacher_subjects:
                st.warning("Select at least one subject.")

            else:
                backend.data["teachers"][new_teacher] = {
                    "subjects": teacher_subjects,
                    "availability": {
                        day: [True] * periods_per_day
                        for day in backend.DAYS
                    },
                    "substitute_count": 0
                }

                for subject in teacher_subjects:
                    if subject in backend.data["subjects"]:
                        subject_teachers = backend.data[
                            "subjects"
                        ][subject].setdefault("teachers", [])

                        if new_teacher not in subject_teachers:
                            subject_teachers.append(new_teacher)

                backend.save_data()
                st.success(f"Teacher {new_teacher} added.")
                st.rerun()

    with col2:
        st.subheader("🗑️ Remove Teacher")

        if teachers:
            teacher_to_remove = st.selectbox(
                "Select Teacher",
                teachers,
                key="remove_teacher_select"
            )

            if st.button("REMOVE TEACHER", key="remove_teacher"):
                del backend.data["teachers"][teacher_to_remove]

                for subject_info in backend.data["subjects"].values():
                    subject_info["teachers"] = [
                        teacher
                        for teacher in subject_info.get("teachers", [])
                        if teacher != teacher_to_remove
                    ]

                backend.save_data()
                st.success(f"Teacher {teacher_to_remove} removed.")
                st.rerun()

        else:
            st.info("No teachers configured.")

    st.divider()

    # ---------------------------------------------
    # APPLY CHANGES
    # ---------------------------------------------

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
        # Do NOT call create_demo_data() here.
        # That would replace the customized data with demo data.
        backend.save_data()

        success = backend.generate_timetable(verbose=False)

        if success:
            backend.save_data()
            st.success("✅ Updated timetable generated successfully!")
            st.info(
                "Your configured classes, subjects, teachers and "
                "weekly requirements have been applied."
            )
        else:
            st.error("The timetable could not be generated.")
            st.warning(
                "Check your class requirements, subject assignments, "
                "teacher qualifications and available periods."
            )

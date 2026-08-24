#!/usr/bin/env python3
"""
SubstituteSOS — Smart Dynamic Timetable & Substitute Management System

Standard-library-only Python project for a school hackathon.
Run with:
    python SubstituteSOS_FINAL.py

Main demo:
    Main menu -> 5. Run Live Hackathon Demo
"""

import json
import os
from collections import defaultdict

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MAX_PERIODS = 8

data = {
    "settings": {"periods_per_day": 8, "school_days": DAYS[:]},
    "classes": {},
    "teachers": {},
    "subjects": {},
    "fixed_activities": {},
    "timetable": {},
    "absences": {},
    "substitutions": {},
}
# ----------------------------- DATA PERSISTENCE ---------------------------

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "substitutesos_data.json"
)


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4
        )


def load_data():
    global data

    if os.path.exists(DATA_FILE):
        try:
            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            print("Saved SubstituteSOS data loaded.")

        except (
            json.JSONDecodeError,
            OSError
        ):
            print(
                "Could not load saved data. "
                "Starting with empty data."
            )
load_data()
# ----------------------------- UTILITIES ---------------------------------

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def ask(prompt, default=None):
    value = input(prompt).strip()
    return default if not value and default is not None else value


def ask_int(prompt, minimum, maximum, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            value = int(raw)
            if minimum <= value <= maximum:
                return value
        except ValueError:
            pass
        print(f"Please enter a number from {minimum} to {maximum}.")


def yes_no(prompt, default=True):
    suffix = " [Y/n]: " if default else " [y/N]: "
    raw = input(prompt + suffix).strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes")


def periods():
    return int(data["settings"].get("periods_per_day", 8))


def save_data(filename="substitutesos_data.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except OSError as exc:
        print("Could not save:", exc)
        return False


def load_data(filename="substitutesos_data.json"):
    global data
    if not os.path.exists(filename):
        return False
    try:
        with open(filename, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        if isinstance(loaded, dict):
            for key in data:
                if key in loaded:
                    data[key] = loaded[key]
            return True
    except (OSError, json.JSONDecodeError) as exc:
        print("Could not load:", exc)
    return False


# ----------------------------- CLASSES -----------------------------------

def manage_classes():
    while True:
        clear_screen()
        print("=== MANAGE CLASSES ===")
        print("1. Add class")
        print("2. Edit class")
        print("3. Remove class")
        print("4. View classes")
        print("5. Back")
        choice = ask_int("Choose: ", 1, 5)

        if choice == 1:
            name = ask("Class name (e.g. 9A): ")
            if not name:
                continue
            if name in data["classes"]:
                print("That class already exists.")
                pause()
                continue

            print("\nAll school days use the same period structure.")
            p = ask_int(
                f"Number of periods per day (1-{MAX_PERIODS}) [8]: ",
                1, MAX_PERIODS, 8
            )

            if not data["classes"]:
                data["settings"]["periods_per_day"] = p
            elif p != periods():
                print(f"Using the existing school-wide value: {periods()} periods/day.")

            data["classes"][name] = {
                "periods_per_day": periods(),
                "subject_requirements": {},
            }
            print(f"Class {name} added.")
            pause()

        elif choice == 2:
            names = list(data["classes"])
            if not names:
                print("No classes yet.")
                pause()
                continue
            for i, n in enumerate(names, 1):
                print(f"{i}. {n}")
            old = names[ask_int("Select class: ", 1, len(names)) - 1]
            new = ask(f"New name [{old}]: ", old)
            if new != old and new in data["classes"]:
                print("That name already exists.")
            else:
                data["classes"][new] = data["classes"].pop(old)
                print("Updated.")
            pause()

        elif choice == 3:
            names = list(data["classes"])
            if not names:
                print("No classes yet.")
                pause()
                continue
            for i, n in enumerate(names, 1):
                print(f"{i}. {n}")
            cls = names[ask_int("Select class: ", 1, len(names)) - 1]
            if yes_no(f"Remove {cls}?", False):
                del data["classes"][cls]
                data["timetable"].pop(cls, None)
                print("Removed.")
            pause()

        elif choice == 4:
            if not data["classes"]:
                print("No classes added.")
            for name, info in data["classes"].items():
                req = info.get("subject_requirements", {})
                print(f"- {name}: {info.get('periods_per_day', periods())} periods/day")
                if req:
                    print("  " + ", ".join(f"{s}={n}" for s, n in req.items()))
            pause()

        else:
            return


# ----------------------------- TEACHERS ----------------------------------

def manage_teachers():
    while True:
        clear_screen()
        print("=== MANAGE TEACHERS ===")
        print("1. Add teacher")
        print("2. Edit teacher")
        print("3. Remove teacher")
        print("4. View teachers")
        print("5. Set teacher availability")
        print("6. Back")
        choice = ask_int("Choose: ", 1, 6)

        if choice == 1:
            name = ask("Teacher name: ")
            if not name:
                continue
            if name in data["teachers"]:
                print("Teacher already exists.")
                pause()
                continue

            raw = ask("Subjects they can teach (comma-separated): ")
            subjects = [s.strip() for s in raw.split(",") if s.strip()]
            data["teachers"][name] = {
                "subjects": subjects,
                "availability": {d: [True] * periods() for d in DAYS},
                "substitute_count": 0,
            }
            print(f"Teacher {name} added.")
            pause()

        elif choice == 2:
            names = list(data["teachers"])
            if not names:
                print("No teachers yet.")
                pause()
                continue
            for i, n in enumerate(names, 1):
                print(f"{i}. {n}")
            old = names[ask_int("Select teacher: ", 1, len(names)) - 1]
            raw = ask("Subjects they can teach (blank = unchanged): ")
            if raw:
                data["teachers"][old]["subjects"] = [
                    s.strip() for s in raw.split(",") if s.strip()
                ]
            new = ask(f"New name [{old}]: ", old)
            if new != old:
                data["teachers"][new] = data["teachers"].pop(old)
            print("Updated.")
            pause()

        elif choice == 3:
            names = list(data["teachers"])
            if not names:
                print("No teachers yet.")
                pause()
                continue
            for i, n in enumerate(names, 1):
                print(f"{i}. {n}")
            t = names[ask_int("Select teacher: ", 1, len(names)) - 1]
            if yes_no(f"Remove {t}?", False):
                del data["teachers"][t]
                print("Removed.")
            pause()

        elif choice == 4:
            if not data["teachers"]:
                print("No teachers added.")
            for name, info in data["teachers"].items():
                print(f"- {name}: {', '.join(info.get('subjects', []))}")
            pause()

        elif choice == 5:
            set_availability()

        else:
            return


def set_availability():
    names = list(data["teachers"])
    if not names:
        print("Add teachers first.")
        pause()
        return

    for i, n in enumerate(names, 1):
        print(f"{i}. {n}")
    teacher = names[ask_int("Select teacher: ", 1, len(names)) - 1]

    print("Enter unavailable slots. Leave Day blank to finish.")
    while True:
        day = input("Day: ").strip().title()
        if not day:
            break
        if day not in DAYS:
            print("Use Monday-Saturday.")
            continue
        p = ask_int(f"Period (1-{periods()}): ", 1, periods())
        data["teachers"][teacher]["availability"][day][p - 1] = False
        print(f"{teacher}: unavailable on {day} P{p}.")
    pause()


# ----------------------------- SUBJECTS ----------------------------------

def manage_subjects():
    while True:
        clear_screen()
        print("=== SUBJECTS & CLASS REQUIREMENTS ===")
        print("1. Add subject")
        print("2. Remove subject")
        print("3. Set weekly requirement for a class")
        print("4. View subjects")
        print("5. View requirements")
        print("6. Back")
        choice = ask_int("Choose: ", 1, 6)

        if choice == 1:
            subject = ask("Subject name: ")
            if subject:
                data["subjects"].setdefault(subject, {"teachers": []})
                print("Subject added.")
            pause()

        elif choice == 2:
            subjects = list(data["subjects"])
            if not subjects:
                print("No subjects.")
                pause()
                continue
            for i, s in enumerate(subjects, 1):
                print(f"{i}. {s}")
            s = subjects[ask_int("Select: ", 1, len(subjects)) - 1]
            if yes_no(f"Remove {s}?", False):
                del data["subjects"][s]
            pause()

        elif choice == 3:
            set_requirement()

        elif choice == 4:
            if not data["subjects"]:
                print("No subjects.")
            for s in data["subjects"]:
                teachers = data["subjects"][s].get("teachers", [])
                print(f"- {s}: {', '.join(teachers) or 'teacher assignment from teacher data'}")
            pause()

        elif choice == 5:
            for cls, info in data["classes"].items():
                print(f"\n{cls}:")
                req = info.get("subject_requirements", {})
                print("  " + (", ".join(f"{s}={n}" for s, n in req.items()) or "No requirements"))
            pause()

        else:
            return


def set_requirement():
    if not data["classes"] or not data["subjects"]:
        print("Add classes and subjects first.")
        pause()
        return

    classes = list(data["classes"])
    for i, c in enumerate(classes, 1):
        print(f"{i}. {c}")
    cls = classes[ask_int("Select class: ", 1, len(classes)) - 1]

    subjects = list(data["subjects"])
    for i, s in enumerate(subjects, 1):
        print(f"{i}. {s}")
    subject = subjects[ask_int("Select subject: ", 1, len(subjects)) - 1]

    count = ask_int(
        f"Weekly periods for {subject} in {cls} (0-{len(DAYS)*periods()}): ",
        0, len(DAYS) * periods()
    )
    data["classes"][cls].setdefault("subject_requirements", {})[subject] = count
    print(f"Saved: {cls} -> {subject}: {count} periods/week.")
    pause()


# -------------------------- FIXED ACTIVITIES ------------------------------

def manage_fixed_activities():
    while True:
        clear_screen()
        print("=== FIXED ACTIVITIES ===")
        print("1. Add")
        print("2. Remove")
        print("3. View")
        print("4. Back")
        choice = ask_int("Choose: ", 1, 4)

        if choice == 1:
            classes = list(data["classes"])
            if not classes:
                print("Add a class first.")
                pause()
                continue
            for i, c in enumerate(classes, 1):
                print(f"{i}. {c}")
            cls = classes[ask_int("Class: ", 1, len(classes)) - 1]

            day = ask("Day: ").title()
            if day not in DAYS:
                print("Invalid day.")
                pause()
                continue
            p = ask_int(f"Period (1-{periods()}): ", 1, periods())
            activity = ask("Activity (Sports/Club/Library/Performing Arts/etc.): ")
            if activity:
                data["fixed_activities"][f"{cls}|{day}|{p}"] = activity
            pause()

        elif choice == 2:
            keys = list(data["fixed_activities"])
            if not keys:
                print("No fixed activities.")
                pause()
                continue
            for i, k in enumerate(keys, 1):
                print(f"{i}. {k} -> {data['fixed_activities'][k]}")
            k = keys[ask_int("Select: ", 1, len(keys)) - 1]
            del data["fixed_activities"][k]
            pause()

        elif choice == 3:
            if not data["fixed_activities"]:
                print("No fixed activities.")
            for k, v in data["fixed_activities"].items():
                print(f"- {k}: {v}")
            pause()

        else:
            return


# --------------------------- TIMETABLE ENGINE ----------------------------

def teacher_subjects(teacher):
    return data["teachers"].get(teacher, {}).get("subjects", [])


def qualified_teachers(subject):
    return [
        name for name in data["teachers"]
        if subject in teacher_subjects(name)
    ]


def teacher_available(teacher, day, p):
    values = data["teachers"].get(teacher, {}).get(
        "availability", {}
    ).get(day, [True] * periods())
    return p <= len(values) and values[p - 1]


def teacher_busy(timetable, teacher, day, p):
    slot = str(p)
    for class_days in timetable.values():
        entry = class_days.get(day, {}).get(slot)
        if entry and entry.get("teacher") == teacher:
            return True
    return False


def fixed_activity(cls, day, p):
    return data["fixed_activities"].get(f"{cls}|{day}|{p}")


def generate_timetable(verbose=True):
    if not data["classes"] or not data["subjects"] or not data["teachers"]:
        print("Add classes, subjects and teachers first.")
        return False

    total_slots = len(DAYS) * periods()
    timetable = {
        cls: {day: {} for day in DAYS}
        for cls in data["classes"]
    }

    requirements = {}
    for cls, info in data["classes"].items():
        req = info.get("subject_requirements", {})
        total = sum(int(v) for v in req.values())
        if total > total_slots:
            print(f"{cls} needs {total} lessons but has only {total_slots} slots.")
            return False
        requirements[cls] = []
        for subject, count in req.items():
            if subject in data["subjects"]:
                requirements[cls].extend([subject] * int(count))

    # Fixed activities first.
    for cls in timetable:
        for day in DAYS:
            for p in range(1, periods() + 1):
                activity = fixed_activity(cls, day, p)
                if activity:
                    timetable[cls][day][str(p)] = {
                        "type": "activity",
                        "subject": activity,
                        "teacher": "",
                    }

    # Most constrained classes/subjects first.
    class_order = sorted(
        data["classes"],
        key=lambda c: len(requirements[c]),
        reverse=True
    )

    for cls in class_order:
        subjects = sorted(
            requirements[cls],
            key=lambda s: len(qualified_teachers(s))
        )

        for subject in subjects:
            options = []

            for day_index, day in enumerate(DAYS):
                for p in range(1, periods() + 1):
                    if str(p) in timetable[cls][day]:
                        continue

                    for teacher in qualified_teachers(subject):
                        if not teacher_available(teacher, day, p):
                            continue
                        if teacher_busy(timetable, teacher, day, p):
                            continue

                        same_subject_same_day = sum(
                            1 for entry in timetable[cls][day].values()
                            if entry.get("subject") == subject
                        )

                        score = same_subject_same_day * 20 + day_index
                        options.append((score, day, p, teacher))

            if options:
                options.sort(key=lambda x: x[0])
                _, day, p, teacher = options[0]
                timetable[cls][day][str(p)] = {
                    "type": "lesson",
                    "subject": subject,
                    "teacher": teacher,
                }
            else:
                print(f"WARNING: Could not place {subject} for {cls}.")

    data["timetable"] = timetable
    if verbose:
        print("\nTimetable generated successfully.")
    return True


def print_timetable(cls):
    if cls not in data["timetable"]:
        print("No timetable for this class.")
        return

    w_day = 12
    w = 19
    pcount = periods()
    line = "+" + "-" * w_day + "+" + "+".join("-" * w for _ in range(pcount)) + "+"

    print(f"\nTIMETABLE — {cls}")
    print(line)
    print("|" + f"{'Day':^{w_day}}" + "|" +
          "|".join(f"{'P'+str(p):^{w}}" for p in range(1, pcount + 1)) + "|")
    print(line)

    for day in DAYS:
        row = []
        for p in range(1, pcount + 1):
            entry = data["timetable"][cls].get(day, {}).get(str(p))
            if not entry:
                text = "FREE"
            elif entry.get("type") == "activity":
                text = entry.get("subject", "Activity")
            else:
                text = f"{entry.get('subject', '?')}\n{entry.get('teacher', '')}"
            row.append(text)

        print("|" + f"{day:^{w_day}}" + "|" +
              "|".join(f"{x:^{w}}" for x in row) + "|")
        print(line)


def view_timetable():
    classes = list(data["classes"])
    if not classes:
        print("No classes.")
        pause()
        return
    for i, c in enumerate(classes, 1):
        print(f"{i}. {c}")
    cls = classes[ask_int("Select class: ", 1, len(classes)) - 1]
    print_timetable(cls)
    pause()


def validate_timetable():
    clashes = []
    occupied = defaultdict(list)

    for cls, days in data["timetable"].items():
        for day, slots in days.items():
            for p, entry in slots.items():
                teacher = entry.get("teacher")
                if teacher:
                    occupied[(day, p, teacher)].append(cls)

    for (day, p, teacher), classes in occupied.items():
        if len(classes) > 1:
            clashes.append(
                f"{teacher} teaches {', '.join(classes)} simultaneously on {day} P{p}."
            )

    for cls, days in data["timetable"].items():
        for day, slots in days.items():
            for p, entry in slots.items():
                teacher = entry.get("teacher")
                if teacher and not teacher_available(teacher, day, int(p)):
                    clashes.append(f"{teacher} is unavailable on {day} P{p}.")

    if clashes:
        print("\nVALIDATION: PROBLEMS FOUND")
        for item in clashes:
            print("-", item)
        return False

    print("\nVALIDATION: PASSED")
    print("No teacher clashes or availability conflicts detected.")
    return True


# --------------------------- SUBSTITUTE SOS ------------------------------

def affected_classes(teacher, day, p):
    result = []
    for cls, days in data["timetable"].items():
        entry = days.get(day, {}).get(str(p))
        if entry and entry.get("teacher") == teacher:
            result.append((cls, entry))
    return result


def substitute_candidates(absent_teacher, subject, day, p):
    candidates = []

    for teacher, info in data["teachers"].items():
        if teacher == absent_teacher:
            continue
        if subject not in info.get("subjects", []):
            continue
        if not teacher_available(teacher, day, p):
            continue
        if teacher_busy(data["timetable"], teacher, day, p):
            continue

        score = info.get("substitute_count", 0) * 10
        if teacher in data["subjects"].get(subject, {}).get("teachers", []):
            score -= 5
        candidates.append((score, teacher))

    return sorted(candidates, key=lambda x: (x[0], x[1]))


def mark_absence():
    teachers = list(data["teachers"])
    if not teachers:
        print("No teachers.")
        pause()
        return

    for i, t in enumerate(teachers, 1):
        print(f"{i}. {t}")
    teacher = teachers[ask_int("Absent teacher: ", 1, len(teachers)) - 1]

    day = ask("Day: ").title()
    if day not in DAYS:
        print("Invalid day.")
        pause()
        return

    p = ask_int(f"Period (1-{periods()}): ", 1, periods())
    reason = ask("Reason [Absent]: ", "Absent")
    data["absences"][f"{teacher}|{day}|{p}"] = reason

    print(f"{teacher} marked absent on {day} P{p}.")
    pause()


def find_and_assign_substitute():
    if not data["absences"]:
        print("No absences recorded.")
        pause()
        return

    keys = list(data["absences"])
    for i, k in enumerate(keys, 1):
        print(f"{i}. {k} -> {data['absences'][k]}")
    selected = keys[ask_int("Select absence: ", 1, len(keys)) - 1]

    absent_teacher, day, p = selected.split("|")
    p = int(p)

    affected = affected_classes(absent_teacher, day, p)
    if not affected:
        print("No class is currently assigned to that teacher at this time.")
        pause()
        return

    for cls, entry in affected:
        subject = entry.get("subject", "")
        candidates = substitute_candidates(absent_teacher, subject, day, p)

        print(f"\nAffected class: {cls}")
        print(f"Subject: {subject}")

        if not candidates:
            print("No suitable substitute is available.")
            continue

        print("Suitable candidates:")
        for i, (_, teacher) in enumerate(candidates[:5], 1):
            load = data["teachers"][teacher].get("substitute_count", 0)
            print(f"{i}. {teacher}  (substitute load: {load})")

        count = min(5, len(candidates))
        idx = ask_int(f"Choose substitute (1-{count}): ", 1, count)
        substitute = candidates[idx - 1][1]

        entry["substitute_for"] = absent_teacher
        entry["substitute_teacher"] = substitute
        data["substitutions"][f"{cls}|{day}|{p}"] = substitute
        data["teachers"][substitute]["substitute_count"] += 1

        print(f"Assigned {substitute} to {cls} for {subject} on {day} P{p}.")

    pause()


def view_updated_timetable():
    classes = list(data["classes"])
    if not classes:
        print("No classes.")
        pause()
        return

    for i, c in enumerate(classes, 1):
        print(f"{i}. {c}")
    cls = classes[ask_int("Select class: ", 1, len(classes)) - 1]

    pcount = periods()
    w_day, w = 12, 21
    line = "+" + "-" * w_day + "+" + "+".join("-" * w for _ in range(pcount)) + "+"

    print(f"\nUPDATED TIMETABLE — {cls}")
    print(line)
    print("|" + f"{'Day':^{w_day}}" + "|" +
          "|".join(f"{'P'+str(p):^{w}}" for p in range(1, pcount + 1)) + "|")
    print(line)

    for day in DAYS:
        row = []
        for p in range(1, pcount + 1):
            entry = data["timetable"][cls].get(day, {}).get(str(p))
            if not entry:
                text = "FREE"
            elif entry.get("type") == "activity":
                text = entry.get("subject", "Activity")
            else:
                subject = entry.get("subject", "?")
                sub = entry.get("substitute_teacher")
                text = f"{subject}\nSUB: {sub}" if sub else f"{subject}\n{entry.get('teacher', '')}"
            row.append(text)

        print("|" + f"{day:^{w_day}}" + "|" +
              "|".join(f"{x:^{w}}" for x in row) + "|")
        print(line)

    pause()


def substitute_sos():
    while True:
        clear_screen()
        print("=== SUBSTITUTE SOS ===")
        print("1. Mark teacher absent")
        print("2. Find / assign substitute")
        print("3. View updated timetable")
        print("4. View absences")
        print("5. Back")
        choice = ask_int("Choose: ", 1, 5)

        if choice == 1:
            mark_absence()
        elif choice == 2:
            find_and_assign_substitute()
        elif choice == 3:
            view_updated_timetable()
        elif choice == 4:
            if not data["absences"]:
                print("No absences.")
            else:
                for k, reason in data["absences"].items():
                    print(f"- {k}: {reason}")
            pause()
        else:
            return


# ----------------------------- MODULE A ----------------------------------

def timetable_module():
    while True:
        clear_screen()
        print("=== MODULE A — DYNAMIC TIMETABLE ===")
        print("1. Manage Classes")
        print("2. Manage Teachers")
        print("3. Manage Subjects & Requirements")
        print("4. Fixed Activities")
        print("5. Generate / Regenerate Timetable")
        print("6. View Class Timetable")
        print("7. Validate Timetable")
        print("8. Back")
        choice = ask_int("Choose: ", 1, 8)

        if choice == 1:
            manage_classes()
        elif choice == 2:
            manage_teachers()
        elif choice == 3:
            manage_subjects()
        elif choice == 4:
            manage_fixed_activities()
        elif choice == 5:
            generate_timetable()
            pause()
        elif choice == 6:
            view_timetable()
        elif choice == 7:
            validate_timetable()
            pause()
        else:
            return


# -------------------------- HACKATHON DEMO -------------------------------

def create_demo_data():
    global data

    data = {
        "settings": {"periods_per_day": 8, "school_days": DAYS[:]},
        "classes": {
            "9A": {
                "periods_per_day": 8,
                "subject_requirements": {
                    "Mathematics": 7,
                    "Physics": 6,
                    "Chemistry": 6,
                    "English": 6,
                    "Computer": 5,
                    "Sanskrit": 4,
                    "Sports": 2,
                },
            }
        },
        "teachers": {
            "Sharma": {
                "subjects": ["Mathematics","Sanskrit"],
                "availability": {d: [True] * 8 for d in DAYS},
                "substitute_count": 0,
            },
            "Verma": {
                "subjects": ["Physics"],
                "availability": {d: [True] * 8 for d in DAYS},
                "substitute_count": 0,
            },
            "Singh": {
                "subjects": ["Chemistry","Computer"],
                "availability": {d: [True] * 8 for d in DAYS},
                "substitute_count": 0,
            },
            "Gupta": {
                "subjects": ["English","Sports"],
                "availability": {d: [True] * 8 for d in DAYS},
                "substitute_count": 0,
            },
            "Mehta": {
                "subjects": ["Computer","English"],
                "availability": {d: [True] * 8 for d in DAYS},
                "substitute_count": 0,
            },
            "Khan": {
                "subjects": ["Sanskrit","Chemistry"],
                "availability": {d: [True] * 8 for d in DAYS},
                "substitute_count": 0,
            },
            "Patel": {
                "subjects": ["Physics", "Sports","Mathematics"],
                "availability": {d: [True] * 8 for d in DAYS},
                "substitute_count": 0,
            },
        },
        "subjects": {
            "Mathematics": {"teachers": ["Sharma","Patel"]},
            "Physics": {"teachers": ["Verma", "Patel"]},
            "Chemistry": {"teachers": ["Singh","Khan"]},
            "English": {"teachers": ["Gupta","Mehta"]},
            "Computer": {"teachers": ["Mehta","Singh"]},
            "Sanskrit": {"teachers": ["Khan","Sharma"]},
            "Sports": {"teachers": ["Patel","Gupta"]},
        },
        "fixed_activities": {
            "9A|Saturday|1": "Sports",
            "9A|Wednesday|8": "Club",
            "9A|Friday|8": "Library",
        },
        "timetable": {},
        "absences": {},
        "substitutions": {},
    }


def live_hackathon_demo():
    create_demo_data()

    print("\n=== LIVE HACKATHON DEMO ===")
    print("Generating timetable from school requirements...")
    generate_timetable(verbose=False)
    print_timetable("9A")

    # Find an actual Verma Physics period.
    target = None
    for day in DAYS:
        for p in range(1, 9):
            entry = data["timetable"]["9A"][day].get(str(p))
            if entry and entry.get("teacher") == "Verma":
                target = (day, p)
                break
        if target:
            break

    if not target:
        print("Could not find a Physics period taught by Verma.")
        return

    day, p = target
    data["absences"][f"Verma|{day}|{p}"] = "Sudden absence"

    print("\n--- TEACHER ABSENCE ---")
    print(f"Verma is absent on {day}, Period {p}.")
    print("Searching for a qualified, available substitute...")

    affected = affected_classes("Verma", day, p)
    for cls, entry in affected:
        subject = entry["subject"]
        candidates = substitute_candidates("Verma", subject, day, p)

        if candidates:
            substitute = candidates[0][1]
            entry["substitute_for"] = "Verma"
            entry["substitute_teacher"] = substitute
            data["substitutions"][f"{cls}|{day}|{p}"] = substitute
            data["teachers"][substitute]["substitute_count"] += 1
            print(f"Recommended substitute: {substitute}")
            print(f"{cls} / {subject} / {day} P{p}")
        else:
            print("No suitable substitute available.")

    print("\n--- UPDATED TIMETABLE ---")
    print_timetable("9A")


# ------------------------------- MAIN ------------------------------------

def main():
    load_data()

    while True:
        clear_screen()
        print("=" * 66)
        print("        SubstituteSOS")
        print("Smart Dynamic Timetable & Substitute Management System")
        print("=" * 66)
        print("1. Module A - Timetable Management")
        print("2. Module B - Substitute SOS")
        print("3. Save Data")
        print("4. Validate Generated Timetable")
        print("5. Run Live Hackathon Demo")
        print("6. Exit")
        print("=" * 66)

        choice = ask_int("Choose an option: ", 1, 6)

        if choice == 1:
            timetable_module()
        elif choice == 2:
            substitute_sos()
        elif choice == 3:
            print("Saved." if save_data() else "Save failed.")
            pause()
        elif choice == 4:
            validate_timetable()
            pause()
        elif choice == 5:
            live_hackathon_demo()
            pause()
        else:
            save_data()
            print("Good luck with your hackathon! 🚀")
            break


if __name__ == "__main__":
    main()

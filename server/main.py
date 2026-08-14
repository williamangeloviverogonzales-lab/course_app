import csv
import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from sqlalchemy import text  # <-- ADDED for the migration
from pydantic import BaseModel

from server.database import init_db, get_session, engine
from server.models import Student, Subject, Section, Topic, Enrollment, LessonProgress

app = FastAPI(title="Academic Course Portal API")

# Mount static asset folders
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/lessons", StaticFiles(directory="lessons"), name="lessons")

@app.on_event("startup")
def on_startup():
    init_db()
    migrate_db_schema()  # <-- ADDED to run the migration check on startup
    seed_default_courses()
    sync_all_subject_rosters("lessons")

def migrate_db_schema():
    """Safely alter existing SQLite tables to add new columns if they don't exist yet."""
    with Session(engine) as session:
        try:
            # Check if student table has last_login column; if not, add it!
            session.exec(text("ALTER TABLE student ADD COLUMN last_login DATETIME;"))
            session.commit()
            print("[MIGRATION] Added missing 'last_login' column to 'student' table.")
        except Exception:
            # Column already exists, so ignore the exception safely
            session.rollback()

def seed_default_courses():
    """Ensure Subjects and Topics exist and update file paths in DB on restart."""
    with Session(engine) as session:
        # --- 1. PROBABILITY (MATH302) ---
        prob_subject = session.exec(select(Subject).where(Subject.subject_code == "MATH302")).first()
        if not prob_subject:
            prob_subject = Subject(subject_code="MATH302", title="Probability", description="College Level Probability")
            session.add(prob_subject)
            session.commit()

        prob_topics = [
            ("Topic 1: Sample Spaces & Axioms of Probability", "published", "lessons/MATH302/topic-01-sample-spaces.html"),
            ("Topic 2: Counting Rules, Permutations & Combinations", "published", "lessons/MATH302/topic-02-counting-rules.html"),
            ("Topic 3: Conditional Probability & Bayes' Theorem", "locked", "lessons/MATH302/topic-03-conditional-prob.html"),
            ("Topic 4: Discrete Random Variables & Expected Value", "locked", None),
            ("Topic 5: Common Discrete Distributions (Binomial, Poisson)", "locked", None),
            ("Topic 6: Continuous Random Variables & PDFs", "locked", None),
            ("Topic 7: The Normal Distribution & Limit Theorems", "locked", None),
        ]

        for idx, (title, status_flag, file_path) in enumerate(prob_topics, start=1):
            existing_topic = session.exec(
                select(Topic).where(Topic.subject_code == "MATH302", Topic.topic_number == idx)
            ).first()

            if existing_topic:
                existing_topic.topic_title = title
                existing_topic.status = status_flag
                existing_topic.lesson_file_path = file_path
                session.add(existing_topic)
            else:
                topic = Topic(
                    subject_code="MATH302",
                    topic_number=idx,
                    topic_title=title,
                    status=status_flag,
                    lesson_file_path=file_path
                )
                session.add(topic)

        # --- 2. STATISTICS (STAT101) ---
        stat_subject = session.exec(select(Subject).where(Subject.subject_code == "STAT101")).first()
        if not stat_subject:
            stat_subject = Subject(subject_code="STAT101", title="Applied Statistics", description="Introductory Statistics & Data Analysis")
            session.add(stat_subject)
            session.commit()

        stat_topics = [
            ("Topic 1: Measures of Central Tendency", "published", "lessons/STAT101/topic-01-descriptive-stats.html"),
            ("Topic 2: Measures of Dispersion & Variance", "published", "lessons/STAT101/topic-02-dispersion.html"),
            ("Topic 3: Z-Scores & The Normal Distribution", "locked", "lessons/STAT101/topic-03-zscores.html"),
            ("Topic 4: Sampling Distributions & Central Limit Theorem", "locked", None),
            ("Topic 5: Confidence Intervals for Means & Proportions", "locked", None),
            ("Topic 6: Hypothesis Testing (One-Sample & Two-Sample)", "locked", None),
            ("Topic 7: Simple Linear Regression & Correlation", "locked", None),
        ]

        for idx, (title, status_flag, file_path) in enumerate(stat_topics, start=1):
            existing_topic = session.exec(
                select(Topic).where(Topic.subject_code == "STAT101", Topic.topic_number == idx)
            ).first()

            if existing_topic:
                existing_topic.topic_title = title
                existing_topic.status = status_flag
                existing_topic.lesson_file_path = file_path
                session.add(existing_topic)
            else:
                topic = Topic(
                    subject_code="STAT101",
                    topic_number=idx,
                    topic_title=title,
                    status=status_flag,
                    lesson_file_path=file_path
                )
                session.add(topic)

        # --- 3. MATHEMATICAL ECONOMICS (RC4) ---
        rc4_subject = session.exec(select(Subject).where(Subject.subject_code == "RC4")).first()
        if not rc4_subject:
            rc4_subject = Subject(
                subject_code="RC4", 
                title="Mathematical Economics", 
                description="Mathematical Methods & Models in Economics"
            )
            session.add(rc4_subject)
            session.commit()

        rc4_topics = [
            ("Topic 1: Nature of Mathematical Economics", "published", "lessons/RC4/topic-01-nature-of-mathematical-economics.html"),
            ("Topic 2: Sets, Real Numbers, Relations & Functions", "published", "lessons/RC4/topic-02-foundations-and-functions.html"),
            ("Topic 3: Comparative Static Analysis & Derivatives", "locked", None),
            ("Topic 4: Optimization & Unconstrained Problems", "locked", None),
            ("Topic 5: Constrained Optimization & Lagrange Multipliers", "locked", None),
        ]

        for idx, (title, status_flag, file_path) in enumerate(rc4_topics, start=1):
            existing_topic = session.exec(
                select(Topic).where(Topic.subject_code == "RC4", Topic.topic_number == idx)
            ).first()

            if existing_topic:
                existing_topic.topic_title = title
                existing_topic.status = status_flag
                existing_topic.lesson_file_path = file_path
                session.add(existing_topic)
            else:
                topic = Topic(
                    subject_code="RC4",
                    topic_number=idx,
                    topic_title=title,
                    status=status_flag,
                    lesson_file_path=file_path
                )
                session.add(topic)

        # --- 4. PHYSICS FOR INDUSTRIAL TECHNOLOGISTS (BIT04) ---
        bit04_subject = session.exec(select(Subject).where(Subject.subject_code == "BIT04")).first()
        if not bit04_subject:
            bit04_subject = Subject(
                subject_code="BIT04", 
                title="Physics for Industrial Technologists", 
                description="Applied Physics Principles for Industrial Technology"
            )
            session.add(bit04_subject)
            session.commit()

        bit04_topics = [
            ("Topic 1: Units & Physical Quantities", "published", "lessons/BIT04/topic-01-units.html"),
            ("Topic 2: Vectors", "published", "lessons/BIT04/topic-02-vectors.html"),
            ("Topic 3: Kinematics", "locked", None),
            ("Topic 4: Electricity & Magnetism", "locked", None),
        ]

        for idx, (title, status_flag, file_path) in enumerate(bit04_topics, start=1):
            existing_topic = session.exec(
                select(Topic).where(Topic.subject_code == "BIT04", Topic.topic_number == idx)
            ).first()

            if existing_topic:
                existing_topic.topic_title = title
                existing_topic.status = status_flag
                existing_topic.lesson_file_path = file_path
                session.add(existing_topic)
            else:
                topic = Topic(
                    subject_code="BIT04",
                    topic_number=idx,
                    topic_title=title,
                    status=status_flag,
                    lesson_file_path=file_path
                )
                session.add(topic)

        # --- 5. MATHEMATICS IN THE MODERN WORLD (GEC4) ---
        gec4_subject = session.exec(select(Subject).where(Subject.subject_code == "GEC4")).first()
        if not gec4_subject:
            gec4_subject = Subject(
                subject_code="GEC4", 
                title="Mathematics in the Modern World", 
                description="Nature of Mathematics, Patterns, & Practical Applications"
            )
            session.add(gec4_subject)
            session.commit()

        gec4_topics = [
            ("Topic 1: Mathematics and Nature", "published", "lessons/GEC4/topic-01-patterns.html"),
            ("Topic 2: Fibonacci Sequence", "published", "lessons/GEC4/topic-02-fibonacci.html"),
            ("Topic 3: Mathematical Language & Symbols", "locked", None),
            ("Topic 4: Problem Solving & Reasoning Strategies", "locked", None),
            ("Topic 5: Mathematics of Finance", "locked", None),
        ]

        for idx, (title, status_flag, file_path) in enumerate(gec4_topics, start=1):
            existing_topic = session.exec(
                select(Topic).where(Topic.subject_code == "GEC4", Topic.topic_number == idx)
            ).first()

            if existing_topic:
                existing_topic.topic_title = title
                existing_topic.status = status_flag
                existing_topic.lesson_file_path = file_path
                session.add(existing_topic)
            else:
                topic = Topic(
                    subject_code="GEC4",
                    topic_number=idx,
                    topic_title=title,
                    status=status_flag,
                    lesson_file_path=file_path
                )
                session.add(topic)

        session.commit()

def sync_all_subject_rosters(lessons_dir: str):
    """Dynamically scan each subject subfolder in lessons/ for a roster.csv file."""
    if not os.path.exists(lessons_dir):
        return

    with Session(engine) as session:
        for subject_code in os.listdir(lessons_dir):
            subject_folder = os.path.join(lessons_dir, subject_code)
            
            if os.path.isdir(subject_folder):
                roster_path = os.path.join(subject_folder, "roster.csv")
                
                if os.path.exists(roster_path):
                    process_subject_csv(session, subject_code, roster_path)

        session.commit()

def process_subject_csv(session: Session, subject_code: str, csv_path: str):
    """Read student roster from a subject's roster.csv and enroll them in SQLModel DB."""
    # Ensure subject exists before attempting section creation
    subject = session.exec(select(Subject).where(Subject.subject_code == subject_code)).first()
    if not subject:
        return

    sec_id = f"SEC_{subject_code}_DEFAULT"
    
    section = session.exec(select(Section).where(Section.section_id == sec_id)).first()
    if not section:
        section = Section(
            section_id=sec_id, 
            subject_code=subject_code, 
            section_name=f"{subject_code} Section A", 
            term="1st Sem 2026"
        )
        session.add(section)
        session.commit()

    with open(csv_path, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            s_id = row.get("Student ID", "").strip()
            if not s_id:
                continue

            first = row.get("First Name", "").strip()
            middle = row.get("Middle Name", "").strip()
            last = row.get("Last Name", "").strip()
            ext = row.get("Name Ext.", "").strip()

            name_parts = [first, middle, last, ext]
            full_name = " ".join([p for p in name_parts if p])

            email = row.get("Email", "").strip() or f"{s_id}@school.edu"

            student = session.exec(select(Student).where(Student.student_id == s_id)).first()
            if not student:
                student = Student(student_id=s_id, name=full_name, email=email)
                session.add(student)
                session.commit()

            enrollment = session.exec(select(Enrollment).where(
                Enrollment.student_id == s_id,
                Enrollment.section_id == sec_id
            )).first()
            if not enrollment:
                enrollment = Enrollment(student_id=s_id, section_id=sec_id)
                session.add(enrollment)

# --- REQUEST SCHEMAS ---

class AuthRequest(BaseModel):
    student_id: str
    subject_code: str

class ProgressUpdate(BaseModel):
    student_id: str
    subject_code: str
    topic_number: int
    progress_percent: int
    completed: bool = False

# --- ROUTES ---

@app.get("/")
def serve_portal():
    """Serve the main Portal Shell."""
    return FileResponse("static/index.html")

@app.get("/admin")
def serve_admin_dashboard():
    """Serve the Teacher Analytics Dashboard."""
    return FileResponse("static/admin.html")

@app.post("/api/verify-access")
def verify_student_access(auth: AuthRequest, session: Session = Depends(get_session)):
    """Check if the given student ID is present in the chosen subject's roster."""
    student = session.exec(select(Student).where(Student.student_id == auth.student_id.strip())).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student ID not found in system roster.")

    is_enrolled = any(sec.subject_code == auth.subject_code for sec in student.sections)
    if not is_enrolled:
        raise HTTPException(status_code=403, detail=f"Access Denied: You are not enrolled in {auth.subject_code}.")

    # Log access timestamp to database and console
    student.last_login = datetime.utcnow()
    session.add(student)
    session.commit()

    print(f"[ACCESS LOG] Student {student.name} ({student.student_id}) accessed {auth.subject_code}")

    return {
        "status": "success",
        "student_name": student.name,
        "subject_code": auth.subject_code
    }

@app.get("/api/subjects/{subject_code}/topics")
def get_subject_topics(subject_code: str, session: Session = Depends(get_session)):
    """Fetch topic syllabus for a subject ordered by topic number."""
    topics = session.exec(
        select(Topic)
        .where(Topic.subject_code == subject_code)
        .order_by(Topic.topic_number)
    ).all()
    return topics

@app.post("/api/progress/update")
def update_lesson_progress(data: ProgressUpdate, session: Session = Depends(get_session)):
    """Record or update a student's progress for a specific lesson topic."""
    prog = session.exec(select(LessonProgress).where(
        LessonProgress.student_id == data.student_id,
        LessonProgress.subject_code == data.subject_code,
        LessonProgress.topic_number == data.topic_number
    )).first()

    if not prog:
        prog = LessonProgress(
            student_id=data.student_id,
            subject_code=data.subject_code,
            topic_number=data.topic_number
        )

    prog.progress_percent = max(prog.progress_percent, data.progress_percent)
    if data.completed:
        prog.completed = True
    prog.updated_at = datetime.utcnow()

    session.add(prog)
    session.commit()
    return {"status": "success"}

@app.get("/api/admin/dashboard/{subject_code}")
def get_admin_dashboard_data(subject_code: str, session: Session = Depends(get_session)):
    """Fetch student access times and topic completion percentages for the admin dashboard."""
    sec_id = f"SEC_{subject_code}_DEFAULT"
    enrollments = session.exec(select(Enrollment).where(Enrollment.section_id == sec_id)).all()
    topics = session.exec(select(Topic).where(Topic.subject_code == subject_code).order_by(Topic.topic_number)).all()

    student_data = []
    for enr in enrollments:
        student = session.exec(select(Student).where(Student.student_id == enr.student_id)).first()
        if not student:
            continue

        progress_records = session.exec(select(LessonProgress).where(
            LessonProgress.student_id == student.student_id,
            LessonProgress.subject_code == subject_code
        )).all()

        prog_map = {p.topic_number: p.progress_percent for p in progress_records}

        student_data.append({
            "student_id": student.student_id,
            "name": student.name,
            "last_login": student.last_login.strftime("%b %d, %Y %I:%M %p") if student.last_login else "Never",
            "progress": [
                {
                    "topic_number": t.topic_number,
                    "topic_title": t.topic_title,
                    "percent": prog_map.get(t.topic_number, 0)
                }
                for t in topics
            ]
        })

    return {
        "subject_code": subject_code,
        "topics": [{"topic_number": t.topic_number, "topic_title": t.topic_title} for t in topics],
        "students": student_data
    }
import csv
import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from pydantic import BaseModel

from server.database import init_db, get_session, engine
from server.models import Student, Subject, Section, Topic, Enrollment

app = FastAPI(title="Academic Course Portal API")

# Mount static asset folders
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/lessons", StaticFiles(directory="lessons"), name="lessons")

@app.on_event("startup")
def on_startup():
    init_db()
    seed_default_courses()
    sync_all_subject_rosters("lessons")

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
            ("Topic 1: Sample Spaces & Axioms of Probability", "published", "lessons/PROB101/topic-01-sample-spaces.html"),
            ("Topic 2: Counting Rules, Permutations & Combinations", "published", "lessons/PROB101/topic-02-counting-rules.html"),
            ("Topic 3: Conditional Probability & Bayes' Theorem", "locked", "lessons/PROB101/topic-03-conditional-prob.html"),
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
    (
        "Topic 1: Nature of Mathematical Economics", 
        "published", 
        "lessons/RC4/topic-01-nature-of-mathematical-economics.html"
    ),
    (
        "Topic 2: Sets, Real Numbers, Relations & Functions", 
        "published", 
        "lessons/RC4/topic-02-foundations-and-functions.html"
    ),
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

        # --- 4. PHYSICS FOR INDUSTRIAL TECHNOLOGISTS (BIT02) ---
        bit02_subject = session.exec(select(Subject).where(Subject.subject_code == "BIT02")).first()
        if not bit02_subject:
            bit02_subject = Subject(
                subject_code="BIT02", 
                title="Physics for Industrial Technologists", 
                description="Applied Physics Principles for Industrial Technology"
            )
            session.add(bit02_subject)
            session.commit()

        bit02_topics = [
            ("Topic 1: Applied Mechanics & Kinematics", "published", "lessons/BIT02/topic-01-mechanics.html"),
            ("Topic 2: Work, Energy & Power in Industrial Systems", "locked", None),
            ("Topic 3: Thermodynamics & Heat Transfer", "locked", None),
            ("Topic 4: Fluid Mechanics & Pneumatics", "locked", None),
        ]

        for idx, (title, status_flag, file_path) in enumerate(bit02_topics, start=1):
            existing_topic = session.exec(
                select(Topic).where(Topic.subject_code == "BIT02", Topic.topic_number == idx)
            ).first()

            if existing_topic:
                existing_topic.topic_title = title
                existing_topic.status = status_flag
                existing_topic.lesson_file_path = file_path
                session.add(existing_topic)
            else:
                topic = Topic(
                    subject_code="BIT02",
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
            ("Topic 1: Mathematics in Our World & Patterns in Nature", "published", "lessons/GEC4/topic-01-patterns.html"),
            ("Topic 2: Mathematical Language & Symbols", "locked", None),
            ("Topic 3: Problem Solving & Reasoning Strategies", "locked", None),
            ("Topic 4: Mathematics of Finance", "locked", None),
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

# --- ROUTES ---

@app.get("/")
def serve_portal():
    """Serve the main Portal Shell."""
    return FileResponse("static/index.html")

@app.post("/api/verify-access")
def verify_student_access(auth: AuthRequest, session: Session = Depends(get_session)):
    """Check if the given student ID is present in the chosen subject's roster."""
    student = session.exec(select(Student).where(Student.student_id == auth.student_id.strip())).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student ID not found in system roster.")

    is_enrolled = any(sec.subject_code == auth.subject_code for sec in student.sections)
    if not is_enrolled:
        raise HTTPException(status_code=403, detail=f"Access Denied: You are not enrolled in {auth.subject_code}.")

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
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# Junction table: Link Students to specific Class Sections
class Enrollment(SQLModel, table=True):
    student_id: str = Field(foreign_key="student.student_id", primary_key=True)
    section_id: str = Field(foreign_key="section.section_id", primary_key=True)

class Subject(SQLModel, table=True):
    subject_code: str = Field(primary_key=True)  # e.g. MATH302, STAT101
    title: str                                    # e.g. "Probability"
    description: Optional[str] = None

    sections: List["Section"] = Relationship(back_populates="subject")
    topics: List["Topic"] = Relationship(back_populates="subject")

class Section(SQLModel, table=True):
    section_id: str = Field(primary_key=True)    # e.g. SEC_PROB_A_2026
    subject_code: str = Field(foreign_key="subject.subject_code")
    section_name: str                            # e.g. "Probability - Section A (MWF)"
    term: str                                    # e.g. "1st Sem 2026"

    subject: Subject = Relationship(back_populates="sections")
    students: List["Student"] = Relationship(back_populates="sections", link_model=Enrollment)

class Student(SQLModel, table=True):
    student_id: str = Field(primary_key=True)    # e.g. 2024-00101
    name: str
    email: Optional[str] = None
    last_login: Optional[datetime] = Field(default=None)
    sections: List[Section] = Relationship(back_populates="students", link_model=Enrollment)

class LessonProgress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str = Field(foreign_key="student.student_id")
    subject_code: str
    topic_number: int
    progress_percent: int = Field(default=0)
    completed: bool = Field(default=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_code: str = Field(foreign_key="subject.subject_code")
    topic_number: int                            # 1, 2, 3, etc.
    topic_title: str                             # e.g. "Sample Spaces & Set Operations"
    status: str = Field(default="locked")        # published, draft, locked
    lesson_file_path: Optional[str] = None       # e.g. lessons/MATH302/topic-01-sample-spaces.html

    subject: Subject = Relationship(back_populates="topics")

class StudentProgress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str = Field(foreign_key="student.student_id")
    section_id: str = Field(foreign_key="section.section_id")
    topic_number: int
    card_index: int
    completed_at: datetime = Field(default_factory=datetime.utcnow)
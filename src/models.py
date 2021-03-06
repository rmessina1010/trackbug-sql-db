import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

dev_skills = db.Table(
    'dev_skills',
    db.Column(
        'person_id', db.Integer,
        db.ForeignKey('personel.person_id'),
        primary_key=True
    ),
    db.Column(
        'skill_id', db.Integer,
        db.ForeignKey('skills.skill_id'),
        primary_key=True
    )
)


class Personel(db.Model):
    __tablename__ = 'personel'
    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255),  nullable=False)
    last_name = db.Column(db.String(255),  nullable=False)
    p_role = db.Column(db.String(255))
    work_stat = db.Column(db.String(32))
    reports_to = db.Column(db.Integer, db.ForeignKey('personel.person_id'))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(32))
    email = db.Column(db.String(255),  nullable=False)
    password = db.Column(db.String(255),  nullable=False)
    nacl = db.Column(db.String(255),  nullable=False)

    def __init__(self, first_name: str, last_name: str, p_role: str, work_stat: str, reports_to: int, age: int, sex: str, email: str, password: str, nacl: str):
        self.first_name = first_name
        self.last_name = last_name
        self.p_role = p_role
        self.work_stat = work_stat
        self.reports_to = reports_to
        self.age = age
        self.sex = sex
        self.email = email
        self.password = password
        self.nacl = nacl

    def serialize(self):
        return {
            "person_id": self.person_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "p_role": self.p_role,
            "work_stat": self.work_stat,
            "reports_to": self.reports_to,
            "age": self.age,
            "sex": self.sex,
            "email": self.email,
            "password": self.password,
            "nacl": self.nacl
        }

    skilled_in = db.relationship(
        'Skill', secondary=dev_skills,
        lazy='subquery',
        backref=db.backref('dev_skills', lazy=True)
    )


class Project(db.Model):
    __tablename__ = 'projects'
    proj_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proj_title = db.Column(db.String(255),  unique=True, nullable=False)
    proj_status = db.Column(db.String(255))
    proj_excerpt = db.Column(db.Text())
    managed_by = db.Column(db.Integer, db.ForeignKey('personel.person_id'))

    def __init__(self, proj_title: str, proj_status: str, proj_excerpt: str, managed_by: int):
        self.proj_title = proj_title
        self.proj_status = proj_status
        self.proj_excerpt = proj_excerpt
        self.managed_by = managed_by

    def serialize(self):
        return {
            "proj_id": self.proj_id,
            "proj_title": self.proj_title,
            "proj_status": self.proj_status,
            "proj_excerpt": self.proj_excerpt,
            "managed_by": self.managed_by
        }


class Tech(db.Model):
    __tablename__ = "techs"
    tech_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tech_name = db.Column(db.String(255),  unique=True,  nullable=False)

    def __init__(self, tech_name: str):
        self.tech_name = tech_name

    def serialize(self):
        return {
            "tech_id": self.tech_id,
            "tech_name": self.tech_name
        }


class Skill(db.Model):
    __tablename__ = 'skills'
    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column(db.String(255),  unique=True,  nullable=False)
    tech = db.Column(db.Integer, db.ForeignKey('techs.tech_id'))
    lev = db.Column(db.Integer, default=1)

    def __init__(self, skill_name: str, tech: int, lev: int):
        self.skill_name = skill_name
        self.tech = tech
        self.lev = lev

    def serialize(self):
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "tech": self.tech,
            "lev": self.lev
        }


class Report(db.Model):
    __tablename__ = 'reports'
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reported_by = db.Column(db.Integer, db.ForeignKey(
        'personel.person_id'),  nullable=False)
    reported_on = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())
    in_project = db.Column(db.Integer, db.ForeignKey(
        'projects.proj_id'), nullable=False)
    defined_as = db.Column(db.Integer, db.ForeignKey(
        'bugs.bug_id'))

    def __init__(self, reported_by: int, subject: str, description: str, in_project: int):
        self.reported_by = reported_by
        self.subject = subject
        self.description = description
        self.in_project = in_project

    def serialize(self):
        return {
            "report_id": self.report_id,
            "reported_by": self.reported_by,
            "reported_on": self.reported_on,
            "subject": self.subject,
            "description": self.description,
            "in_project": self.in_project,
            "defined_as": self.defined_as
        }


bug_skills = db.Table(
    'bug_skills',
    db.Column(
        'bug_id', db.Integer,
        db.ForeignKey('bugs.bug_id'),
        primary_key=True
    ),
    db.Column(
        'skill_id', db.Integer,
        db.ForeignKey('skills.skill_id'),
        primary_key=True
    )
)


class Bug(db.Model):
    __tablename__ = 'bugs'
    bug_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bug_title = db.Column(db.String(255),  nullable=False)
    bug_status = db.Column(db.String(255))
    bug_summary = db.Column(db.Text(),  nullable=False)
    bug_weight = db.Column(db.Integer)
    in_proj = db.Column(db.Integer,   db.ForeignKey(
        'projects.proj_id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('personel.person_id'))
    defined_on = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, bug_title: str, bug_status: str, bug_summary: str, in_proj: int, assigned_to: int):
        self.bug_title = bug_title
        self.bug_status = bug_status
        self.bug_summary = bug_summary
        self.in_proj = in_proj
        self.assigned_to = assigned_to

    def serialize(self):
        return {
            "bug_id": self.bug_id,
            "bug_title": self.bug_title,
            "bug_status": self.bug_status,
            "bug_summary": self.bug_summary,
            "bug_weight": self.bug_weight,
            "in_proj": self.in_proj,
            "assigned_to": self.assigned_to,
            "defined_on": self.defined_on
        }

    req_skill = db.relationship(
        'Skill', secondary=bug_skills,
        lazy='subquery',
        backref=db.backref('bug_skills', lazy=True)
    )


class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text(),  nullable=False)
    comm_author = db.Column(db.Integer, db.ForeignKey(
        'personel.person_id'),  nullable=False)
    refers_to = db.Column(db.Integer,  db.ForeignKey(
        'bugs.bug_id'), nullable=False)
    comm_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, text: str, comm_author: int, refers_to: int):
        self.text = text
        self.comm_author = comm_author
        self.refers_to = refers_to

    def serialize(self):
        return {
            "comment_id": self.comment_id,
            "text": self.text,
            "comm_author": self.comm_author,
            "refers_to": self.refers_to,
            "comm_date": self.comm_date,
        }

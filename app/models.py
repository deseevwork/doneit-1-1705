from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt, login_manager
from sqlalchemy.types import JSON

# --- Таблица связки задача <-> документ ---
task_documents = db.Table('task_documents',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True)
)

# --- Таблица связки задача <-> тег ---
task_tags = db.Table('task_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# --- Пользователь ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    telegram = db.Column(db.String(100))
    telegram_chat_id = db.Column(db.String(100), nullable=True)
    notifications_enabled = db.Column(db.Boolean, default=True, nullable=False)


    projects = db.relationship('Project', backref='owner', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Проект ---
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete')
    documents = db.relationship('Document', backref='project', lazy=True, cascade='all, delete')
    tags = db.relationship('Tag', backref='project', lazy=True, cascade='all, delete')

# --- Задача ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(10), nullable=False, default='средний')  # низкий, средний, высокий
    status = db.Column(db.String(20), nullable=False, default='в списке')   # в списке, в работе, выполнена
    deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    documents = db.relationship('Document', secondary=task_documents, back_populates='tasks')
    tags = db.relationship('Tag', secondary=task_tags, back_populates='tasks')

# --- Тег ---
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    tasks = db.relationship('Task', secondary=task_tags, back_populates='tags')

# --- Документ ---
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    tasks = db.relationship('Task', secondary=task_documents, back_populates='documents')

# --- Повторяющаяся задача ---
class RepeatingTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    days_of_week = db.Column(JSON)  # список чисел от 0 до 6
    interval = db.Column(db.Integer)  # каждые N дней (если задан)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    checks = db.relationship('RepeatingTaskCheck', backref='task', lazy=True, cascade='all, delete')

# --- Отметка выполнения привычки ---
class RepeatingTaskCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    task_id = db.Column(db.Integer, db.ForeignKey('repeating_task.id'), nullable=False)

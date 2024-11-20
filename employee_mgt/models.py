from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from app import db
from flask_login import UserMixin

# Core Models for Employees, Departments, and Roles (expanded as necessary)
# (Assuming existing models like Employee, Department, Role, etc., from the previous example are available)

bcrypt = Bcrypt()

# Department Model
class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    employees = relationship("Employee", back_populates="department")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


# Employee Model
class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    salary = db.Column(db.Float)
    
    # ForeignKey Relationships
    department_id = db.Column(db.Integer, ForeignKey('departments.id'), nullable=True)
    role_id = db.Column(db.Integer, ForeignKey('roles.id'), nullable=True)
    
    # Relationship Fields
    department = relationship("Department", back_populates="employees")
    role = relationship("Role", back_populates="employees")
    projects = relationship("Project", secondary="project_assignments", back_populates="employees")
    access_permissions = relationship("AccessPermission", back_populates="employee")

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            # 'password': self.password_hash
            # 'date': self.date_joined,
            # 'roles': self.role,
            'admin': self.is_admin,
            'department_id': self.department_id
            # 'password': self.password_hash
        }
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Role Model
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    access_level = db.Column(db.Integer, nullable=False, default=1)
    
    employees = relationship("Employee", back_populates="role")

# Project Model
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    # Many-to-Many relationship with Employee
    employees = relationship("Employee", secondary="project_assignments", back_populates="projects")

# ProjectAssignment Association Table for Many-to-Many Relationship between Employee and Project
class ProjectAssignment(db.Model):
    __tablename__ = 'project_assignments'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, ForeignKey('employees.id'), nullable=False)
    project_id = db.Column(db.Integer, ForeignKey('projects.id'), nullable=False)

# AccessPermission Model to Manage Access Levels and Permissions
class AccessPermission(db.Model):
    __tablename__ = 'access_permissions'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, ForeignKey('employees.id'), nullable=False)
    can_view_personal_data = db.Column(db.Boolean, default=False)
    can_edit_personal_data = db.Column(db.Boolean, default=False)
    can_assign_roles = db.Column(db.Boolean, default=False)

    employee = relationship("Employee", back_populates="access_permissions")
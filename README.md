# 🎓 AcademiaPro - Online Course Management Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

**A comprehensive web-based course management system built with Flask and PostgreSQL**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Database Schema](#-database-schema) • [Screenshots](#-screenshots)

</div>

---

## 📋 About The Project

AcademiaPro is a full-stack web application designed for managing online courses. The platform supports four distinct user roles with specialized functionalities, providing a complete ecosystem for online education management.

### 👥 Development Team - The DB Architects

- **Mayank Seth** - 23CS30032
- **Pratyush Parackal** - 23CS30040
- **Siddharth Konnur** - 23CS30052
- **Y.V.S.Raghu Vardhan** - 23CS30060

---

## ✨ Features

### 🎯 Role-Based Access Control

The system implements **four distinct user roles**, each with specialized dashboards and permissions:

#### 👨‍🎓 Students
- Browse and search available courses
- View detailed course information (instructors, content, topics)
- Enroll in courses with one click
- Access course materials (videos, documents, assignments)
- Track personal performance and grades
- View CGPA and enrollment history

#### 👨‍🏫 Instructors
- Manage assigned courses
- Add course content (videos, PDFs, assignments)
- View enrolled students
- Update and manage student marks
- Track course enrollment statistics
- Access personal teaching dashboard

#### 👨‍💼 System Administrators
- Complete system oversight dashboard
- Create and manage courses
- Assign instructors to courses
- Manage student enrollments
- Add/remove users from the system
- View system-wide statistics
- Monitor recent platform activity

#### 📊 Data Analysts
- Access comprehensive analytics dashboard
- View course enrollment statistics
- Track student performance rankings
- Analyze instructor workload distribution
- Monitor enrollment trends over time
- Identify popular courses
- Generate university-wise reports

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.0+** - Web framework
- **PostgreSQL** - Relational database
- **postgresql-connector-python** - Database driver

### Frontend
- **HTML5 & CSS3** - Structure and styling
- **Bootstrap 5.3** - Responsive UI framework
- **Bootstrap Icons** - Icon library
- **Jinja2** - Template engine

### Architecture
- **3-Tier Architecture**
  - Presentation Layer (HTML/CSS/JS)
  - Application Layer (Flask)
  - Data Layer (PostgreSQL)

---

## 📖 Usage

### For Students

1. **Browse Courses**
   - Navigate to "Browse Courses" from the dashboard
   - Use the search bar to filter courses
   - View detailed information before enrolling

2. **Enroll in Courses**
   - Click "Enroll" on any course card
   - Access course materials immediately after enrollment

3. **Track Progress**
   - View marks and grades in your dashboard
   - Monitor your CGPA

### For Instructors

1. **Manage Your Courses**
   - View all assigned courses in your dashboard
   - Click "Manage Course" to access detailed controls

2. **Add Course Content**
   - Click "Add Content" in course details
   - Provide title, URL, and content type
   - Content immediately available to enrolled students

3. **Grade Students**
   - View enrolled students in course management
   - Click the edit icon next to student names
   - Enter marks (0-100)

### For Administrators

1. **Create New Courses**
   - Navigate to "Manage Courses"
   - Click "Add New Course"
   - Fill in course details and submit

2. **Assign Instructors**
   - Click "Assign Instructor" on any course
   - Select from available instructors

3. **Manage Enrollments**
   - Click "Manage Students" on any course
   - Add or remove students as needed

### For Analysts

- Access pre-built analytics from your dashboard
- View real-time statistics and trends
- Export data for further analysis

---

## 🗄️ Database Schema

### Core Tables (15 Total)

**Entity Tables:**
- `Users` - Base table for all users
- `Students` - Student-specific information
- `Instructors` - Instructor profiles
- `Courses` - Course catalog
- `Universities` - Partner institutions
- `Programs` - Academic programs
- `Content` - Learning materials
- `Topics` - Subject matter tags
- `Textbooks` - Course textbooks

**Relationship Tables:**
- `Enrolled_In` - Student enrollments
- `Taught_By` - Instructor assignments
- `Has_Content` - Course materials
- `Course_Topics` - Course categorization
- `Program_Courses` - Program curricula
- `Prerequisites` - Course dependencies
- `Student_Skills` - Student competencies

### Database Views (3)

1. **course_enrollment_stats** - Aggregate enrollment and performance data
2. **student_performance** - Student rankings and averages
3. **instructor_workload** - Teaching load analysis

## 📁 Project Structure

```
academiapro/
│
├── app_server.py                      # Main Flask application
├── setup_database.sql                  # Database schema and sample data
├── requirements.txt            # Python dependencies
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Landing page
│   ├── login.html             # Authentication
│   ├── register.html          # User registration
│   │__ 404.html               #client error
|   |__ 500.html               #server html
│   ├── student_*.html         # Student views
│   ├── instructor_*.html      # Instructor views
│   ├── admin_*.html           # Admin views
│   └── analyst_dashboard.html # Analytics view
│
├── static/
    └── css/
      └── style.css          # Custom styling
```

---

## 🎯 Key Functionalities Implemented

### ✅ Core Features

- [x] Role-based authentication and authorization
- [x] Dynamic dashboard routing based on user type
- [x] Course catalog with search functionality
- [x] Student enrollment system
- [x] Course content management
- [x] Grade management system
- [x] User management (CRUD operations)
- [x] Real-time analytics and reporting
- [x] Responsive design for all devices

### ✅ Database Features

- [x] Normalized database schema (3NF)
- [x] Foreign key constraints with CASCADE
- [x] Database views for complex queries
- [x] Sample data for testing
- [x] Proper indexing on primary keys

### ✅ UI/UX Features

- [x] Modern, clean interface
- [x] Bootstrap-based responsive design
- [x] Consistent navigation across all pages
- [x] Flash messages for user feedback
- [x] Form validation
- [x] Loading states and error handling

---

## 🔧 Configuration

### Flask Configuration

```python
app.secret_key = 'your-secret-key'  # Change in production
app.run(debug=True, host='0.0.0.0', port=30032)
```

## 📚 API Endpoints

### Authentication
- `GET /` - Landing page
- `GET/POST /login` - User authentication
- `GET/POST /register` - New user registration
- `GET /logout` - End session

### Student Routes
- `GET /student/dashboard` - Student home
- `GET /student/courses` - Browse courses
- `POST /student/enroll/<course_id>` - Enroll in course
- `GET /student/course/<course_id>` - Course details

### Instructor Routes
- `GET /instructor/dashboard` - Instructor home
- `GET /instructor/course/<course_id>` - Manage course
- `POST /instructor/course/<course_id>/add_content` - Add material
- `POST /instructor/course/<course_id>/update_marks` - Update grades

### Admin Routes
- `GET /admin/dashboard` - Admin home
- `GET /admin/courses` - Course management
- `POST /admin/add_course` - Create course
- `GET /admin/users` - User management
- `POST /admin/assign_instructor/<course_id>` - Assign instructor

### Analyst Routes
- `GET /analyst/dashboard` - Analytics dashboard
---

<div align="center">

Made with ❤️ by The DB Architects

</div>

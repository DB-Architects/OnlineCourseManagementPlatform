"""
Online Course Management Platform - Flask Application
Database Management Systems Lab Assignment IV
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',           # <--- CHANGED: Force IPv4 instead of 'localhost'
    'database': '23CS30052',       # Your roll number
    'user': '23CS30052',           # Your roll number
    'password': '23CS30052',       # Your roll number
    'port': '5432'
}
# Database connection helper
def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Authentication decorators
def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to require specific role(s) for certain routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get some statistics for the homepage
            cur.execute("SELECT COUNT(*) as count FROM Courses")
            total_courses = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM Students")
            total_students = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM Instructors")
            total_instructors = cur.fetchone()['count']
            
            # Get some featured courses
            cur.execute("""
                SELECT c.course_id, c.name, c.credits, c.description, u.name as university
                FROM Courses c
                LEFT JOIN Universities u ON c.university_id = u.university_id
                LIMIT 6
            """)
            featured_courses = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template('index.html', 
                                 stats={
                                     'courses': total_courses,
                                     'students': total_students,
                                     'instructors': total_instructors
                                 },
                                 featured_courses=featured_courses)
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return render_template('index.html', stats={}, featured_courses=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with Plain Text Passwords"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
                user = cur.fetchone()
                
                # CHANGED: Direct string comparison instead of check_password_hash
                if user and user['password'] == password:
                    # Set session variables
                    session['user_id'] = user['user_id']
                    session['name'] = user['name']
                    session['email'] = user['email']
                    session['role'] = user['role_type']
                    
                    flash(f'Welcome back, {user["name"]}!', 'success')
                    cur.close()
                    conn.close()
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid email or password.', 'danger')
                
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Login error: {e}")
                flash('An error occurred during login.', 'danger')
                conn.close()
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with Plain Text Passwords"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password') # Plain text password
        phone_number = request.form.get('country_code', '') + request.form.get('phone_number', '')
        country = request.form.get('country')
        gender = request.form.get('gender')
        role_type = request.form.get('role_type', 'Student')
        
        date_of_birth = request.form.get('date_of_birth')
        post = request.form.get('post')
        university_id = request.form.get('university_id')
        
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                
                # Check email
                cur.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
                if cur.fetchone():
                    flash('Email already registered.', 'danger')
                    cur.close()
                    conn.close()
                    return redirect(url_for('register'))
                
                # CHANGED: Storing password directly as plain text
                cur.execute("""
                    INSERT INTO Users (name, email, password, phone_number, country, gender, role_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING user_id
                """, (name, email, password, phone_number, country, gender, role_type))
                
                user_id = cur.fetchone()['user_id']
                
                # Auto-generate IDs
                current_year = datetime.now().year
                
                if role_type == 'Student':
                    student_roll_id = f"STU{current_year}{user_id:05d}"
                    cur.execute("""
                        INSERT INTO Students (user_id, student_roll_id, date_of_birth)
                        VALUES (%s, %s, %s)
                    """, (user_id, student_roll_id, date_of_birth if date_of_birth else None))
                
                elif role_type == 'Instructor':
                    faculty_id = f"FAC{current_year}{user_id:05d}"
                    cur.execute("""
                        INSERT INTO Instructors (user_id, faculty_id, post, university_id)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, faculty_id, post, university_id if university_id else None))
                
                conn.commit()
                flash('Registration successful! Please log in.', 'success')
                cur.close()
                conn.close()
                return redirect(url_for('login'))
                
            except Exception as e:
                conn.rollback()
                print(f"Registration error: {e}")
                flash(f'An error occurred: {e}', 'danger')
                cur.close()
                conn.close()
    
    conn = get_db_connection()
    universities = []
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT university_id, name FROM Universities ORDER BY name")
            universities = cur.fetchall()
            cur.close()
            conn.close()
        except Exception:
            conn.close()
    
    return render_template('register.html', universities=universities)
@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# ==================== DASHBOARD ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Role-based dashboard redirect"""
    role = session.get('role')
    
    if role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'Instructor':
        return redirect(url_for('instructor_dashboard'))
    elif role == 'Student':
        return redirect(url_for('student_dashboard'))
    elif role == 'Analyst':
        return redirect(url_for('analyst_dashboard'))
    else:
        return render_template('dashboard.html')

# ==================== STUDENT ROUTES ====================

@app.route('/student/dashboard')
@role_required('Student')
def student_dashboard():
    """Student dashboard"""
    user_id = session.get('user_id')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get student info with CGPA
            cur.execute("""
                SELECT * FROM student_performance WHERE user_id = %s
            """, (user_id,))
            student = cur.fetchone()
            
            # Get enrolled courses (FIXED: Added JOIN to Universities to get university name)
            cur.execute("""
                SELECT c.course_id, c.name, c.credits, u.name as university, e.marks, e.enrollment_date
                FROM Enrolled_In e
                JOIN Courses c ON e.course_id = c.course_id
                LEFT JOIN Universities u ON c.university_id = u.university_id
                WHERE e.student_id = %s
                ORDER BY e.enrollment_date DESC
            """, (user_id,))
            enrolled_courses = cur.fetchall()

            # Get Student Skills
            cur.execute("""
                SELECT skill_name 
                FROM Student_Skills 
                WHERE user_id = %s
            """, (user_id,))
            skills = [row['skill_name'] for row in cur.fetchall()]
            
            cur.close()
            conn.close()
            
            return render_template('student_dashboard.html', 
                                 data={
                                     'student': student,
                                     'enrolled_courses': enrolled_courses,
                                     'skills': skills
                                 })
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return render_template('student_dashboard.html', data={})

@app.route('/student/courses')
@role_required('Student')
def student_courses():
    """Browse available courses"""
    user_id = session.get('user_id')
    search = request.args.get('search', '')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # FIXED: Changed alias 'u.name as university' to 'u.name as university_name'
            query = """
                SELECT c.course_id, c.name, c.credits, c.description, 
                       u.name as university_name,
                       EXISTS(SELECT 1 FROM Enrolled_In WHERE student_id = %s AND course_id = c.course_id) as is_enrolled,
                       (SELECT COUNT(*) FROM Enrolled_In WHERE course_id = c.course_id) as enrolled_count
                FROM Courses c
                LEFT JOIN Universities u ON c.university_id = u.university_id
            """
            
            if search:
                query += " WHERE c.name ILIKE %s OR c.description ILIKE %s"
                cur.execute(query + " ORDER BY c.name", (user_id, f'%{search}%', f'%{search}%'))
            else:
                cur.execute(query + " ORDER BY c.name", (user_id,))
            
            courses = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template('student_courses.html', courses=courses, search=search)
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return render_template('student_courses.html', courses=[], search=search)

@app.route('/student/course/<int:course_id>')
@role_required('Student')
def student_course_detail(course_id):
    """View course details"""
    user_id = session.get('user_id')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get course details
            cur.execute("""
                SELECT c.*, u.name as university_name, t.title as textbook_title, t.author as textbook_author
                FROM Courses c
                LEFT JOIN Universities u ON c.university_id = u.university_id
                LEFT JOIN Textbooks t ON c.textbook_isbn = t.isbn
                WHERE c.course_id = %s
            """, (course_id,))
            course = cur.fetchone()
            
            if not course:
                flash('Course not found.', 'danger')
                cur.close()
                conn.close()
                return redirect(url_for('student_courses'))
            
            # Check enrollment status
            cur.execute("""
                SELECT marks, enrollment_date FROM Enrolled_In 
                WHERE student_id = %s AND course_id = %s
            """, (user_id, course_id))
            enrollment = cur.fetchone()
            
            # Get instructors
            cur.execute("""
                SELECT u.name, i.faculty_id, i.post, uni.name as university
                FROM Taught_By tb
                JOIN Instructors i ON tb.instructor_id = i.user_id
                JOIN Users u ON i.user_id = u.user_id
                LEFT JOIN Universities uni ON i.university_id = uni.university_id
                WHERE tb.course_id = %s
            """, (course_id,))
            instructors = cur.fetchall()
            
            # Get topics
            cur.execute("""
                SELECT t.name
                FROM Course_Topics ct
                JOIN Topics t ON ct.topic_id = t.topic_id
                WHERE ct.course_id = %s
            """, (course_id,))
            topics = cur.fetchall()
            
            # Get content
            cur.execute("""
                SELECT c.title, c.url, c.type
                FROM Has_Content hc
                JOIN Content c ON hc.content_id = c.content_id
                WHERE hc.course_id = %s
            """, (course_id,))
            content = cur.fetchall()
            
            cur.close()
            conn.close()
            
            # FIXED: Wrapped in 'data' dictionary to match HTML template
            return render_template('student_course_detail.html',
                                 data={
                                     'course': course,
                                     'enrollment': enrollment,
                                     'instructors': instructors,
                                     'topics': topics,
                                     'content': content
                                 })
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return redirect(url_for('student_courses'))

@app.route('/student/enroll/<int:course_id>', methods=['POST'])
@role_required('Student')
def enroll_course(course_id):
    """Enroll in a course with Strict Prerequisite Checking"""
    user_id = session.get('user_id')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # 1. Check if already enrolled
            cur.execute("SELECT 1 FROM Enrolled_In WHERE student_id = %s AND course_id = %s", (user_id, course_id))
            if cur.fetchone():
                flash('You are already enrolled in this course.', 'warning')
                cur.close()
                conn.close()
                return redirect(url_for('student_courses'))

            # 2. PREREQUISITE CHECK LOGIC
            # Find prerequisites for the target course
            cur.execute("""
                SELECT p.prereq_id, c.name as prereq_name
                FROM Prerequisites p
                JOIN Courses c ON p.prereq_id = c.course_id
                WHERE p.course_id = %s
            """, (course_id,))
            prerequisites = cur.fetchall()

            if prerequisites:
                for prereq in prerequisites:
                    # Check the student's marks in the prerequisite course
                    cur.execute("""
                        SELECT marks 
                        FROM Enrolled_In 
                        WHERE student_id = %s AND course_id = %s
                    """, (user_id, prereq['prereq_id']))
                    
                    result = cur.fetchone()
                    
                    # Logic: Must have taken the course AND marks must be > 50
                    if not result:
                        flash(f"Cannot enroll: You have not taken the prerequisite course '{prereq['prereq_name']}'.", 'danger')
                        cur.close()
                        conn.close()
                        return redirect(url_for('student_courses'))
                    
                    if result['marks'] is None:
                        flash(f"Cannot enroll: Your prerequisite '{prereq['prereq_name']}' is not yet graded.", 'danger')
                        cur.close()
                        conn.close()
                        return redirect(url_for('student_courses'))
                        
                    if result['marks'] <= 50:
                        flash(f"Cannot enroll: You scored {result['marks']} in prerequisite '{prereq['prereq_name']}'. Minimum 50 required.", 'danger')
                        cur.close()
                        conn.close()
                        return redirect(url_for('student_courses'))

            # 3. If passed all checks, enroll
            cur.execute("""
                INSERT INTO Enrolled_In (student_id, course_id, marks, enrollment_date)
                VALUES (%s, %s, NULL, CURRENT_TIMESTAMP)
            """, (user_id, course_id))
            
            conn.commit()
            flash('Successfully enrolled in the course!', 'success')
            
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Enrollment error: {e}")
            flash('Failed to enroll in the course.', 'danger')
            conn.close()
    
    return redirect(url_for('student_course_detail', course_id=course_id))

@app.route('/student/unenroll/<int:course_id>', methods=['POST'])
@role_required('Student')
def unenroll_course(course_id):
    """Unenroll from a course"""
    user_id = session.get('user_id')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM Enrolled_In WHERE student_id = %s AND course_id = %s
            """, (user_id, course_id))
            conn.commit()
            flash('Successfully unenrolled from the course.', 'success')
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Unenrollment error: {e}")
            flash('Failed to unenroll from the course.', 'danger')
            conn.close()
    
    return redirect(url_for('student_courses'))

# ==================== INSTRUCTOR ROUTES ====================

# ==================== INSTRUCTOR ROUTES ====================

@app.route('/instructor/dashboard')
@role_required('Instructor')
def instructor_dashboard():
    """Instructor dashboard"""
    user_id = session.get('user_id')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get instructor info
            cur.execute("""
                SELECT i.*, u.name, u.email, uni.name as university_name
                FROM Instructors i
                JOIN Users u ON i.user_id = u.user_id
                LEFT JOIN Universities uni ON i.university_id = uni.university_id
                WHERE i.user_id = %s
            """, (user_id,))
            instructor = cur.fetchone()
            
            # Get courses taught
            cur.execute("""
                SELECT c.course_id, c.name, c.credits, c.description,
                       (SELECT COUNT(*) FROM Enrolled_In WHERE course_id = c.course_id) as student_count
                FROM Taught_By tb
                JOIN Courses c ON tb.course_id = c.course_id
                WHERE tb.instructor_id = %s
                ORDER BY c.name
            """, (user_id,))
            courses = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template('instructor_dashboard.html',
                                 data={
                                     'instructor': instructor,
                                     'courses': courses
                                 })
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return render_template('instructor_dashboard.html', data={})

@app.route('/instructor/course/<int:course_id>')
@role_required('Instructor')
def instructor_course_detail(course_id):
    """View course details and manage content"""
    user_id = session.get('user_id')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Verify instructor teaches this course
            cur.execute("""
                SELECT 1 FROM Taught_By WHERE instructor_id = %s AND course_id = %s
            """, (user_id, course_id))
            
            if not cur.fetchone():
                flash('You do not have permission to view this course.', 'danger')
                cur.close()
                conn.close()
                return redirect(url_for('instructor_dashboard'))
            
            # Get course details
            cur.execute("""
                SELECT c.*, u.name as university_name
                FROM Courses c
                LEFT JOIN Universities u ON c.university_id = u.university_id
                WHERE c.course_id = %s
            """, (course_id,))
            course = cur.fetchone()
            
            # FIXED QUERY: Added "AS student_id" so the HTML popup works
            cur.execute("""
                SELECT u.user_id AS student_id, u.name, s.student_roll_id, e.marks, e.enrollment_date
                FROM Enrolled_In e
                JOIN Students s ON e.student_id = s.user_id
                JOIN Users u ON s.user_id = u.user_id
                WHERE e.course_id = %s
                ORDER BY u.name
            """, (course_id,))
            students = cur.fetchall()
            
            # Get content
            cur.execute("""
                SELECT c.content_id, c.title, c.url, c.type
                FROM Has_Content hc
                JOIN Content c ON hc.content_id = c.content_id
                WHERE hc.course_id = %s
            """, (course_id,))
            content = cur.fetchall()
            
            # Get topics
            cur.execute("""
                SELECT t.topic_id, t.name
                FROM Course_Topics ct
                JOIN Topics t ON ct.topic_id = t.topic_id
                WHERE ct.course_id = %s
            """, (course_id,))
            topics = cur.fetchall()
            
            # Get all available topics for adding
            cur.execute("SELECT topic_id, name FROM Topics ORDER BY name")
            all_topics = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template('instructor_course_detail.html',
                                 data={
                                     'course': course,
                                     'students': students,
                                     'content': content,
                                     'topics': topics,
                                     'all_topics': all_topics
                                 })
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return redirect(url_for('instructor_dashboard'))


@app.route('/instructor/course/<int:course_id>/add-content', methods=['POST'])
@role_required('Instructor')
def add_content(course_id):
    """Add content to a course"""
    user_id = session.get('user_id')
    title = request.form.get('title')
    url = request.form.get('url')
    content_type = request.form.get('type')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Verify permission
            cur.execute("SELECT 1 FROM Taught_By WHERE instructor_id = %s AND course_id = %s", (user_id, course_id))
            if not cur.fetchone():
                flash('Permission denied.', 'danger')
                return redirect(url_for('instructor_dashboard'))
            
            # Insert content
            cur.execute("""
                INSERT INTO Content (title, url, type) VALUES (%s, %s, %s) RETURNING content_id
            """, (title, url, content_type))
            content_id = cur.fetchone()['content_id']
            
            # Link content
            cur.execute("INSERT INTO Has_Content (course_id, content_id) VALUES (%s, %s)", (course_id, content_id))
            
            conn.commit()
            flash('Content added successfully!', 'success')
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Error adding content: {e}")
            flash('Failed to add content.', 'danger')
            conn.close()
    
    return redirect(url_for('instructor_course_detail', course_id=course_id))

@app.route('/instructor/course/<int:course_id>/update-marks', methods=['POST'])
@role_required('Instructor')
def update_marks(course_id):
    """Update student marks"""
    user_id = session.get('user_id')
    student_id = request.form.get('student_id')
    marks = request.form.get('marks')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # Verify permission
            cur.execute("SELECT 1 FROM Taught_By WHERE instructor_id = %s AND course_id = %s", (user_id, course_id))
            if not cur.fetchone():
                flash('Permission denied.', 'danger')
                return redirect(url_for('instructor_dashboard'))
            
            # Update marks
            cur.execute("""
                UPDATE Enrolled_In SET marks = %s WHERE student_id = %s AND course_id = %s
            """, (marks, student_id, course_id))
            
            conn.commit()
            flash('Marks updated successfully!', 'success')
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Error updating marks: {e}")
            flash('Failed to update marks.', 'danger')
            conn.close()
    
    return redirect(url_for('instructor_course_detail', course_id=course_id))


# ==================== ADMIN ROUTES ====================

# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@role_required('Admin')
def admin_dashboard():
    """Admin dashboard"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get statistics
            cur.execute("SELECT COUNT(*) as count FROM Students")
            total_students = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM Instructors")
            total_instructors = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM Courses")
            total_courses = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM Universities")
            total_universities = cur.fetchone()['count']
            
            # Get recent enrollments
            cur.execute("""
                SELECT u.name as student_name, c.name as course_name, e.enrollment_date
                FROM Enrolled_In e
                JOIN Users u ON e.student_id = u.user_id
                JOIN Courses c ON e.course_id = c.course_id
                ORDER BY e.enrollment_date DESC
                LIMIT 10
            """)
            recent_enrollments = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template('admin_dashboard.html',
                                 stats={
                                     'total_students': total_students,
                                     'total_instructors': total_instructors,
                                     'total_courses': total_courses,
                                     'total_universities': total_universities
                                 },
                                 recent_enrollments=recent_enrollments)
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return render_template('admin_dashboard.html', stats={}, recent_enrollments=[])

@app.route('/admin/users')
@role_required('Admin')
def admin_users():
    """Manage users"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get all users
            cur.execute("""
                SELECT u.user_id, u.name, u.email, u.role_type, u.country,
                       s.student_roll_id, i.faculty_id
                FROM Users u
                LEFT JOIN Students s ON u.user_id = s.user_id
                LEFT JOIN Instructors i ON u.user_id = i.user_id
                ORDER BY u.created_at DESC
            """)
            users = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template('admin_users.html', users=users)
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return render_template('admin_users.html', users=[])

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@role_required('Admin')
def delete_user(user_id):
    """Delete a user"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            conn.commit()
            flash('User deleted successfully!', 'success')
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Error deleting user: {e}")
            flash('Failed to delete user.', 'danger')
            conn.close()
    
    return redirect(url_for('admin_users'))

@app.route('/admin/courses')
@role_required('Admin')
def admin_courses():
    """Manage courses"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get all courses
            cur.execute("""
                SELECT c.course_id, c.name, c.credits, c.description, u.name as university_name,
                       (SELECT COUNT(*) FROM Enrolled_In WHERE course_id = c.course_id) as enrollment_count,
                       (SELECT COUNT(*) FROM Taught_By WHERE course_id = c.course_id) as instructor_count
                FROM Courses c
                LEFT JOIN Universities u ON c.university_id = u.university_id
                ORDER BY c.name
            """)
            courses = cur.fetchall()
            
            # Get universities for the form
            cur.execute("SELECT university_id, name FROM Universities ORDER BY name")
            universities = cur.fetchall()
            
            # Get textbooks for the form
            cur.execute("SELECT isbn, title FROM Textbooks ORDER BY title")
            textbooks = cur.fetchall()
            
            # Get instructors for assignment
            cur.execute("""
                SELECT i.user_id, u.name, i.faculty_id
                FROM Instructors i
                JOIN Users u ON i.user_id = u.user_id
                ORDER BY u.name
            """)
            instructors = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template('admin_courses.html',
                                 courses=courses,
                                 universities=universities,
                                 textbooks=textbooks,
                                 instructors=instructors)
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return render_template('admin_courses.html', courses=[], universities=[], textbooks=[], instructors=[])

# --- THIS IS THE FUNCTION THAT CAUSED THE ERROR ---
# Renamed from add_course() to admin_add_course() to match HTML
@app.route('/admin/courses/add', methods=['POST'])
@role_required('Admin')
def admin_add_course():
    """Add a new course"""
    name = request.form.get('name')
    credits = request.form.get('credits')
    university_id = request.form.get('university_id')
    textbook_isbn = request.form.get('textbook_isbn')
    description = request.form.get('description')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Courses (name, credits, university_id, textbook_isbn, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, credits, university_id if university_id else None,
                  textbook_isbn if textbook_isbn else None, description))
            conn.commit()
            flash('Course added successfully!', 'success')
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Error adding course: {e}")
            flash('Failed to add course. Course name might already exist.', 'danger')
            conn.close()
    
    return redirect(url_for('admin_courses'))

@app.route('/admin/courses/delete/<int:course_id>', methods=['POST'])
@role_required('Admin')
def delete_course(course_id):
    """Delete a course"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM Courses WHERE course_id = %s", (course_id,))
            conn.commit()
            flash('Course deleted successfully!', 'success')
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Error deleting course: {e}")
            flash('Failed to delete course.', 'danger')
            conn.close()
    
    return redirect(url_for('admin_courses'))

@app.route('/admin/courses/<int:course_id>/assign-instructor', methods=['POST'])
@role_required('Admin')
def assign_instructor(course_id):
    """Assign an instructor to a course"""
    instructor_id = request.form.get('instructor_id')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Taught_By (instructor_id, course_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (instructor_id, course_id))
            conn.commit()
            flash('Instructor assigned successfully!', 'success')
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Error assigning instructor: {e}")
            flash('Failed to assign instructor.', 'danger')
            conn.close()
    
    return redirect(url_for('admin_courses'))

@app.route('/admin/manage-enrollment/<int:course_id>')
@role_required('Admin')
def admin_manage_enrollment(course_id):
    """Manage student enrollments for a specific course"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # 1. Get Course Details
            cur.execute("SELECT * FROM Courses WHERE course_id = %s", (course_id,))
            course = cur.fetchone()
            
            if not course:
                flash('Course not found', 'danger')
                cur.close()
                conn.close()
                return redirect(url_for('admin_courses'))

            # 2. Get Enrolled Students for THIS course
            cur.execute("""
                SELECT s.user_id as student_id, u.name, s.student_roll_id, e.marks
                FROM Enrolled_In e
                JOIN Students s ON e.student_id = s.user_id
                JOIN Users u ON s.user_id = u.user_id
                WHERE e.course_id = %s
                ORDER BY u.name
            """, (course_id,))
            enrolled_students = cur.fetchall()
            
            # 3. Get All Students to calculate who is available to add
            cur.execute("""
                SELECT s.user_id, u.name, s.student_roll_id
                FROM Students s
                JOIN Users u ON s.user_id = u.user_id
                ORDER BY u.name
            """)
            all_students = cur.fetchall()
            
            # 4. Filter: Available = All - Enrolled
            enrolled_ids = {s['student_id'] for s in enrolled_students}
            available_students = [s for s in all_students if s['user_id'] not in enrolled_ids]
            
            cur.close()
            conn.close()
            
            # FIXED: Sending 'data' dictionary as expected by HTML
            return render_template('admin_manage_enrollment.html',
                                 data={
                                     'course': course,
                                     'enrolled_students': enrolled_students,
                                     'available_students': available_students
                                 })
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return redirect(url_for('admin_courses'))

# FIXED: Renamed to match HTML 'admin_add_student' and added course_id param
@app.route('/admin/course/<int:course_id>/add-student', methods=['POST'])
@role_required('Admin')
def admin_add_student(course_id):
    """Add a student to a course"""
    student_id = request.form.get('student_id')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Enrolled_In (student_id, course_id, enrollment_date)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT DO NOTHING
            """, (student_id, course_id))
            conn.commit()
            flash('Student enrolled successfully!', 'success')
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Error enrolling student: {e}")
            flash('Failed to enroll student.', 'danger')
            conn.close()
    
    return redirect(url_for('admin_manage_enrollment', course_id=course_id))

# FIXED: Renamed to match HTML 'admin_remove_student' and added params
@app.route('/admin/course/<int:course_id>/remove-student/<int:student_id>', methods=['POST'])
@role_required('Admin')
def admin_remove_student(course_id, student_id):
    """Remove a student from a course"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM Enrolled_In
                WHERE student_id = %s AND course_id = %s
            """, (student_id, course_id))
            conn.commit()
            flash('Student unenrolled successfully!', 'success')
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            print(f"Error unenrolling student: {e}")
            flash('Failed to unenroll student.', 'danger')
            conn.close()
    
    return redirect(url_for('admin_manage_enrollment', course_id=course_id))

# ==================== ANALYST ROUTES ====================

@app.route('/analyst/dashboard')
@role_required('Analyst')
def analyst_dashboard():
    """Data analyst dashboard"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # 1. Course enrollment statistics
            cur.execute("""
                SELECT c.name as course_name, 
                       COUNT(e.student_id) as total_students,
                       AVG(e.marks) as average_marks,
                       MAX(e.marks) as highest_marks,
                       MIN(e.marks) as lowest_marks
                FROM Courses c
                LEFT JOIN Enrolled_In e ON c.course_id = e.course_id
                GROUP BY c.course_id, c.name
                ORDER BY total_students DESC
            """)
            course_stats = cur.fetchall()
            
            # 2. Top performing students
            cur.execute("""
                SELECT u.name, s.student_roll_id,
                       (SUM(e.marks * c.credits) / NULLIF(SUM(c.credits), 0)) / 10 as cgpa,
                       AVG(e.marks) as average_marks
                FROM Students s
                JOIN Users u ON s.user_id = u.user_id
                JOIN Enrolled_In e ON s.user_id = e.student_id
                JOIN Courses c ON e.course_id = c.course_id
                GROUP BY s.user_id, u.name, s.student_roll_id
                ORDER BY cgpa DESC
                LIMIT 10
            """)
            top_students = cur.fetchall()
            
            # 3. FIXED & IMPROVED: Instructor workload
            # Uses STRING_AGG to list course names
            cur.execute("""
                SELECT u.name, i.faculty_id, uni.name as university,
                       COUNT(tb.course_id) as course_count,
                       STRING_AGG(c.name, ', ') as course_list
                FROM Instructors i
                JOIN Users u ON i.user_id = u.user_id
                LEFT JOIN Universities uni ON i.university_id = uni.university_id
                LEFT JOIN Taught_By tb ON i.user_id = tb.instructor_id
                LEFT JOIN Courses c ON tb.course_id = c.course_id
                GROUP BY i.user_id, u.name, i.faculty_id, uni.name
                ORDER BY course_count DESC
            """)
            instructor_workload = cur.fetchall()
            
            # 4. Enrollment trends
            cur.execute("""
                SELECT TO_CHAR(enrollment_date, 'YYYY-MM-DD') as date, COUNT(*) as count
                FROM Enrolled_In
                WHERE enrollment_date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY TO_CHAR(enrollment_date, 'YYYY-MM-DD')
                ORDER BY date DESC
            """)
            enrollment_trends = cur.fetchall()
            
            # 5. University statistics
            cur.execute("""
                SELECT u.name, COUNT(DISTINCT c.course_id) as course_count
                FROM Universities u
                LEFT JOIN Courses c ON u.university_id = c.university_id
                GROUP BY u.name
                ORDER BY course_count DESC
            """)
            university_stats = cur.fetchall()

            # 6. NEW: Students by Program (Distinct students taking courses in a program)
            cur.execute("""
                SELECT p.name as program, COUNT(DISTINCT e.student_id) as student_count
                FROM Programs p
                JOIN Program_Courses pc ON p.name = pc.program_name
                JOIN Enrolled_In e ON pc.course_id = e.course_id
                GROUP BY p.name
                ORDER BY student_count DESC
            """)
            students_by_program = cur.fetchall()

            # 7. NEW: Enrollments by Topic (Popularity of topics)
            cur.execute("""
                SELECT t.name as topic, COUNT(e.student_id) as enrollment_count
                FROM Topics t
                JOIN Course_Topics ct ON t.topic_id = ct.topic_id
                JOIN Enrolled_In e ON ct.course_id = e.course_id
                GROUP BY t.name
                ORDER BY enrollment_count DESC
                LIMIT 8
            """)
            enrollments_by_topic = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return render_template('analyst_dashboard.html',
                                 data={
                                     'course_stats': course_stats,
                                     'top_students': top_students,
                                     'instructor_workload': instructor_workload,
                                     'enrollment_trends': enrollment_trends,
                                     'university_stats': university_stats,
                                     'students_by_program': students_by_program,
                                     'enrollments_by_topic': enrollments_by_topic
                                 })
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
    
    return render_template('analyst_dashboard.html', data={})
# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    return render_template('500.html'), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    # Create static directory and CSS file if they don't exist
    os.makedirs('static/css', exist_ok=True)
    
    # Check if database connection works
    conn = get_db_connection()
    if conn:
        print("✓ Database connection successful")
        conn.close()
    else:
        print("✗ Database connection failed - please check your configuration")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)

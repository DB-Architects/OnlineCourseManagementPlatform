from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash  # Added for encryption
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # <--- REPLACE THIS WITH YOUR REAL PASSWORD
    'database': 'course_management'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Authentication Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            # Fetch user by email
            cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            # CHANGED: Direct comparison (Plain Text)
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['user_id']
                session['name'] = user['name']
                session['role'] = user['role_type']
                flash(f'Welcome {user["name"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        plain_password = request.form['password']
        hashed_password = generate_password_hash(plain_password)
        
        # Phone Number Logic
        country_code = request.form.get('country_code', '')
        phone_number_only = request.form.get('phone_number', '')
        full_phone = f"{country_code}{phone_number_only}"

        country = request.form.get('country', '')
        gender = request.form.get('gender', '')
        role = request.form['role']

        # Validation
        if len(phone_number_only) != 10 or not phone_number_only.isdigit():
             flash('Phone number must be exactly 10 digits.', 'error')
             return render_template('register.html')
        
        # CHANGED: No encryption, storing plain password
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO Users (name, email, password, phone_number, country, gender, role_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, email, hashed_password, full_phone, country, gender, role))
                
                user_id = cursor.lastrowid
                
                if role == 'Student':
                    roll_id = f"STU{user_id:05d}"
                    # REMOVED cgpa from INSERT statement
                    cursor.execute("""
                        INSERT INTO Students (user_id, student_roll_id, date_of_birth)
                        VALUES (%s, %s, %s)
                    """, (user_id, roll_id, None))
                
                elif role == 'Instructor':
                    faculty_id = f"FAC{user_id:05d}"
                    cursor.execute("""
                        INSERT INTO Instructors (user_id, faculty_id, post, university_id)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, faculty_id, None, None))
                
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except Error as e:
                conn.rollback()
                flash(f'Registration failed: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Main dashboard based on user role"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role')
    
    if role == 'Student':
        return redirect(url_for('student_dashboard'))
    elif role == 'Instructor':
        return redirect(url_for('instructor_dashboard'))
    elif role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'Analyst':
        return redirect(url_for('analyst_dashboard'))
    
    return render_template('dashboard.html')

# Student Routes
@app.route('/student/dashboard')
def student_dashboard():
    """Student dashboard"""
    if 'user_id' not in session or session.get('role') != 'Student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    data = {}
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get student info
        cursor.execute("""
            SELECT s.*, u.name, u.email,
                   (SELECT SUM(e.marks * c.credits) / SUM(c.credits) / 10 
                    FROM Enrolled_In e 
                    JOIN Courses c ON e.course_id = c.course_id 
                    WHERE e.student_id = s.user_id AND e.marks IS NOT NULL) as cgpa
            FROM Students s 
            JOIN Users u ON s.user_id = u.user_id 
            WHERE s.user_id = %s
        """, (session['user_id'],))
        data['student'] = cursor.fetchone()
        
        # Get enrolled courses
        cursor.execute("""
            SELECT c.*, e.marks, e.enrollment_date
            FROM Courses c
            JOIN Enrolled_In e ON c.course_id = e.course_id
            WHERE e.student_id = %s
        """, (session['user_id'],))
        data['enrolled_courses'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
    
    return render_template('student_dashboard.html', data=data)

@app.route('/student/courses')
def student_courses():
    """View all available courses"""
    if 'user_id' not in session or session.get('role') != 'Student':
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '')
    
    conn = get_db_connection()
    courses = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if search_query:
            cursor.execute("""
                SELECT c.*, u.name as university_name,
                       (SELECT COUNT(*) FROM Enrolled_In WHERE course_id = c.course_id) as enrollment_count
                FROM Courses c
                LEFT JOIN Universities u ON c.university_id = u.university_id
                WHERE c.name LIKE %s OR c.description LIKE %s
            """, (f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute("""
                SELECT c.*, u.name as university_name,
                       (SELECT COUNT(*) FROM Enrolled_In WHERE course_id = c.course_id) as enrollment_count
                FROM Courses c
                LEFT JOIN Universities u ON c.university_id = u.university_id
            """)
        
        courses = cursor.fetchall()
        
        # Check which courses the student is already enrolled in
        cursor.execute("""
            SELECT course_id FROM Enrolled_In WHERE student_id = %s
        """, (session['user_id'],))
        enrolled_ids = [row['course_id'] for row in cursor.fetchall()]
        
        for course in courses:
            course['is_enrolled'] = course['course_id'] in enrolled_ids
        
        cursor.close()
        conn.close()
    
    return render_template('student_courses.html', courses=courses, search_query=search_query)

@app.route('/student/enroll/<int:course_id>', methods=['POST'])
def enroll_course(course_id):
    """Enroll in a course"""
    if 'user_id' not in session or session.get('role') != 'Student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Enrolled_In (student_id, course_id)
                VALUES (%s, %s)
            """, (session['user_id'], course_id))
            conn.commit()
            flash('Successfully enrolled in course!', 'success')
        except Error as e:
            conn.rollback()
            flash(f'Enrollment failed: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('student_courses'))

@app.route('/student/course/<int:course_id>')
def student_course_detail(course_id):
    """View course details and content"""
    if 'user_id' not in session or session.get('role') != 'Student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    data = {}
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get course details
        cursor.execute("""
            SELECT c.*, u.name as university_name, t.title as textbook_title, t.author as textbook_author
            FROM Courses c
            LEFT JOIN Universities u ON c.university_id = u.university_id
            LEFT JOIN Textbooks t ON c.textbook_isbn = t.isbn
            WHERE c.course_id = %s
        """, (course_id,))
        data['course'] = cursor.fetchone()
        
        # Get instructors
        cursor.execute("""
            SELECT u.name, i.post, uni.name as university
            FROM Taught_By tb
            JOIN Instructors i ON tb.instructor_id = i.user_id
            JOIN Users u ON i.user_id = u.user_id
            LEFT JOIN Universities uni ON i.university_id = uni.university_id
            WHERE tb.course_id = %s
        """, (course_id,))
        data['instructors'] = cursor.fetchall()
        
        # Get content
        cursor.execute("""
            SELECT cnt.*
            FROM Content cnt
            JOIN Has_Content hc ON cnt.content_id = hc.content_id
            WHERE hc.course_id = %s
        """, (course_id,))
        data['content'] = cursor.fetchall()
        
        # Get topics
        cursor.execute("""
            SELECT t.name
            FROM Topics t
            JOIN Course_Topics ct ON t.topic_id = ct.topic_id
            WHERE ct.course_id = %s
        """, (course_id,))
        data['topics'] = cursor.fetchall()
        
        # Get enrollment info if enrolled
        cursor.execute("""
            SELECT marks, enrollment_date
            FROM Enrolled_In
            WHERE student_id = %s AND course_id = %s
        """, (session['user_id'], course_id))
        data['enrollment'] = cursor.fetchone()
        
        cursor.close()
        conn.close()
    
    return render_template('student_course_detail.html', data=data)

# Instructor Routes
@app.route('/instructor/dashboard')
def instructor_dashboard():
    """Instructor dashboard"""
    if 'user_id' not in session or session.get('role') != 'Instructor':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    data = {}
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get instructor info
        cursor.execute("""
            SELECT i.*, u.name, u.email, uni.name as university_name
            FROM Instructors i
            JOIN Users u ON i.user_id = u.user_id
            LEFT JOIN Universities uni ON i.university_id = uni.university_id
            WHERE i.user_id = %s
        """, (session['user_id'],))
        data['instructor'] = cursor.fetchone()
        
        # Get courses teaching
        cursor.execute("""
            SELECT c.*, 
                   (SELECT COUNT(*) FROM Enrolled_In WHERE course_id = c.course_id) as student_count
            FROM Courses c
            JOIN Taught_By tb ON c.course_id = tb.course_id
            WHERE tb.instructor_id = %s
        """, (session['user_id'],))
        data['courses'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
    
    return render_template('instructor_dashboard.html', data=data)

@app.route('/instructor/course/<int:course_id>')
def instructor_course_detail(course_id):
    """View course details for instructor"""
    if 'user_id' not in session or session.get('role') != 'Instructor':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    data = {}
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Verify instructor teaches this course
        cursor.execute("""
            SELECT * FROM Taught_By WHERE instructor_id = %s AND course_id = %s
        """, (session['user_id'], course_id))
        
        if not cursor.fetchone():
            flash('You do not have access to this course', 'error')
            return redirect(url_for('instructor_dashboard'))
        
        # Get course details
        cursor.execute("""
            SELECT c.*, u.name as university_name
            FROM Courses c
            LEFT JOIN Universities u ON c.university_id = u.university_id
            WHERE c.course_id = %s
        """, (course_id,))
        data['course'] = cursor.fetchone()
        
        # Get enrolled students
        cursor.execute("""
            SELECT s.user_id, u.name, s.student_roll_id, e.marks, e.enrollment_date
            FROM Enrolled_In e
            JOIN Students s ON e.student_id = s.user_id
            JOIN Users u ON s.user_id = u.user_id
            WHERE e.course_id = %s
        """, (course_id,))
        data['students'] = cursor.fetchall()
        
        # Get content
        cursor.execute("""
            SELECT cnt.*
            FROM Content cnt
            JOIN Has_Content hc ON cnt.content_id = hc.content_id
            WHERE hc.course_id = %s
        """, (course_id,))
        data['content'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
    
    return render_template('instructor_course_detail.html', data=data)

@app.route('/instructor/add_content/<int:course_id>', methods=['POST'])
def add_content(course_id):
    """Add content to a course"""
    if 'user_id' not in session or session.get('role') != 'Instructor':
        return redirect(url_for('login'))
    
    title = request.form['title']
    url = request.form['url']
    content_type = request.form['type']
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Verify instructor teaches this course
            cursor.execute("""
                SELECT * FROM Taught_By WHERE instructor_id = %s AND course_id = %s
            """, (session['user_id'], course_id))
            
            if not cursor.fetchone():
                flash('You do not have access to this course', 'error')
            else:
                # Insert content
                cursor.execute("""
                    INSERT INTO Content (title, url, type)
                    VALUES (%s, %s, %s)
                """, (title, url, content_type))
                
                content_id = cursor.lastrowid
                
                # Link content to course
                cursor.execute("""
                    INSERT INTO Has_Content (course_id, content_id)
                    VALUES (%s, %s)
                """, (course_id, content_id))
                
                conn.commit()
                flash('Content added successfully!', 'success')
        except Error as e:
            conn.rollback()
            flash(f'Failed to add content: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('instructor_course_detail', course_id=course_id))

@app.route('/instructor/update_marks/<int:course_id>', methods=['POST'])
def update_marks(course_id):
    """Update student marks"""
    if 'user_id' not in session or session.get('role') != 'Instructor':
        return redirect(url_for('login'))
    
    student_id = request.form['student_id']
    marks = request.form['marks']
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Enrolled_In
                SET marks = %s
                WHERE student_id = %s AND course_id = %s
            """, (marks, student_id, course_id))
            conn.commit()
            flash('Marks updated successfully!', 'success')
        except Error as e:
            conn.rollback()
            flash(f'Failed to update marks: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('instructor_course_detail', course_id=course_id))

# Admin Routes
@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    stats = {}
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) as count FROM Users WHERE role_type = 'Student'")
        stats['total_students'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM Users WHERE role_type = 'Instructor'")
        stats['total_instructors'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM Courses")
        stats['total_courses'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM Universities")
        stats['total_universities'] = cursor.fetchone()['count']
        
        # Recent enrollments
        cursor.execute("""
            SELECT u.name as student_name, c.name as course_name, e.enrollment_date
            FROM Enrolled_In e
            JOIN Users u ON e.student_id = u.user_id
            JOIN Courses c ON e.course_id = c.course_id
            ORDER BY e.enrollment_date DESC
            LIMIT 10
        """)
        stats['recent_enrollments'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
    
    return render_template('admin_dashboard.html', stats=stats)

@app.route('/admin/courses')
def admin_courses():
    """Manage courses"""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    courses = []
    universities = []
    instructors = []  # <--- FIX: Initialize list
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT c.*, u.name as university_name,
                   (SELECT COUNT(*) FROM Enrolled_In WHERE course_id = c.course_id) as enrollment_count
            FROM Courses c
            LEFT JOIN Universities u ON c.university_id = u.university_id
        """)
        courses = cursor.fetchall()
        
        cursor.execute("SELECT * FROM Universities")
        universities = cursor.fetchall()

        # <--- FIX: Fetch instructors for the dropdown
        cursor.execute("SELECT user_id, name FROM Users WHERE role_type = 'Instructor'")
        instructors = cursor.fetchall()
        
        cursor.close()
        conn.close()
    
    # <--- FIX: Pass instructors to template
    return render_template('admin_courses.html', courses=courses, universities=universities, instructors=instructors)

@app.route('/admin/add_course', methods=['POST'])
def admin_add_course():
    """Add a new course"""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    name = request.form['name']
    credits = request.form['credits']
    university_id = request.form.get('university_id') or None
    description = request.form.get('description', '')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Courses (name, credits, university_id, description)
                VALUES (%s, %s, %s, %s)
            """, (name, credits, university_id, description))
            conn.commit()
            flash('Course added successfully!', 'success')
        except Error as e:
            conn.rollback()
            flash(f'Failed to add course: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_courses'))

@app.route('/admin/users')
def admin_users():
    """Manage users"""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    role_filter = request.args.get('role', 'all')
    
    conn = get_db_connection()
    users = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if role_filter != 'all':
            cursor.execute("SELECT * FROM Users WHERE role_type = %s", (role_filter,))
        else:
            cursor.execute("SELECT * FROM Users")
        
        users = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template('admin_users.html', users=users, role_filter=role_filter)

@app.route('/admin/assign_instructor/<int:course_id>', methods=['POST'])
def assign_instructor(course_id):
    """Assign instructor to course"""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    instructor_id = request.form['instructor_id']
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Taught_By (instructor_id, course_id)
                VALUES (%s, %s)
            """, (instructor_id, course_id))
            conn.commit()
            flash('Instructor assigned successfully!', 'success')
        except Error as e:
            conn.rollback()
            flash(f'Failed to assign instructor: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_courses'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            conn.commit()
            flash('User deleted successfully!', 'success')
        except Error as e:
            conn.rollback()
            flash(f'Failed to delete user: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_users'))

@app.route('/admin/manage_enrollment/<int:course_id>')
def admin_manage_enrollment(course_id):
    """Manage course enrollments"""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    data = {}
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Courses WHERE course_id = %s", (course_id,))
        data['course'] = cursor.fetchone()
        
        # Get all students
        cursor.execute("""
            SELECT u.user_id, u.name, s.student_roll_id
            FROM Users u
            JOIN Students s ON u.user_id = s.user_id
            WHERE u.role_type = 'Student'
        """)
        data['all_students'] = cursor.fetchall()
        
        # Get enrolled students
        cursor.execute("""
            SELECT e.student_id, u.name, s.student_roll_id, e.marks
            FROM Enrolled_In e
            JOIN Users u ON e.student_id = u.user_id
            JOIN Students s ON e.student_id = s.user_id
            WHERE e.course_id = %s
        """, (course_id,))
        data['enrolled_students'] = cursor.fetchall()
        
        enrolled_ids = [s['student_id'] for s in data['enrolled_students']]
        data['available_students'] = [s for s in data['all_students'] if s['user_id'] not in enrolled_ids]
        
        cursor.close()
        conn.close()
    
    return render_template('admin_manage_enrollment.html', data=data)

@app.route('/admin/add_student_to_course/<int:course_id>', methods=['POST'])
def admin_add_student(course_id):
    """Add student to course"""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    student_id = request.form['student_id']
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Enrolled_In (student_id, course_id)
                VALUES (%s, %s)
            """, (student_id, course_id))
            conn.commit()
            flash('Student added to course successfully!', 'success')
        except Error as e:
            conn.rollback()
            flash(f'Failed to add student: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_manage_enrollment', course_id=course_id))

@app.route('/admin/remove_student_from_course/<int:course_id>/<int:student_id>', methods=['POST'])
def admin_remove_student(course_id, student_id):
    """Remove student from course"""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM Enrolled_In
                WHERE student_id = %s AND course_id = %s
            """, (student_id, course_id))
            conn.commit()
            flash('Student removed from course successfully!', 'success')
        except Error as e:
            conn.rollback()
            flash(f'Failed to remove student: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_manage_enrollment', course_id=course_id))

# Analyst Routes
@app.route('/analyst/dashboard')
def analyst_dashboard():
    """Data analyst dashboard with statistics"""
    if 'user_id' not in session or session.get('role') != 'Analyst':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    data = {}
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Course enrollment statistics
        cursor.execute("SELECT * FROM course_enrollment_stats")
        data['course_stats'] = cursor.fetchall()
        
        # Student performance
        cursor.execute("SELECT * FROM student_performance ORDER BY average_marks DESC LIMIT 10")
        data['top_students'] = cursor.fetchall()
        
        # Instructor workload
        cursor.execute("SELECT * FROM instructor_workload")
        data['instructor_workload'] = cursor.fetchall()
        
        # Enrollment trends
        cursor.execute("""
            SELECT DATE_FORMAT(enrollment_date, '%Y-%m') as month,
                   COUNT(*) as enrollments
            FROM Enrolled_In
            GROUP BY DATE_FORMAT(enrollment_date, '%Y-%m')
            ORDER BY month DESC
            LIMIT 6
        """)
        data['enrollment_trends'] = cursor.fetchall()
        
        # Popular courses
        cursor.execute("""
            SELECT c.name, COUNT(e.student_id) as enrollment_count
            FROM Courses c
            LEFT JOIN Enrolled_In e ON c.course_id = e.course_id
            GROUP BY c.course_id, c.name
            ORDER BY enrollment_count DESC
            LIMIT 10
        """)
        data['popular_courses'] = cursor.fetchall()
        
        # University statistics
        cursor.execute("""
            SELECT u.name, COUNT(c.course_id) as course_count
            FROM Universities u
            LEFT JOIN Courses c ON u.university_id = c.university_id
            GROUP BY u.university_id, u.name
        """)
        data['university_stats'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
    
    return render_template('analyst_dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=30032)
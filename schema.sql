-- Database Creation
DROP DATABASE IF EXISTS course_management;
CREATE DATABASE course_management;
USE course_management;

-- Users Table (Base Table)
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    country VARCHAR(50),
    gender VARCHAR(10),
    role_type ENUM('Student', 'Instructor', 'Admin', 'Analyst') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Universities Table
CREATE TABLE Universities (
    university_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Programs Table
CREATE TABLE Programs (
    name VARCHAR(50) PRIMARY KEY,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students Table
CREATE TABLE Students (
    user_id INT PRIMARY KEY,
    student_roll_id VARCHAR(20) UNIQUE NOT NULL,
    date_of_birth DATE,
   
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Instructors Table
CREATE TABLE Instructors (
    user_id INT PRIMARY KEY,
    faculty_id VARCHAR(20) UNIQUE NOT NULL,
    post VARCHAR(50),
    university_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (university_id) REFERENCES Universities(university_id) ON DELETE SET NULL
);

-- Textbooks Table
CREATE TABLE Textbooks (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses Table
CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    credits INT NOT NULL,
    university_id INT,
    textbook_isbn VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (university_id) REFERENCES Universities(university_id) ON DELETE SET NULL,
    FOREIGN KEY (textbook_isbn) REFERENCES Textbooks(isbn) ON DELETE SET NULL
);

-- Content Table
CREATE TABLE Content (
    content_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Topics Table
CREATE TABLE Topics (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Taught_By Table (Instructor-Course Relationship)
CREATE TABLE Taught_By (
    instructor_id INT,
    course_id INT,
    PRIMARY KEY (instructor_id, course_id),
    FOREIGN KEY (instructor_id) REFERENCES Instructors(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

-- Has_Content Table (Course-Content Relationship)
CREATE TABLE Has_Content (
    course_id INT,
    content_id INT,
    PRIMARY KEY (course_id, content_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES Content(content_id) ON DELETE CASCADE
);

-- Program_Courses Table (Program-Course Relationship)
CREATE TABLE Program_Courses (
    program_name VARCHAR(50),
    course_id INT,
    PRIMARY KEY (program_name, course_id),
    FOREIGN KEY (program_name) REFERENCES Programs(name) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

-- Enrolled_In Table (Student-Course Relationship)
CREATE TABLE Enrolled_In (
    student_id INT,
    course_id INT,
    marks DECIMAL(5,2) DEFAULT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Students(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

-- Course_Topics Table (Course-Topic Relationship)
CREATE TABLE Course_Topics (
    course_id INT,
    topic_id INT,
    PRIMARY KEY (course_id, topic_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id) ON DELETE CASCADE
);

-- Prerequisites Table (Course Prerequisites)
CREATE TABLE Prerequisites (
    course_id INT,
    prereq_id INT,
    PRIMARY KEY (course_id, prereq_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (prereq_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

-- Student_Skills Table
CREATE TABLE Student_Skills (
    user_id INT,
    skill_name VARCHAR(50),
    PRIMARY KEY (user_id, skill_name),
    FOREIGN KEY (user_id) REFERENCES Students(user_id) ON DELETE CASCADE
);

-- Insert Sample Data
-- Sample Universities
INSERT INTO Universities (name) VALUES 
('Massachusetts Institute of Technology'),
('Stanford University'),
('Indian Institute of Technology Kharagpur'),
('University of California Berkeley');

-- Sample Programs
INSERT INTO Programs (name, description) VALUES 
('Computer Science', 'Bachelor of Technology in Computer Science'),
('Data Science', 'Master of Science in Data Science'),
('Artificial Intelligence', 'Specialized program in AI and Machine Learning');

-- Sample Admin User
INSERT INTO Users (name, email, password, role_type, country) 
VALUES ('Admin', 'admin@courseplatform.com', 'scrypt:32768:8:1$h5SmxVjvZ1C790fZ$ba0556cd49a57c54a65cf8ffd7f571d6b616cc518b4d574709ac0b7c73eccce4def93d61488945c5f4a00c04d958b1aa5e7bad78945c69b35d67049d4119beb1', 'Admin', 'USA');
-- -- Sample Instructors
-- INSERT INTO Users (name, email, password, phone_number, country, gender, role_type) VALUES
-- ('Dr. John Smith', 'john.smith@mit.edu', 'pass123', '+1234567891', 'USA', 'Male', 'Instructor'),
-- ('Prof. Sarah Johnson', 'sarah.j@stanford.edu', 'pass123', '+1234567892', 'USA', 'Female', 'Instructor'),
-- ('Dr. Rajesh Kumar', 'rajesh.k@iitkgp.ac.in', 'pass123', '+919876543210', 'India', 'Male', 'Instructor');

-- INSERT INTO Instructors (user_id, faculty_id, post, university_id) VALUES
-- (2, 'MIT001', 'Associate Professor', 1),
-- (3, 'STAN001', 'Professor', 2),
-- (4, 'IIT001', 'Assistant Professor', 3);

-- Sample Students
-- INSERT INTO Users (name, email, password, phone_number, country, gender, role_type) VALUES
-- ('Alice Brown', 'alice.brown@student.edu', 'pass123', '+1234567893', 'USA', 'Female', 'Student'),
-- ('Bob Wilson', 'bob.wilson@student.edu', 'pass123', '+1234567894', 'USA', 'Male', 'Student'),
-- ('Charlie Davis', 'charlie.d@student.edu', 'pass123', '+1234567895', 'Canada', 'Male', 'Student'),
-- ('Diana Prince', 'diana.p@student.edu', 'pass123', '+1234567896', 'UK', 'Female', 'Student');

-- INSERT INTO Students (user_id, student_roll_id, date_of_birth) VALUES
-- (5, 'STU001', '2003-05-15'),
-- (6, 'STU002', '2002-08-22'),
-- (7, 'STU003', '2003-01-10'),
-- (8, 'STU004', '2002-11-30');

-- Sample Data Analyst
INSERT INTO Users (name, email, password, role_type, country) 
VALUES ('Analyst', 'analyst@courseplatform.com', 'scrypt:32768:8:1$BSYCwvLh81xy7qtS$21b900306e4fa57523e4ac1b4eb6eb31c278dd098da4ad6ba9e442300f9ffcf475b1d8bb1ac4584439d596270b4237ed145c2e8298c0079faff7a96197103642', 'Analyst', 'USA');

-- Sample Textbooks
-- INSERT INTO Textbooks (isbn, title, author) VALUES
-- ('978-0262033848', 'Introduction to Algorithms', 'Cormen, Leiserson, Rivest, Stein'),
-- ('978-0134685991', 'Effective Java', 'Joshua Bloch'),
-- ('978-0135957059', 'The Pragmatic Programmer', 'Andrew Hunt, David Thomas'),
-- ('978-0262046305', 'Deep Learning', 'Ian Goodfellow, Yoshua Bengio');

-- -- Sample Courses
-- INSERT INTO Courses (name, credits, university_id, textbook_isbn, description) VALUES
-- ('Introduction to Computer Science', 4, 1, '978-0262033848', 'Fundamental concepts of computer science and programming'),
-- ('Data Structures and Algorithms', 4, 1, '978-0262033848', 'Advanced data structures and algorithm design'),
-- ('Machine Learning', 3, 2, '978-0262046305', 'Introduction to machine learning techniques'),
-- ('Database Management Systems', 4, 3, NULL, 'Design and implementation of database systems'),
-- ('Web Development', 3, 2, NULL, 'Full-stack web application development'),
-- ('Artificial Intelligence', 4, 1, NULL, 'Fundamentals of AI and intelligent systems');

-- Sample Topics
-- INSERT INTO Topics (name) VALUES
-- ('Programming'),
-- ('Algorithms'),
-- ('Machine Learning'),
-- ('Databases'),
-- ('Web Technologies'),
-- ('Artificial Intelligence');

-- -- Link Courses to Topics
-- INSERT INTO Course_Topics (course_id, topic_id) VALUES
-- (1, 1), (1, 2),
-- (2, 1), (2, 2),
-- (3, 3),
-- (4, 4),
-- (5, 5),
-- (6, 6), (6, 3);

-- -- Assign Instructors to Courses
-- INSERT INTO Taught_By (instructor_id, course_id) VALUES
-- (2, 1), (2, 2),
-- (3, 3), (3, 5),
-- (4, 4), (4, 6);

-- -- Link Courses to Programs
-- INSERT INTO Program_Courses (program_name, course_id) VALUES
-- ('Computer Science', 1),
-- ('Computer Science', 2),
-- ('Computer Science', 4),
-- ('Computer Science', 5),
-- ('Data Science', 3),
-- ('Data Science', 4),
-- ('Artificial Intelligence', 3),
-- ('Artificial Intelligence', 6);

-- -- Prerequisites
-- INSERT INTO Prerequisites (course_id, prereq_id) VALUES
-- (2, 1),  -- Data Structures requires Intro to CS
-- (3, 2),  -- Machine Learning requires Data Structures
-- (6, 3);  -- AI requires Machine Learning

-- -- Sample Content
-- INSERT INTO Content (title, url, type) VALUES
-- ('Introduction Lecture', 'https://example.com/lectures/intro.mp4', 'Video'),
-- ('Course Syllabus', 'https://example.com/docs/syllabus.pdf', 'Document'),
-- ('Week 1 Assignment', 'https://example.com/assignments/week1.pdf', 'Assignment'),
-- ('Sorting Algorithms Tutorial', 'https://example.com/tutorials/sorting.mp4', 'Video'),
-- ('Database Design Slides', 'https://example.com/slides/db-design.pdf', 'Document');

-- -- Link Content to Courses
-- INSERT INTO Has_Content (course_id, content_id) VALUES
-- (1, 1), (1, 2), (1, 3),
-- (2, 4),
-- (4, 5);

-- -- Enroll Students in Courses
-- INSERT INTO Enrolled_In (student_id, course_id, marks) VALUES
-- (5, 1, 85.5),
-- (5, 2, 78.0),
-- (5, 3, 92.0),
-- (6, 1, 75.5),
-- (6, 4, 88.0),
-- (7, 2, 95.0),
-- (7, 3, 89.5),
-- (8, 1, 91.0),
-- (8, 5, 87.5);

-- -- Student Skills
-- INSERT INTO Student_Skills (user_id, skill_name) VALUES
-- (5, 'Python'),
-- (5, 'Java'),
-- (5, 'Machine Learning'),
-- (6, 'SQL'),
-- (6, 'Web Development'),
-- (7, 'Python'),
-- (7, 'Data Analysis'),
-- (8, 'JavaScript'),
-- (8, 'React');

-- Create Views for Analytics
CREATE VIEW course_enrollment_stats AS
SELECT 
    c.course_id,
    c.name AS course_name,
    COUNT(e.student_id) AS total_students,
    AVG(e.marks) AS average_marks,
    MAX(e.marks) AS highest_marks,
    MIN(e.marks) AS lowest_marks
FROM Courses c
LEFT JOIN Enrolled_In e ON c.course_id = e.course_id
GROUP BY c.course_id, c.name;

CREATE VIEW student_performance AS
SELECT 
    s.user_id,
    u.name,
    s.student_roll_id,
    -- Dynamic CGPA Calculation: (Sum(Marks*Credits) / Sum(Credits)) / 10
    (SUM(e.marks * c.credits) / NULLIF(SUM(c.credits), 0)) / 10 AS cgpa,
    COUNT(e.course_id) AS courses_enrolled,
    AVG(e.marks) AS average_marks
FROM Students s
JOIN Users u ON s.user_id = u.user_id
LEFT JOIN Enrolled_In e ON s.user_id = e.student_id
LEFT JOIN Courses c ON e.course_id = c.course_id
GROUP BY s.user_id, u.name, s.student_roll_id;

CREATE VIEW instructor_workload AS
SELECT 
    i.user_id,
    u.name,
    i.faculty_id,
    uni.name AS university,
    COUNT(tb.course_id) AS courses_teaching
FROM Instructors i
JOIN Users u ON i.user_id = u.user_id
LEFT JOIN Universities uni ON i.university_id = uni.university_id
LEFT JOIN Taught_By tb ON i.user_id = tb.instructor_id
GROUP BY i.user_id, u.name, i.faculty_id, uni.name;

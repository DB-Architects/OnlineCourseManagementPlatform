-- PostgreSQL Schema for Course Management System
-- Database: 23CS30052
-- Passwords: Plain text ('admin123' for Admin, 'user123' for others)

-- 1. CLEANUP
DROP TABLE IF EXISTS Student_Skills CASCADE;
DROP TABLE IF EXISTS Prerequisites CASCADE;
DROP TABLE IF EXISTS Course_Topics CASCADE;
DROP TABLE IF EXISTS Enrolled_In CASCADE;
DROP TABLE IF EXISTS Program_Courses CASCADE;
DROP TABLE IF EXISTS Has_Content CASCADE;
DROP TABLE IF EXISTS Taught_By CASCADE;
DROP TABLE IF EXISTS Topics CASCADE;
DROP TABLE IF EXISTS Content CASCADE;
DROP TABLE IF EXISTS Courses CASCADE;
DROP TABLE IF EXISTS Textbooks CASCADE;
DROP TABLE IF EXISTS Instructors CASCADE;
DROP TABLE IF EXISTS Students CASCADE;
DROP TABLE IF EXISTS Programs CASCADE;
DROP TABLE IF EXISTS Universities CASCADE;
DROP TABLE IF EXISTS Users CASCADE;

DROP VIEW IF EXISTS instructor_workload;
DROP VIEW IF EXISTS student_performance;
DROP VIEW IF EXISTS course_enrollment_stats;

-- 2. TABLE CREATION
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    country VARCHAR(50),
    gender VARCHAR(10),
    role_type VARCHAR(20) NOT NULL CHECK (role_type IN ('Student', 'Instructor', 'Admin', 'Analyst')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Universities (
    university_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Programs (
    name VARCHAR(50) PRIMARY KEY,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Students (
    user_id INT PRIMARY KEY,
    student_roll_id VARCHAR(20) UNIQUE NOT NULL,
    date_of_birth DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Instructors (
    user_id INT PRIMARY KEY,
    faculty_id VARCHAR(20) UNIQUE NOT NULL,
    post VARCHAR(50),
    university_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (university_id) REFERENCES Universities(university_id) ON DELETE SET NULL
);

CREATE TABLE Textbooks (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Courses (
    course_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    credits INT NOT NULL,
    university_id INT,
    textbook_isbn VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (university_id) REFERENCES Universities(university_id) ON DELETE SET NULL,
    FOREIGN KEY (textbook_isbn) REFERENCES Textbooks(isbn) ON DELETE SET NULL
);

CREATE TABLE Content (
    content_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Topics (
    topic_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Taught_By (
    instructor_id INT,
    course_id INT,
    PRIMARY KEY (instructor_id, course_id),
    FOREIGN KEY (instructor_id) REFERENCES Instructors(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

CREATE TABLE Has_Content (
    course_id INT,
    content_id INT,
    PRIMARY KEY (course_id, content_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES Content(content_id) ON DELETE CASCADE
);

CREATE TABLE Program_Courses (
    program_name VARCHAR(50),
    course_id INT,
    PRIMARY KEY (program_name, course_id),
    FOREIGN KEY (program_name) REFERENCES Programs(name) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

CREATE TABLE Enrolled_In (
    student_id INT,
    course_id INT,
    marks DECIMAL(5,2) DEFAULT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Students(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

CREATE TABLE Course_Topics (
    course_id INT,
    topic_id INT,
    PRIMARY KEY (course_id, topic_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id) ON DELETE CASCADE
);

CREATE TABLE Prerequisites (
    course_id INT,
    prereq_id INT,
    PRIMARY KEY (course_id, prereq_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (prereq_id) REFERENCES Courses(course_id) ON DELETE CASCADE
);

CREATE TABLE Student_Skills (
    user_id INT,
    skill_name VARCHAR(50),
    PRIMARY KEY (user_id, skill_name),
    FOREIGN KEY (user_id) REFERENCES Students(user_id) ON DELETE CASCADE
);

-- 3. DATA POPULATION

-- Universities
INSERT INTO Universities (university_id, name) VALUES 
(1, 'Massachusetts Institute of Technology'),
(2, 'Stanford University'),
(3, 'Indian Institute of Technology Kharagpur'),
(4, 'University of California Berkeley');

-- Programs
INSERT INTO Programs (name, description) VALUES 
('Certificate', 'Short term skill based certification'),
('Degree', 'Full time 4 year undergraduate degree'),
('Training', 'Vocational training program');

-- Textbooks
INSERT INTO Textbooks (isbn, title, author) VALUES
('978-0131103627', 'The C Programming Language', 'Brian Kernighan'),
('978-0132145375', 'Database Systems: The Complete Book', 'Hector Garcia-Molina'),
('978-0073383095', 'Operating System Concepts', 'Abraham Silberschatz'),
('978-0262033848', 'Introduction to Algorithms', 'Thomas H. Cormen');

-- Topics
INSERT INTO Topics (topic_id, name) VALUES
(1, 'Pointers'), (2, 'Memory Management'), 
(3, 'SQL'), (4, 'Normalization'), 
(5, 'Processes'), (6, 'Scheduling'),
(7, 'Dynamic Programming'), (8, 'Graph Theory');

-- =========================================================
-- PLAIN TEXT PASSWORDS
-- Admin: admin123
-- Everyone else: user123
-- =========================================================

-- Admin & Analyst
INSERT INTO Users (user_id, name, email, password, role_type, country) VALUES 
(1, 'Admin', 'admin@courseplatform.com', 'admin123', 'Admin', 'USA'),
(2, 'Analyst', 'analyst@courseplatform.com', 'user123', 'Analyst', 'USA');

-- Instructors
INSERT INTO Users (user_id, name, email, password, role_type, country, gender) VALUES
(10, 'Dr. Alan Turing', 'alan@mit.edu', 'user123', 'Instructor', 'USA', 'Male'),
(11, 'Dr. Grace Hopper', 'grace@stanford.edu', 'user123', 'Instructor', 'USA', 'Female'),
(12, 'Prof. H.C. Verma', 'hcverma@iitkgp.ac.in', 'user123', 'Instructor', 'India', 'Male');

INSERT INTO Instructors (user_id, faculty_id, post, university_id) VALUES
(10, 'FAC-001', 'Professor', 1),
(11, 'FAC-002', 'Assistant Professor', 2),
(12, 'FAC-003', 'Senior Professor', 3);

-- Students
INSERT INTO Users (user_id, name, email, password, role_type, country, gender) VALUES
(20, 'Siddharth Konnur', 'sid@student.com', 'user123', 'Student', 'India', 'Male'),
(21, 'Alice Smith', 'alice@student.com', 'user123', 'Student', 'USA', 'Female'),
(22, 'Bob Jones', 'bob@student.com', 'user123', 'Student', 'UK', 'Male'),
(23, 'Charlie Brown', 'charlie@student.com', 'user123', 'Student', 'Canada', 'Male'),
(24, 'David Lee', 'david@student.com', 'user123', 'Student', 'Singapore', 'Male'),
(25, 'Eva Green', 'eva@student.com', 'user123', 'Student', 'France', 'Female'),
(26, 'Frank Miller', 'frank@student.com', 'user123', 'Student', 'Germany', 'Male'),
(27, 'Grace Lin', 'glin@student.com', 'user123', 'Student', 'China', 'Female'),
(28, 'Harry Potter', 'harry@student.com', 'user123', 'Student', 'UK', 'Male'),
(29, 'Isla Fisher', 'isla@student.com', 'user123', 'Student', 'Australia', 'Female'),
(30, 'Jack Sparrow', 'jack@student.com', 'user123', 'Student', 'USA', 'Male'),
(31, 'Karen Gillan', 'karen@student.com', 'user123', 'Student', 'UK', 'Female'),
(32, 'Leo Messi', 'leo@student.com', 'user123', 'Student', 'Argentina', 'Male'),
(33, 'Mina Myoui', 'mina@student.com', 'user123', 'Student', 'Japan', 'Female'),
(34, 'Nikhil Gupta', 'nikhil@student.com', 'user123', 'Student', 'India', 'Male');

INSERT INTO Students (user_id, student_roll_id, date_of_birth) VALUES
(20, 'STU-2025-001', '2003-05-15'), (21, 'STU-2025-002', '2004-01-20'), (22, 'STU-2025-003', '2003-11-10'), 
(23, 'STU-2025-004', '2004-03-30'), (24, 'STU-2025-005', '2003-06-12'), (25, 'STU-2025-006', '2004-02-14'),
(26, 'STU-2025-007', '2003-09-21'), (27, 'STU-2025-008', '2004-11-05'), (28, 'STU-2025-009', '2003-07-31'),
(29, 'STU-2025-010', '2004-04-19'), (30, 'STU-2025-011', '2003-12-25'), (31, 'STU-2025-012', '2004-08-10'),
(32, 'STU-2025-013', '2003-01-24'), (33, 'STU-2025-014', '2004-03-24'), (34, 'STU-2025-015', '2003-10-02');

-- Courses
INSERT INTO Courses (course_id, name, credits, university_id, textbook_isbn, description) VALUES
(100, 'Introduction to C Programming', 3, 1, '978-0131103627', 'Basics of C, Pointers, and Memory.'),
(101, 'Advanced Database Systems', 4, 2, '978-0132145375', 'SQL, Normalization, and Transactions.'),
(102, 'Operating Systems', 4, 3, '978-0073383095', 'Processes, Threads, and Scheduling.'),
(103, 'Design of Algorithms', 3, 1, '978-0262033848', 'Sorting, Searching, and Dynamic Programming.');

-- Taught By
INSERT INTO Taught_By (instructor_id, course_id) VALUES
(10, 100), (10, 103), (11, 101), (12, 102); 

-- Course Topics
INSERT INTO Course_Topics (course_id, topic_id) VALUES
(100, 1), (100, 2), (101, 3), (101, 4), 
(102, 5), (102, 6), (103, 7), (103, 8); 

-- Content
INSERT INTO Content (content_id, title, url, type) VALUES
(501, 'Lecture 1: Pointers', 'https://youtube.com/lecture1', 'Video'),
(502, 'Lecture 1: SQL Basics', 'https://youtube.com/lecture_sql', 'Video'),
(503, 'Assignment 1 PDF', 'https://drive.google.com/assign1', 'Document');

INSERT INTO Has_Content (course_id, content_id) VALUES
(100, 501), (100, 503), (101, 502);

-- PROGRAM_COURSES
INSERT INTO Program_Courses (program_name, course_id) VALUES
('Certificate', 100),
('Degree', 101),
('Degree', 102),
('Degree', 103),
('Training', 100),
('Training', 103);

-- PREREQUISITES
INSERT INTO Prerequisites (course_id, prereq_id) VALUES
(102, 100), -- C is prereq for OS
(103, 100); -- C is prereq for Algo

-- STUDENT_SKILLS
INSERT INTO Student_Skills (user_id, skill_name) VALUES
(20, 'Python'), (20, 'Java'),
(21, 'C++'), (21, 'SQL'),
(24, 'Web Development'),
(30, 'React'),
(34, 'Machine Learning');

-- ENROLLED_IN
INSERT INTO Enrolled_In (student_id, course_id, marks, enrollment_date) VALUES
-- Course 100: C Programming
(20, 100, 85.00, CURRENT_DATE - INTERVAL '10 days'), 
(21, 100, 98.00, CURRENT_DATE - INTERVAL '5 days'), 
(22, 100, 70.00, CURRENT_DATE - INTERVAL '15 days'),
(23, 100, 35.00, CURRENT_DATE - INTERVAL '2 days'), 
(24, 100, 88.00, CURRENT_DATE - INTERVAL '1 day'), 
(25, 100, 91.50, CURRENT_DATE - INTERVAL '3 days'),
(30, 100, 60.00, CURRENT_DATE - INTERVAL '20 days'), 
(31, 100, 75.00, CURRENT_DATE - INTERVAL '12 days'), 
(34, 100, 82.00, CURRENT_DATE - INTERVAL '4 days'),

-- Course 101: Database Systems
(20, 101, 92.50, CURRENT_DATE - INTERVAL '10 days'), 
(21, 101, 95.00, CURRENT_DATE - INTERVAL '8 days'), 
(25, 101, 89.00, CURRENT_DATE - INTERVAL '2 days'),
(26, 101, 78.00, CURRENT_DATE - INTERVAL '5 days'), 
(27, 101, 65.00, CURRENT_DATE - INTERVAL '3 days'), 
(28, 101, 45.00, CURRENT_DATE - INTERVAL '1 day'),
(29, 101, 88.00, CURRENT_DATE - INTERVAL '1 day'), 
(32, 101, 99.00, CURRENT_DATE - INTERVAL '6 days'), 
(33, 101, 90.00, CURRENT_DATE - INTERVAL '2 days'),

-- Course 102: OS
(20, 102, 78.00, CURRENT_DATE - INTERVAL '25 days'), 
(23, 102, 40.00, CURRENT_DATE - INTERVAL '15 days'), 
(24, 102, 72.00, CURRENT_DATE - INTERVAL '8 days'),
(26, 102, 68.00, CURRENT_DATE - INTERVAL '9 days'), 
(28, 102, 55.00, CURRENT_DATE - INTERVAL '12 days'), 
(30, 102, 62.00, CURRENT_DATE - INTERVAL '18 days'),
(34, 102, 80.00, CURRENT_DATE - INTERVAL '3 days'),

-- Course 103: Algorithms
(21, 103, 99.00, CURRENT_DATE - INTERVAL '1 day'), 
(22, 103, 65.00, CURRENT_DATE - INTERVAL '2 days'), 
(25, 103, 92.00, CURRENT_DATE - INTERVAL '5 days'),
(27, 103, 85.00, CURRENT_DATE - INTERVAL '4 days'), 
(29, 103, 70.00, CURRENT_DATE - INTERVAL '3 days'), 
(31, 103, 74.00, CURRENT_DATE - INTERVAL '2 days'),
(32, 103, 94.00, CURRENT_DATE - INTERVAL '1 day'), 
(33, 103, 89.00, CURRENT_DATE - INTERVAL '1 day');

-- 4. VIEWS RECREATION
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

-- 5. RESET SEQUENCES 
SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM Users));
SELECT setval('universities_university_id_seq', (SELECT MAX(university_id) FROM Universities));
SELECT setval('courses_course_id_seq', (SELECT MAX(course_id) FROM Courses));
SELECT setval('content_content_id_seq', (SELECT MAX(content_id) FROM Content));
SELECT setval('topics_topic_id_seq', (SELECT MAX(topic_id) FROM Topics));

SELECT 'Database schema created successfully!' AS status;

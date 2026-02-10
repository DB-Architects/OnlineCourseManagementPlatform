-- MySQL dump 10.13  Distrib 9.6.0, for macos26.2 (arm64)
--
-- Host: localhost    Database: course_management
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'a7603cbe-04f6-11f1-ae82-13f284bf30b4:1-564';

--
-- Table structure for table `Content`
--

DROP TABLE IF EXISTS `Content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Content` (
  `content_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `url` text NOT NULL,
  `type` varchar(20) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`content_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Content`
--

LOCK TABLES `Content` WRITE;
/*!40000 ALTER TABLE `Content` DISABLE KEYS */;
/*!40000 ALTER TABLE `Content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `course_enrollment_stats`
--

DROP TABLE IF EXISTS `course_enrollment_stats`;
/*!50001 DROP VIEW IF EXISTS `course_enrollment_stats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `course_enrollment_stats` AS SELECT 
 1 AS `course_id`,
 1 AS `course_name`,
 1 AS `total_students`,
 1 AS `average_marks`,
 1 AS `highest_marks`,
 1 AS `lowest_marks`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Course_Topics`
--

DROP TABLE IF EXISTS `Course_Topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Course_Topics` (
  `course_id` int NOT NULL,
  `topic_id` int NOT NULL,
  PRIMARY KEY (`course_id`,`topic_id`),
  KEY `topic_id` (`topic_id`),
  CONSTRAINT `course_topics_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`) ON DELETE CASCADE,
  CONSTRAINT `course_topics_ibfk_2` FOREIGN KEY (`topic_id`) REFERENCES `Topics` (`topic_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Course_Topics`
--

LOCK TABLES `Course_Topics` WRITE;
/*!40000 ALTER TABLE `Course_Topics` DISABLE KEYS */;
/*!40000 ALTER TABLE `Course_Topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Courses`
--

DROP TABLE IF EXISTS `Courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Courses` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `credits` int NOT NULL,
  `university_id` int DEFAULT NULL,
  `textbook_isbn` varchar(20) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`course_id`),
  UNIQUE KEY `name` (`name`),
  KEY `university_id` (`university_id`),
  KEY `textbook_isbn` (`textbook_isbn`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`university_id`) REFERENCES `Universities` (`university_id`) ON DELETE SET NULL,
  CONSTRAINT `courses_ibfk_2` FOREIGN KEY (`textbook_isbn`) REFERENCES `Textbooks` (`isbn`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Courses`
--

LOCK TABLES `Courses` WRITE;
/*!40000 ALTER TABLE `Courses` DISABLE KEYS */;
/*!40000 ALTER TABLE `Courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Enrolled_In`
--

DROP TABLE IF EXISTS `Enrolled_In`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Enrolled_In` (
  `student_id` int NOT NULL,
  `course_id` int NOT NULL,
  `marks` decimal(5,2) DEFAULT NULL,
  `enrollment_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`student_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `enrolled_in_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `Students` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `enrolled_in_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Enrolled_In`
--

LOCK TABLES `Enrolled_In` WRITE;
/*!40000 ALTER TABLE `Enrolled_In` DISABLE KEYS */;
/*!40000 ALTER TABLE `Enrolled_In` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Has_Content`
--

DROP TABLE IF EXISTS `Has_Content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Has_Content` (
  `course_id` int NOT NULL,
  `content_id` int NOT NULL,
  PRIMARY KEY (`course_id`,`content_id`),
  KEY `content_id` (`content_id`),
  CONSTRAINT `has_content_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`) ON DELETE CASCADE,
  CONSTRAINT `has_content_ibfk_2` FOREIGN KEY (`content_id`) REFERENCES `Content` (`content_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Has_Content`
--

LOCK TABLES `Has_Content` WRITE;
/*!40000 ALTER TABLE `Has_Content` DISABLE KEYS */;
/*!40000 ALTER TABLE `Has_Content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `instructor_workload`
--

DROP TABLE IF EXISTS `instructor_workload`;
/*!50001 DROP VIEW IF EXISTS `instructor_workload`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `instructor_workload` AS SELECT 
 1 AS `user_id`,
 1 AS `name`,
 1 AS `faculty_id`,
 1 AS `university`,
 1 AS `courses_teaching`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Instructors`
--

DROP TABLE IF EXISTS `Instructors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Instructors` (
  `user_id` int NOT NULL,
  `faculty_id` varchar(20) NOT NULL,
  `post` varchar(50) DEFAULT NULL,
  `university_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `faculty_id` (`faculty_id`),
  KEY `university_id` (`university_id`),
  CONSTRAINT `instructors_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `instructors_ibfk_2` FOREIGN KEY (`university_id`) REFERENCES `Universities` (`university_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instructors`
--

LOCK TABLES `Instructors` WRITE;
/*!40000 ALTER TABLE `Instructors` DISABLE KEYS */;
/*!40000 ALTER TABLE `Instructors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Prerequisites`
--

DROP TABLE IF EXISTS `Prerequisites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Prerequisites` (
  `course_id` int NOT NULL,
  `prereq_id` int NOT NULL,
  PRIMARY KEY (`course_id`,`prereq_id`),
  KEY `prereq_id` (`prereq_id`),
  CONSTRAINT `prerequisites_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`) ON DELETE CASCADE,
  CONSTRAINT `prerequisites_ibfk_2` FOREIGN KEY (`prereq_id`) REFERENCES `Courses` (`course_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Prerequisites`
--

LOCK TABLES `Prerequisites` WRITE;
/*!40000 ALTER TABLE `Prerequisites` DISABLE KEYS */;
/*!40000 ALTER TABLE `Prerequisites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Program_Courses`
--

DROP TABLE IF EXISTS `Program_Courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Program_Courses` (
  `program_name` varchar(50) NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`program_name`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `program_courses_ibfk_1` FOREIGN KEY (`program_name`) REFERENCES `Programs` (`name`) ON DELETE CASCADE,
  CONSTRAINT `program_courses_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Program_Courses`
--

LOCK TABLES `Program_Courses` WRITE;
/*!40000 ALTER TABLE `Program_Courses` DISABLE KEYS */;
/*!40000 ALTER TABLE `Program_Courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Programs`
--

DROP TABLE IF EXISTS `Programs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Programs` (
  `name` varchar(50) NOT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Programs`
--

LOCK TABLES `Programs` WRITE;
/*!40000 ALTER TABLE `Programs` DISABLE KEYS */;
INSERT INTO `Programs` VALUES ('Artificial Intelligence','Specialized program in AI and Machine Learning','2026-02-10 15:26:44'),('Computer Science','Bachelor of Technology in Computer Science','2026-02-10 15:26:44'),('Data Science','Master of Science in Data Science','2026-02-10 15:26:44');
/*!40000 ALTER TABLE `Programs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `student_performance`
--

DROP TABLE IF EXISTS `student_performance`;
/*!50001 DROP VIEW IF EXISTS `student_performance`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `student_performance` AS SELECT 
 1 AS `user_id`,
 1 AS `name`,
 1 AS `student_roll_id`,
 1 AS `cgpa`,
 1 AS `courses_enrolled`,
 1 AS `average_marks`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Student_Skills`
--

DROP TABLE IF EXISTS `Student_Skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Student_Skills` (
  `user_id` int NOT NULL,
  `skill_name` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`,`skill_name`),
  CONSTRAINT `student_skills_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Students` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Student_Skills`
--

LOCK TABLES `Student_Skills` WRITE;
/*!40000 ALTER TABLE `Student_Skills` DISABLE KEYS */;
/*!40000 ALTER TABLE `Student_Skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Students`
--

DROP TABLE IF EXISTS `Students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Students` (
  `user_id` int NOT NULL,
  `student_roll_id` varchar(20) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `student_roll_id` (`student_roll_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Students`
--

LOCK TABLES `Students` WRITE;
/*!40000 ALTER TABLE `Students` DISABLE KEYS */;
/*!40000 ALTER TABLE `Students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Taught_By`
--

DROP TABLE IF EXISTS `Taught_By`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Taught_By` (
  `instructor_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`instructor_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `taught_by_ibfk_1` FOREIGN KEY (`instructor_id`) REFERENCES `Instructors` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `taught_by_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Taught_By`
--

LOCK TABLES `Taught_By` WRITE;
/*!40000 ALTER TABLE `Taught_By` DISABLE KEYS */;
/*!40000 ALTER TABLE `Taught_By` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Textbooks`
--

DROP TABLE IF EXISTS `Textbooks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Textbooks` (
  `isbn` varchar(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Textbooks`
--

LOCK TABLES `Textbooks` WRITE;
/*!40000 ALTER TABLE `Textbooks` DISABLE KEYS */;
/*!40000 ALTER TABLE `Textbooks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Topics`
--

DROP TABLE IF EXISTS `Topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Topics` (
  `topic_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`topic_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Topics`
--

LOCK TABLES `Topics` WRITE;
/*!40000 ALTER TABLE `Topics` DISABLE KEYS */;
/*!40000 ALTER TABLE `Topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Universities`
--

DROP TABLE IF EXISTS `Universities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Universities` (
  `university_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`university_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Universities`
--

LOCK TABLES `Universities` WRITE;
/*!40000 ALTER TABLE `Universities` DISABLE KEYS */;
INSERT INTO `Universities` VALUES (1,'Massachusetts Institute of Technology','2026-02-10 15:26:44'),(2,'Stanford University','2026-02-10 15:26:44'),(3,'Indian Institute of Technology Kharagpur','2026-02-10 15:26:44'),(4,'University of California Berkeley','2026-02-10 15:26:44');
/*!40000 ALTER TABLE `Universities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `role_type` enum('Student','Instructor','Admin','Analyst') NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'Admin','admin@courseplatform.com','scrypt:32768:8:1$h5SmxVjvZ1C790fZ$ba0556cd49a57c54a65cf8ffd7f571d6b616cc518b4d574709ac0b7c73eccce4def93d61488945c5f4a00c04d958b1aa5e7bad78945c69b35d67049d4119beb1',NULL,'USA',NULL,'Admin','2026-02-10 15:26:44'),(2,'Analyst','analyst@courseplatform.com','scrypt:32768:8:1$BSYCwvLh81xy7qtS$21b900306e4fa57523e4ac1b4eb6eb31c278dd098da4ad6ba9e442300f9ffcf475b1d8bb1ac4584439d596270b4237ed145c2e8298c0079faff7a96197103642',NULL,'USA',NULL,'Analyst','2026-02-10 15:26:44');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `course_enrollment_stats`
--

/*!50001 DROP VIEW IF EXISTS `course_enrollment_stats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `course_enrollment_stats` AS select `c`.`course_id` AS `course_id`,`c`.`name` AS `course_name`,count(`e`.`student_id`) AS `total_students`,avg(`e`.`marks`) AS `average_marks`,max(`e`.`marks`) AS `highest_marks`,min(`e`.`marks`) AS `lowest_marks` from (`courses` `c` left join `enrolled_in` `e` on((`c`.`course_id` = `e`.`course_id`))) group by `c`.`course_id`,`c`.`name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `instructor_workload`
--

/*!50001 DROP VIEW IF EXISTS `instructor_workload`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `instructor_workload` AS select `i`.`user_id` AS `user_id`,`u`.`name` AS `name`,`i`.`faculty_id` AS `faculty_id`,`uni`.`name` AS `university`,count(`tb`.`course_id`) AS `courses_teaching` from (((`instructors` `i` join `users` `u` on((`i`.`user_id` = `u`.`user_id`))) left join `universities` `uni` on((`i`.`university_id` = `uni`.`university_id`))) left join `taught_by` `tb` on((`i`.`user_id` = `tb`.`instructor_id`))) group by `i`.`user_id`,`u`.`name`,`i`.`faculty_id`,`uni`.`name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `student_performance`
--

/*!50001 DROP VIEW IF EXISTS `student_performance`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `student_performance` AS select `s`.`user_id` AS `user_id`,`u`.`name` AS `name`,`s`.`student_roll_id` AS `student_roll_id`,((sum((`e`.`marks` * `c`.`credits`)) / nullif(sum(`c`.`credits`),0)) / 10) AS `cgpa`,count(`e`.`course_id`) AS `courses_enrolled`,avg(`e`.`marks`) AS `average_marks` from (((`students` `s` join `users` `u` on((`s`.`user_id` = `u`.`user_id`))) left join `enrolled_in` `e` on((`s`.`user_id` = `e`.`student_id`))) left join `courses` `c` on((`e`.`course_id` = `c`.`course_id`))) group by `s`.`user_id`,`u`.`name`,`s`.`student_roll_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-10 21:48:20

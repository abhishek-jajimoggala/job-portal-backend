-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: jobportaldb
-- ------------------------------------------------------
-- Server version	8.0.46

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

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'Kiran','adminkiran@gmail.com','$2b$12$O92db8RAxhym1RauZIXJ9.hixv7sB50dYUZPwQd8WJTEWQ8E6lKw2','2026-10-01 05:34:11'),(2,'vardhan','adminvardhan@gmail.com','$2b$12$fFPgpOYVKHC4dWfukelUp.K.NnLthMw26hqc0Sl8q5hY8jQEkI/we','2026-10-04 14:08:40');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `job_id` int NOT NULL,
  `applied_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('Pending','Shortlisted','Rejected') DEFAULT 'Pending',
  `resume` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `job_id` (`job_id`),
  CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `applications_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
INSERT INTO `applications` VALUES (1,3,1,'2026-10-04 17:34:27','Rejected','uploads/resumes\\ABHISHEK_JAJIMOGGALA_FlowCV_Resume_2026-08-25_1_1.docx'),(3,3,3,'2026-10-04 17:40:44','Shortlisted','uploads/resumes\\ABHISHEK_JAJIMOGGALA_FlowCV_Resume_2026-08-25_1_1.docx'),(4,4,3,'2026-10-05 06:17:33','Shortlisted','uploads/resumes\\Rohith_fees_lab_reciept.pdf'),(5,4,1,'2026-10-05 07:25:53','Rejected','uploads/resumes\\Rohith_fees_lab_reciept.pdf'),(6,4,5,'2026-10-05 07:43:15','Rejected','uploads/resumes\\Rohith_fees_lab_reciept.pdf'),(7,3,7,'2026-10-05 07:48:57','Rejected','uploads/resumes\\Abhishek_Jajimoggala_FlowCV_Resume_2026-09-25_1.pdf'),(8,3,12,'2026-10-05 09:19:20','Shortlisted','uploads/resumes\\Abhishek_Jajimoggala_FlowCV_Resume_2026-09-25_1.pdf'),(9,3,13,'2026-10-06 07:37:02','Shortlisted','uploads/resumes\\Abhishek_Jajimoggala_FlowCV_Resume_2026-09-25_1.pdf'),(10,3,14,'2026-10-06 07:44:30','Rejected','uploads/resumes\\Abhishek_Jajimoggala_FlowCV_Resume_2026-09-25_1.pdf'),(11,4,14,'2026-10-06 07:55:29','Rejected','uploads/resumes\\Rohith_fees_lab_reciept.pdf'),(12,4,13,'2026-10-06 07:55:41','Shortlisted','uploads/resumes\\Rohith_fees_lab_reciept.pdf'),(13,4,8,'2026-10-06 07:55:58','Rejected','uploads/resumes\\Rohith_fees_lab_reciept.pdf'),(14,4,12,'2026-10-06 07:57:51','Shortlisted','uploads/resumes\\Rohith_fees_lab_reciept.pdf'),(15,5,12,'2026-10-07 15:27:37','Shortlisted','uploads/resumes\\Ravi_Siva_Ram_Teja_Nagulavancha_Resume.pdf'),(16,6,1,'2026-10-12 04:55:13','Rejected','uploads/resumes\\Abhishek_Jajimoggala_FlowCV_Resume_2026-09-25_1.pdf'),(17,6,13,'2026-10-12 04:56:39','Shortlisted','uploads/resumes\\Abhishek_Jajimoggala_FlowCV_Resume_2026-09-25_1.pdf'),(18,3,5,'2026-10-14 05:43:00','Pending','uploads/resumes\\Abhishek_Jajimoggala_FlowCV_Resume_2026-09-25_1.pdf');
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int DEFAULT NULL,
  `job_title` varchar(255) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `salary` varchar(100) DEFAULT NULL,
  `experience` varchar(100) DEFAULT NULL,
  `job_type` varchar(100) DEFAULT NULL,
  `description` text,
  `skills` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,1,'Unit Testing','Amazon','Hyderabad,Banglore','35000-45000','2-3','Full Time','All skills are required','Python,Sql,Flask,Postman Testing,Unit Testing','2026-10-04 17:17:00'),(3,2,'AIML Intern','Codegnan IT Solutions','VIJAYAWADA','Paid','Any Graduate/Degree','Internship','100% placement Assistance and Mock Interviews','Python,Sql,Flask,Pandas,Numpy,Matplotlib','2026-10-04 17:33:15'),(4,1,'Python Full Stack','Codegnan IT Solutions','Vijayawada','10000','0-4','Remote','All skills are required','HTML,CSS,Javascript,Python,Flask,Mysql,React','2026-10-05 07:21:35'),(5,1,'Backend Engineer','Amazon','Vijayawada,Hyderabad','25000-35000','1-5','Full Time','All skills are mandatory','HTML,CSS,Javascript,Python,Flask,Mysql','2026-10-05 07:22:32'),(6,2,'Backend Engineer','Datavalley.ai','Vijayawada,Hyderabad','35000-45000','2-7','Full Time','All testing is mandatory','Flask,Python,Mysql,Unit testing,react','2026-10-05 07:41:27'),(7,2,'Python Developer','Vision Computers','Hyderabad','2-3 LPA','Fresher','Full Time','All skills are mandatory','Python,Sql,Pandas,Numpy,Machine Learning,Deep Learning,LLM,RAG','2026-10-05 07:45:30'),(8,1,'Vedio Editor','VFX design Pvt.Ltd','Chennai','10000-150000','No Prior Experience','Part Time','Only Night Shifts','Photoshop,Videography,Graphical Designer,Adebo Pro,DTP','2026-10-05 08:36:37'),(9,1,'Gen AI and Prompt Engineering','Datavalley.ai','Hyderabad,Vijayawada','NA','Fresher','Internship','It is only internship and Get certificates','python,Basic Prompts,LAG Models,LLM\'s,Hungging Face,Pandas,Numpy,Data Vizualization','2026-10-05 08:38:41'),(12,1,'Java Full Stack','Nextgile','Hyderabad','45000','1-5 ','Full Time',' java must be besic knowledge and AI','Java,HTML,CSS,JavaScript,SpringBoot Frameworks,MySql,Artificial Intelligence','2026-10-05 09:16:10'),(13,1,'Voice Based Caller(Telecaler)','Southerland','Vijayawada,Hyderabad,Visakhapatnam ','15000-20000','Fresher','Part Time','Telugu,English must be mandatory.Night shifts is mandatory and communication skills are must manadatory US Clients','English,communication skills,listening skills,Telugu,Hindi','2026-10-06 06:43:10'),(14,1,'Web developement Intern','Vision Computers','Vijayawada','PAID','Fresher','Internship','It is offline Internship.It is Paid internship that is 10,000 Rs for 2 months.Intrested candidites fill the details','HTML,CSS,JavaScript,Mysql','2026-10-06 07:16:30'),(15,1,'Unit Testing','Codegnan IT Solutions','Vijayawada,Hyderabad,Visakhapatnam ','2-3 LPA','1-5','Full Time','Minimum basic is required for selection process.Intrested candidates apply the job','Flask,Python,Postman Testing Tool,Unit Testing','2026-10-14 05:36:22');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `saved_jobs`
--

DROP TABLE IF EXISTS `saved_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saved_jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `job_id` int NOT NULL,
  `saved_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `job_id` (`job_id`),
  CONSTRAINT `saved_jobs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `saved_jobs_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saved_jobs`
--

LOCK TABLES `saved_jobs` WRITE;
/*!40000 ALTER TABLE `saved_jobs` DISABLE KEYS */;
INSERT INTO `saved_jobs` VALUES (4,3,3,'2026-10-05 05:57:53'),(5,4,1,'2026-10-05 06:17:42'),(6,4,3,'2026-10-05 06:17:44'),(9,3,6,'2026-10-05 07:48:26'),(10,3,5,'2026-10-05 07:48:27'),(12,3,1,'2026-10-05 07:48:33'),(13,3,12,'2026-10-05 09:34:16'),(14,3,9,'2026-10-05 09:34:39'),(15,3,7,'2026-10-06 07:53:59'),(16,4,8,'2026-10-06 07:55:49'),(17,4,12,'2026-10-06 08:02:56'),(18,4,13,'2026-10-06 08:03:00'),(19,4,14,'2026-10-06 08:03:02'),(20,4,9,'2026-10-06 08:03:05'),(21,5,14,'2026-10-07 15:27:43'),(22,5,12,'2026-10-07 15:27:44'),(24,5,1,'2026-10-07 15:27:49'),(25,5,4,'2026-10-07 15:27:51'),(26,6,13,'2026-10-12 04:55:37'),(27,6,7,'2026-10-12 04:55:39'),(28,6,12,'2026-10-12 04:55:42'),(29,6,14,'2026-10-12 04:55:44'),(30,6,9,'2026-10-12 04:55:47'),(31,6,5,'2026-10-12 04:55:53');
/*!40000 ALTER TABLE `saved_jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `otp` varchar(6) DEFAULT NULL,
  `otp_expiry_time` datetime DEFAULT NULL,
  `account_status` varchar(20) DEFAULT 'inactive',
  `resume_path` varchar(255) DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `skills` text,
  `tenth` varchar(20) DEFAULT NULL,
  `intermediate` varchar(20) DEFAULT NULL,
  `degree` varchar(20) DEFAULT NULL,
  `college` varchar(150) DEFAULT NULL,
  `branch` varchar(100) DEFAULT NULL,
  `passout_year` varchar(10) DEFAULT NULL,
  `experience` varchar(50) DEFAULT NULL,
  `linkedin` varchar(255) DEFAULT NULL,
  `github` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'Abhishek Jajimoggala','abhishekjajimoggala@gmail.com','$2b$12$LdUSAUcfjPeMBorPgjUpZ.Q85TLzofa8JXfyru4olkL5DOBpBKt.G',NULL,NULL,'active','uploads/resumes\\Abhishek_Jajimoggala_FlowCV_Resume_2026-09-25_1.pdf','uploads/profile_images/user_3_b18efb0e74bb42f785285b96a39e2ef8.jpeg','9390758579','IN','AP','Vijayawada','React,Flask,Python,Html,CSS,JavaScript,GEN AI','98','78','7.8','Andhra Loyola Institute of Engineering and Technology','Computer Science and Engineering','2026','Fresher','https://www.linkedin.com/in/abhishek-jajimoggala/','https://www.github.com/abhishek-jajimoggala/'),(4,'Rohith','22hp1a05f6@gmail.com','$2b$12$w6C7Xjl.DmqokRexU5jSv.fjy7xsAtRz9yU6fTgRWu94RuDTTEqXK',NULL,NULL,'active','uploads/resumes\\Rohith_fees_lab_reciept.pdf','uploads/profile_images/user_4_d4ac05a3e21744bd8e5061adca584973.png','8887894562','IN','AP','Vijayawada','React,Python,Java,GEN-AI,pandas,Numpy','98','92','B.TECH','PVP Siddhartha Engineering College','Computer Science and Engineering','2029','Fresher','https://www.linkedin.com/in/rohith-jajimoggala/','https://www.github.com/abhishek-jajimoggala/'),(5,'Siva Shankar','sivashankarjajimoggala@gmail.com','$2b$12$LYnWwWoPTCmaSeAvoXzwzuADFT6lWnuuK/NL0hji2aMrBw9lNQCui',NULL,NULL,'active','uploads/resumes\\Ravi_Siva_Ram_Teja_Nagulavancha_Resume.pdf','uploads/profile_images/user_5_6bf743116ea34869ba66842e06777864.jpeg','9989462286','IN','AP','Vijayawada','Speaking,writting\n','85','NaN','NaN','NaN','NaN','1989','No Prior Experience','NaN','NaN'),(6,'Sree Vardhan','sreevardhankurra@gmail.com','$2b$12$EKxiKLyIzF.ABSQ1UbQYxebVj30uxuHsmigPc0or0ZAdIvvmeZtWW',NULL,NULL,'active','uploads/resumes\\Abhishek_Jajimoggala_FlowCV_Resume_2026-09-25_1.pdf','uploads/profile_images/user_6_5b5a1dab06f0420cbe463d813cc9e59a.png','6302675428','IN','AP','Vijayawada','React,Python,HTML,CSS,Flask','90','95','B.Tech','KLU','Computer Science and Engineering','2026','No Prior Experience','https://www.linkedin.com/in/kranthi-kumar/','https://www.github.com/abhishek-jajimoggala/');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-15 11:47:12

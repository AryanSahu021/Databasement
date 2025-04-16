-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: safedocs
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table accesscontrol
--

DROP TABLE IF EXISTS accesscontrol;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE accesscontrol (
  AccessID int NOT NULL AUTO_INCREMENT,
  DocumentID int NOT NULL,
  MemberID int NOT NULL,
  AccessLevel enum('Read','Download','Edit','Delete') NOT NULL,
  PRIMARY KEY (AccessID),
  KEY DocumentID (DocumentID),
  KEY MemberID (MemberID),
  CONSTRAINT accesscontrol_ibfk_1 FOREIGN KEY (DocumentID) REFERENCES pdfdocument (DocumentID) ON DELETE CASCADE,
  CONSTRAINT accesscontrol_ibfk_2 FOREIGN KEY (MemberID) REFERENCES member (MemberID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table accesscontrol
--

LOCK TABLES accesscontrol WRITE;
/*!40000 ALTER TABLE accesscontrol DISABLE KEYS */;
INSERT INTO accesscontrol VALUES (1,1,2,'Read'),(2,1,3,'Download'),(3,2,4,'Edit'),(4,3,1,'Delete');
/*!40000 ALTER TABLE accesscontrol ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table auditlog
--

DROP TABLE IF EXISTS auditlog;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auditlog (
  LogID int NOT NULL AUTO_INCREMENT,
  DocumentID int NOT NULL,
  MemberID int NOT NULL,
  ActionType enum('View','Download','Edit','Delete','Unauthorized Attempt') NOT NULL,
  Timestamp timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (LogID),
  KEY DocumentID (DocumentID),
  KEY MemberID (MemberID),
  CONSTRAINT auditlog_ibfk_1 FOREIGN KEY (DocumentID) REFERENCES pdfdocument (DocumentID) ON DELETE CASCADE,
  CONSTRAINT auditlog_ibfk_2 FOREIGN KEY (MemberID) REFERENCES member (MemberID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table auditlog
--

LOCK TABLES auditlog WRITE;
/*!40000 ALTER TABLE auditlog DISABLE KEYS */;
INSERT INTO auditlog VALUES (1,1,2,'View','2025-02-28 06:41:55'),(2,1,3,'Download','2025-02-28 06:41:55'),(3,2,4,'Edit','2025-02-28 06:41:55'),(4,3,1,'Delete','2025-02-28 06:41:55');
/*!40000 ALTER TABLE auditlog ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table authenticationlog
--

DROP TABLE IF EXISTS authenticationlog;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE authenticationlog (
  LogID int NOT NULL AUTO_INCREMENT,
  MemberID int NOT NULL,
  LoginTime timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  IPAddress varchar(45) DEFAULT NULL,
  Status enum('Success','Failed') NOT NULL,
  PRIMARY KEY (LogID),
  KEY MemberID (MemberID),
  CONSTRAINT authenticationlog_ibfk_1 FOREIGN KEY (MemberID) REFERENCES member (MemberID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table authenticationlog
--

LOCK TABLES authenticationlog WRITE;
/*!40000 ALTER TABLE authenticationlog DISABLE KEYS */;
INSERT INTO authenticationlog VALUES (1,1,'2025-02-28 06:41:55','192.168.1.1','Success'),(2,2,'2025-02-28 06:41:55','192.168.1.2','Failed'),(3,3,'2025-02-28 06:41:55','192.168.1.3','Success'),(4,4,'2025-02-28 06:41:55','192.168.1.4','Success');
/*!40000 ALTER TABLE authenticationlog ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table failedaccessattempts
--

DROP TABLE IF EXISTS failedaccessattempts;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE failedaccessattempts (
  AttemptID int NOT NULL AUTO_INCREMENT,
  MemberID int NOT NULL,
  DocumentID int NOT NULL,
  AttemptTime timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  Reason varchar(255) NOT NULL,
  PRIMARY KEY (AttemptID),
  KEY MemberID (MemberID),
  KEY DocumentID (DocumentID),
  CONSTRAINT failedaccessattempts_ibfk_1 FOREIGN KEY (MemberID) REFERENCES member (MemberID) ON DELETE CASCADE,
  CONSTRAINT failedaccessattempts_ibfk_2 FOREIGN KEY (DocumentID) REFERENCES pdfdocument (DocumentID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table failedaccessattempts
--

LOCK TABLES failedaccessattempts WRITE;
/*!40000 ALTER TABLE failedaccessattempts DISABLE KEYS */;
INSERT INTO failedaccessattempts VALUES (1,2,3,'2025-02-28 06:41:55','Unauthorized Edit Attempt'),(2,3,1,'2025-02-28 06:41:55','Unauthorized Delete Attempt'),(3,4,2,'2025-02-28 06:41:55','Unauthorized Download Attempt');
/*!40000 ALTER TABLE failedaccessattempts ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table folder
--

DROP TABLE IF EXISTS folder;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE folder (
  FolderID int NOT NULL AUTO_INCREMENT,
  MemberID int NOT NULL,
  FolderName varchar(255) NOT NULL,
  CreationTimestamp timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (FolderID),
  KEY MemberID (MemberID),
  CONSTRAINT folder_ibfk_1 FOREIGN KEY (MemberID) REFERENCES member (MemberID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table folder
--

LOCK TABLES folder WRITE;
/*!40000 ALTER TABLE folder DISABLE KEYS */;
INSERT INTO folder VALUES (1,1,'Work Documents','2025-02-28 06:41:55'),(2,2,'Personal Files','2025-02-28 06:41:55'),(3,3,'Project Docs','2025-02-28 06:41:55'),(4,4,'Research Papers','2025-02-28 06:41:55');
/*!40000 ALTER TABLE folder ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table folderdocuments
--

DROP TABLE IF EXISTS folderdocuments;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE folderdocuments (
  FolderID int NOT NULL,
  DocumentID int NOT NULL,
  PRIMARY KEY (FolderID,DocumentID),
  KEY DocumentID (DocumentID),
  CONSTRAINT folderdocuments_ibfk_1 FOREIGN KEY (FolderID) REFERENCES folder (FolderID) ON DELETE CASCADE,
  CONSTRAINT folderdocuments_ibfk_2 FOREIGN KEY (DocumentID) REFERENCES pdfdocument (DocumentID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table folderdocuments
--

LOCK TABLES folderdocuments WRITE;
/*!40000 ALTER TABLE folderdocuments DISABLE KEYS */;
INSERT INTO folderdocuments VALUES (1,1),(2,2),(3,3),(4,4);
/*!40000 ALTER TABLE folderdocuments ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table member
--

DROP TABLE IF EXISTS member;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE member (
  MemberID int NOT NULL AUTO_INCREMENT,
  Name varchar(255) NOT NULL,
  Image text,
  Age int DEFAULT NULL,
  Email varchar(255) NOT NULL,
  ContactNumber varchar(20) NOT NULL,
  PasswordHash varchar(255) NOT NULL,
  Role enum('Admin','User') NOT NULL,
  PRIMARY KEY (MemberID),
  UNIQUE KEY Email (Email),
  UNIQUE KEY ContactNumber (ContactNumber),
  CONSTRAINT member_chk_1 CHECK ((Age >= 13))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table member
--

LOCK TABLES member WRITE;
/*!40000 ALTER TABLE member DISABLE KEYS */;
INSERT INTO member VALUES (1,'Aryan Sahu','Aryan_Sahu.jpg',20,'aryan.sahu@iitgn.ac.in','8962091321','hashed_password_1','Admin'),(2,'Dewansh Kumar','Dewansh_Kumar.jpg',20,'dewansh.kumar@iitgn.ac.in','6203657123','hashed_password_2','Admin');
/*!40000 ALTER TABLE member ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table pdfdocument
--

DROP TABLE IF EXISTS pdfdocument;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE pdfdocument (
  DocumentID int NOT NULL AUTO_INCREMENT,
  OwnerID int NOT NULL,
  FilePath text NOT NULL,
  UploadTimestamp timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (DocumentID),
  KEY OwnerID (OwnerID),
  CONSTRAINT pdfdocument_ibfk_1 FOREIGN KEY (OwnerID) REFERENCES member (MemberID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table pdfdocument
--

LOCK TABLES pdfdocument WRITE;
/*!40000 ALTER TABLE pdfdocument DISABLE KEYS */;
INSERT INTO pdfdocument VALUES (1,1,'/files/report1.pdf','2025-02-28 06:41:55'),(2,2,'/files/design_doc.pdf','2025-02-28 06:41:55'),(3,3,'/files/project_proposal.pdf','2025-02-28 06:41:55'),(4,4,'/files/user_guide.pdf','2025-02-28 06:41:55');
/*!40000 ALTER TABLE pdfdocument ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table reportanalytics
--

DROP TABLE IF EXISTS reportanalytics;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE reportanalytics (
  ReportID int NOT NULL AUTO_INCREMENT,
  DocumentID int NOT NULL,
  TotalViews int DEFAULT '0',
  TotalDownloads int DEFAULT '0',
  TotalEdits int DEFAULT '0',
  TotalShares int DEFAULT '0',
  PRIMARY KEY (ReportID),
  KEY DocumentID (DocumentID),
  CONSTRAINT reportanalytics_ibfk_1 FOREIGN KEY (DocumentID) REFERENCES pdfdocument (DocumentID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table reportanalytics
--

LOCK TABLES reportanalytics WRITE;
/*!40000 ALTER TABLE reportanalytics DISABLE KEYS */;
INSERT INTO reportanalytics VALUES (1,1,10,5,0,2),(2,2,7,3,2,1),(3,3,5,1,1,0),(4,4,8,2,3,1);
/*!40000 ALTER TABLE reportanalytics ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table sharedrequests
--

DROP TABLE IF EXISTS sharedrequests;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE sharedrequests (
  RequestID int NOT NULL AUTO_INCREMENT,
  SenderID int NOT NULL,
  ReceiverID int NOT NULL,
  DocumentID int NOT NULL,
  Status enum('Pending','Accepted','Rejected') DEFAULT 'Pending',
  RequestTimestamp timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (RequestID),
  KEY SenderID (SenderID),
  KEY ReceiverID (ReceiverID),
  KEY DocumentID (DocumentID),
  CONSTRAINT sharedrequests_ibfk_1 FOREIGN KEY (SenderID) REFERENCES member (MemberID) ON DELETE CASCADE,
  CONSTRAINT sharedrequests_ibfk_2 FOREIGN KEY (ReceiverID) REFERENCES member (MemberID) ON DELETE CASCADE,
  CONSTRAINT sharedrequests_ibfk_3 FOREIGN KEY (DocumentID) REFERENCES pdfdocument (DocumentID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table sharedrequests
--

LOCK TABLES sharedrequests WRITE;
/*!40000 ALTER TABLE sharedrequests DISABLE KEYS */;
INSERT INTO sharedrequests VALUES (1,1,2,1,'Accepted','2025-02-28 06:41:55'),(2,2,3,2,'Pending','2025-02-28 06:41:55'),(3,3,4,3,'Rejected','2025-02-28 06:41:55'),(4,4,1,4,'Accepted','2025-02-28 06:41:55');
/*!40000 ALTER TABLE sharedrequests ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-28 12:20:21
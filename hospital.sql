-- MySQL dump 10.13  Distrib 9.2.0, for Win64 (x86_64)
--
-- Host: localhost    Database: hospital
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `patient_id` int DEFAULT NULL,
  PRIMARY KEY (`appointment_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,'2025-03-28','09:00:00',23),(2,'2025-03-28','10:00:00',24),(3,'2025-03-28','11:00:00',25),(4,'2025-03-28','12:00:00',26),(5,'2025-03-28','13:00:00',27),(6,'2025-03-28','14:00:00',28),(7,'2025-03-28','15:00:00',29),(8,'2025-03-28','16:00:00',30),(9,'2025-03-29','09:00:00',31),(10,'2025-03-29','10:00:00',32),(11,'2025-03-29','11:00:00',33),(12,'2025-03-29','12:00:00',34),(13,'2025-03-29','13:00:00',35),(14,'2025-03-29','14:00:00',36),(15,'2025-03-29','15:00:00',37),(16,'2025-03-29','16:00:00',38),(17,'2025-03-30','09:00:00',39),(18,'2025-03-30','10:00:00',40),(19,'2025-03-30','11:00:00',41),(20,'2025-03-30','12:00:00',42);
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bills`
--

DROP TABLE IF EXISTS `bills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bills` (
  `bill_id` int NOT NULL AUTO_INCREMENT,
  `gross_cost` decimal(8,2) NOT NULL,
  `date` date NOT NULL,
  `doctor_id` int DEFAULT NULL,
  PRIMARY KEY (`bill_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `bills_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bills`
--

LOCK TABLES `bills` WRITE;
/*!40000 ALTER TABLE `bills` DISABLE KEYS */;
INSERT INTO `bills` VALUES (1,500.00,'2024-03-01',1),(2,750.50,'2024-03-02',2),(3,300.25,'2024-03-03',3),(4,620.00,'2024-03-04',4),(5,410.75,'2024-03-05',5),(6,900.20,'2024-03-06',6),(7,280.40,'2024-03-07',7),(8,650.30,'2024-03-08',8),(9,710.60,'2024-03-09',9),(10,320.80,'2024-03-10',10),(11,475.00,'2024-03-11',11),(12,510.90,'2024-03-12',12),(13,620.45,'2024-03-13',13),(14,815.70,'2024-03-14',14),(15,390.30,'2024-03-15',15),(16,530.20,'2024-03-16',16),(17,720.60,'2024-03-17',17),(18,295.80,'2024-03-18',18),(19,485.90,'2024-03-19',19),(20,655.40,'2024-03-20',20);
/*!40000 ALTER TABLE `bills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cares`
--

DROP TABLE IF EXISTS `cares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cares` (
  `patient_id` int NOT NULL,
  `nurse_id` int NOT NULL,
  PRIMARY KEY (`patient_id`,`nurse_id`),
  KEY `nurse_id` (`nurse_id`),
  CONSTRAINT `cares_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cares_ibfk_2` FOREIGN KEY (`nurse_id`) REFERENCES `nurses` (`nurse_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cares`
--

LOCK TABLES `cares` WRITE;
/*!40000 ALTER TABLE `cares` DISABLE KEYS */;
INSERT INTO `cares` VALUES (23,1),(24,2),(25,3),(26,4),(27,5),(28,6),(29,7),(30,8),(31,9),(32,10),(33,11),(34,12),(35,13),(36,14),(37,15),(38,16),(39,17),(40,18),(41,19),(42,20);
/*!40000 ALTER TABLE `cares` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `doctor_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(25) NOT NULL,
  `last_name` varchar(25) NOT NULL,
  `speciality` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`doctor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,'John','Smith','Cardiology'),(2,'Emma','Johnson','Neurology'),(3,'Liam','Williams','Orthopedics'),(4,'Olivia','Brown','Pediatrics'),(5,'Noah','Jones','Dermatology'),(6,'Ava','Garcia','Endocrinology'),(7,'William','Martinez','Gastroenterology'),(8,'Sophia','Davis','Oncology'),(9,'James','Rodriguez','Urology'),(10,'Charlotte','Lopez','Ophthalmology'),(11,'Benjamin','Hernandez','Anesthesiology'),(12,'Mia','Gonzalez','Gynecology'),(13,'Elijah','Wilson','Rheumatology'),(14,'Amelia','Anderson','Nephrology'),(15,'Lucas','Thomas','Pulmonology'),(16,'Harper','Taylor','Hematology'),(17,'Mason','Moore','Psychiatry'),(18,'Evelyn','Jackson','Pathology'),(19,'Logan','Martin','General Surgery'),(20,'Abigail','Lee','Emergency Medicine');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insurances`
--

DROP TABLE IF EXISTS `insurances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insurances` (
  `insurance_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `bill_id` int DEFAULT NULL,
  `net_cost` decimal(8,2) NOT NULL,
  PRIMARY KEY (`insurance_id`),
  KEY `bill_id` (`bill_id`),
  CONSTRAINT `insurances_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `bills` (`bill_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insurances`
--

LOCK TABLES `insurances` WRITE;
/*!40000 ALTER TABLE `insurances` DISABLE KEYS */;
INSERT INTO `insurances` VALUES (21,'HealthSecure',1,250.75),(22,'WellCare Plus',2,180.50),(23,'MediAssist',3,250.00),(24,'SafeHealth',4,275.30),(25,'LifeShield',5,400.00),(26,'HealthSecure',6,150.20),(27,'WellCare Plus',7,200.00),(28,'MediAssist',8,180.90),(29,'SafeHealth',9,220.40),(30,'LifeShield',10,305.80),(31,'HealthSecure',11,250.00),(32,'WellCare Plus',12,330.75),(33,'MediAssist',13,290.60),(34,'SafeHealth',14,410.25),(35,'LifeShield',15,225.00),(36,'HealthSecure',16,360.90),(37,'WellCare Plus',17,190.40),(38,'MediAssist',18,270.30),(39,'SafeHealth',19,315.70),(40,'LifeShield',20,280.55);
/*!40000 ALTER TABLE `insurances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical_record`
--

DROP TABLE IF EXISTS `medical_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_record` (
  `medical_record_id` int NOT NULL AUTO_INCREMENT,
  `sex` char(1) NOT NULL,
  `height` int NOT NULL,
  `vaccination_count` int DEFAULT '0',
  PRIMARY KEY (`medical_record_id`),
  CONSTRAINT `medical_record_chk_1` CHECK ((`sex` in (_cp850'M',_cp850'F')))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_record`
--

LOCK TABLES `medical_record` WRITE;
/*!40000 ALTER TABLE `medical_record` DISABLE KEYS */;
INSERT INTO `medical_record` VALUES (1,'M',175,3),(2,'F',160,2),(3,'M',182,5),(4,'F',155,1),(5,'M',178,4),(6,'F',165,2),(7,'M',185,3),(8,'F',170,6),(9,'M',176,0),(10,'F',162,2),(11,'M',180,5),(12,'F',158,1),(13,'M',174,2),(14,'F',167,3),(15,'M',183,4),(16,'F',159,5),(17,'M',177,2),(18,'F',161,1),(19,'M',181,6),(20,'F',168,3);
/*!40000 ALTER TABLE `medical_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nurses`
--

DROP TABLE IF EXISTS `nurses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nurses` (
  `nurse_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(25) NOT NULL,
  `last_name` varchar(25) NOT NULL,
  `speciality` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`nurse_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nurses`
--

LOCK TABLES `nurses` WRITE;
/*!40000 ALTER TABLE `nurses` DISABLE KEYS */;
INSERT INTO `nurses` VALUES (1,'Emily','Smith','Pediatric Nursing'),(2,'Sarah','Johnson','Emergency Care'),(3,'Olivia','Williams','Critical Care'),(4,'Isabella','Brown','Cardiology'),(5,'Sophia','Jones','Orthopedics'),(6,'Mia','Garcia','Geriatrics'),(7,'Charlotte','Martinez','Surgical Nursing'),(8,'Amelia','Davis','Neonatal Care'),(9,'Lily','Rodriguez','Psychiatric Nursing'),(10,'Ella','Wilson','Oncology Nursing'),(11,'Avery','Moore','Infection Control'),(12,'Harper','Taylor','Labor and Delivery'),(13,'Scarlett','Anderson','Rehabilitation'),(14,'Grace','Thomas','Wound Care'),(15,'Zoe','Jackson','Intensive Care Unit (ICU)'),(16,'Luna','White','Gastroenterology'),(17,'Victoria','Harris','Dialysis Nursing'),(18,'Aria','Martin','Anesthesia Nursing'),(19,'Chloe','Lee','Stroke Rehabilitation'),(20,'Ryan','Webster','Nothing');
/*!40000 ALTER TABLE `nurses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(25) DEFAULT NULL,
  `middle_name` varchar(25) DEFAULT NULL,
  `last_name` varchar(25) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `medical_record_id` int DEFAULT NULL,
  `insurance_id` int DEFAULT NULL,
  PRIMARY KEY (`patient_id`),
  KEY `fk_medical_record` (`medical_record_id`),
  KEY `fk_insurance` (`insurance_id`),
  CONSTRAINT `fk_insurance` FOREIGN KEY (`insurance_id`) REFERENCES `insurances` (`insurance_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_medical_record` FOREIGN KEY (`medical_record_id`) REFERENCES `medical_record` (`medical_record_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (23,'John','A','Smith','1985-05-12','555-1234',1,21),(24,'Emma','B','Johnson','1990-07-24','555-5678',2,22),(25,'Liam','C','Williams','1988-03-10','555-9012',3,23),(26,'Olivia','D','Brown','1992-09-05','555-3456',4,24),(27,'Noah','E','Jones','1987-12-18','555-7890',5,25),(28,'Ava','F','Garcia','1995-06-30','555-2345',6,26),(29,'William','G','Martinez','1983-04-14','555-6789',7,27),(30,'Sophia','H','Davis','1998-11-21','555-1239',8,28),(31,'James','I','Rodriguez','1980-01-07','555-5673',9,29),(32,'Charlotte','J','Lopez','1993-08-16','555-9015',10,30),(33,'Benjamin','K','Hernandez','1986-02-25','555-3452',11,31),(34,'Mia','L','Gonzalez','1997-10-29','555-7896',12,32),(35,'Elijah','M','Wilson','1989-05-03','555-2348',13,33),(36,'Amelia','N','Anderson','1991-07-12','555-6784',14,34),(37,'Lucas','O','Thomas','1984-09-27','555-1236',15,35),(38,'Harper','P','Taylor','1996-12-09','555-5671',16,36),(39,'Mason','Q','Moore','1982-03-22','555-9014',17,37),(40,'Evelyn','R','Jackson','1999-06-15','555-3459',18,38),(41,'Logan','S','Martin','1981-11-05','555-7893',19,39),(42,'Abigail','T','Lee','1994-02-18','555-2347',20,40);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescriptions`
--

DROP TABLE IF EXISTS `prescriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescriptions` (
  `prescription_id` int NOT NULL AUTO_INCREMENT,
  `medicine` varchar(50) NOT NULL,
  `dosage` int NOT NULL,
  `length_days` int NOT NULL,
  `instructions` varchar(300) DEFAULT NULL,
  `patient_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  PRIMARY KEY (`prescription_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `prescriptions_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `prescriptions_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescriptions`
--

LOCK TABLES `prescriptions` WRITE;
/*!40000 ALTER TABLE `prescriptions` DISABLE KEYS */;
INSERT INTO `prescriptions` VALUES (1,'Aspirin',100,10,'Take 1 pill after meals',23,1),(2,'Ibuprofen',200,14,'Take 1 pill every 8 hours',24,2),(3,'Amoxicillin',500,7,'Take 1 pill every 6 hours',25,3),(4,'Lisinopril',10,30,'Take 1 pill every morning',26,4),(5,'Metformin',500,30,'Take 2 pills with meals',27,5),(6,'Atorvastatin',20,30,'Take 1 pill before bedtime',28,6),(7,'Paracetamol',500,5,'Take 1 pill every 4-6 hours',29,7),(8,'Losartan',50,30,'Take 1 pill in the morning',30,8),(9,'Ciprofloxacin',250,7,'Take 1 pill twice a day',31,9),(10,'Prednisone',20,10,'Take 1 pill every day',32,10),(11,'Levothyroxine',75,30,'Take 1 pill in the morning on an empty stomach',33,11),(12,'Hydrochlorothiazide',25,30,'Take 1 pill in the morning',34,12),(13,'Albuterol',90,7,'Take 2 puffs as needed',35,13),(14,'Prozac',20,30,'Take 1 pill every morning',36,14),(15,'Zithromax',250,5,'Take 1 pill daily',37,15),(16,'Citalopram',20,30,'Take 1 pill every morning',38,16),(17,'Pantoprazole',40,30,'Take 1 pill before breakfast',39,17),(18,'Clindamycin',300,10,'Take 1 pill every 6 hours',40,18),(19,'Diazepam',10,10,'Take 1 pill every 8 hours',41,19),(20,'Simvastatin',40,30,'Take 1 pill before bedtime',42,20);
/*!40000 ALTER TABLE `prescriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treats`
--

DROP TABLE IF EXISTS `treats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treats` (
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  PRIMARY KEY (`patient_id`,`doctor_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `treats_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `treats_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treats`
--

LOCK TABLES `treats` WRITE;
/*!40000 ALTER TABLE `treats` DISABLE KEYS */;
INSERT INTO `treats` VALUES (23,1),(24,2),(25,3),(26,4),(27,5),(28,6),(29,7),(30,8),(31,9),(32,10),(33,11),(34,12),(35,13),(36,14),(37,15),(38,16),(39,17),(40,18),(41,19),(42,20);
/*!40000 ALTER TABLE `treats` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-01 19:53:03
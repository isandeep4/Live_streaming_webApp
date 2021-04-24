CREATE DATABASE `database_users` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `table_users` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO database_users.table_users(id,Name,email,password) VALUES (1,'sandeep','sandeep@mail.com','12345');

INSERT INTO database_users.table_users(id,Name,email,password) VALUES (4,'Sanjida','sanjida@mail.com','12345');
INSERT INTO database_users.table_users(id,Name,email,password) VALUES (5,'Sandy','sandeep2@mail.com','12345');
INSERT INTO database_users.table_users(id,Name,email,password) VALUES (6,'kumar','sandeep3@mail.com','12345');

SELECT * FROM database_users.table_users; 
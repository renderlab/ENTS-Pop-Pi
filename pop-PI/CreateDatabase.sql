CREATE DATABASE pop_PI;

 CREATE USER 'popPI'@'localhost' IDENTIFIED BY 'pi';

GRANT ALL PRIVILEGES ON pop_PI TO 'popPI'@'localhost'
        WITH GRANT OPTION;

use pop_PI;

CREATE TABLE MemberAccount (Id int PRIMARY KEY AUTO_INCREMENT,RFID VARCHAR(20), Account INT, Email VARCHAR(250));

CREATE TABLE PopVend (Id int PRIMARY KEY AUTO_INCREMENT,Pop int);
--setup initial records
insert PopVend (Pop) values (0);

CREATE TABLE Inventory (Id int PRIMARY KEY AUTO_INCREMENT,Pop int,PopType VARCHAR(20));
insert Inventory (Pop) values (0);
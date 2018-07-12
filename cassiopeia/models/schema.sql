-- Place SQL Datbase, Schema, and Table DDLs here
CREATE DATABASE cassiopeia;

CREATE TABLE country (
  ID INTEGER PRIMARY KEY AUTO_INCREMENT,
  Name VARCHAR(60) NOT NULL,
  FlagImage VARCHAR(20) NOT NULL
);

CREATE TABLE language (
  ID INTEGER PRIMARY KEY AUTO_INCREMENT,
  Name VARCHAR(60) NOT NULL
);

CREATE TABLE users (
    ID int NOT NULL AUTO_INCREMENT,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    UserName varchar(255) NOT NULL,
    Password varchar(255) NOT NULL,
    Email varchar(255) NOT NULL,
    Age int,
    NativeLanguageID int
    ProgressID int
    PRIMARY KEY (ID),
    UNIQUE (LastName, FirstName)
);




-- Place SQL Datbase, Schema, and Table DDLs here
CREATE DATABASE cassiopeia;

CREATE TABLE country (
  ID INTEGER PRIMARY KEY AUTO_INCREMENT,
  Name VARCHAR(60) NOT NULL,
  FlagImage LONGBLOB NOT NULL
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
    LanguageID int
    PRIMARY KEY (ID),
    UNIQUE (UserName, Email)
);

CREATE TABLE content (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(255) NOT NULL,
    LanguageID int
    PublishDate DateTime,
    URL varchar(MAX),
    Level float, 
    PRIMARY KEY (ID),
    FOREIGN KEY (LanguageID) REFERENCES language(ID)
);

CREATE TABLE locale (
  LanguageID int NOT NULL,
  CountryID int NOT NULL,
  FOREIGN KEY (LanguageID) 
    REFERENCES language(ID)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  FOREIGN KEY (CountryID) 
    REFERENCES country(ID) 
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE user_language_skill (
  UserID int NOT NULL,
  LangaugeID int NOT NULL,
  Skill float NOT NULL,

  FOREIGN KEY (UserID) 
    REFERENCES users(ID)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  FOREIGN KEY (LangaugeID) 
    REFERENCES language(ID) 
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE user_sorted_content (
  UserID int NOT NULL,
  ContentID int NOT NULL,
  SortedSkill int NOT NULL,

  FOREIGN KEY (UserID) 
    REFERENCES users(ID)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  FOREIGN KEY (ContentID) 
    REFERENCES content(ID) 
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE content_category (
  ContentID int NOT NULL,
  CategoryID int NOT NULL

  FOREIGN KEY (ContentID) 
    REFERENCES content(ID)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  FOREIGN KEY (CategoryID) 
    REFERENCES category(ID) 
    ON UPDATE CASCADE ON DELETE RESTRICT
);



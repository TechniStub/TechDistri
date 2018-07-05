DROP DATABASE IF EXISTS products;
DROP DATABASE IF EXISTS users;
DROP DATABASE IF EXISTS machines;
DROP DATABASE IF EXISTS parameters;

CREATE DATABASE products;
CREATE DATABASE users;
CREATE DATABASE machines;
CREATE DATABASE parameters;

CREATE TABLE users.Users (
	Id int NOT NULL AUTO_INCREMENT,
    Nom varchar(50),
    PNom varchar(50),
    Grade int,
    PRIMARY KEY (Id)
);

CREATE TABLE users.Badges (
	Id int NOT NULL,
    Data varchar(50),
    PRIMARY KEY (Id)
);

CREATE TABLE users.Credits (
	Id int NOT NULL,
    Value float,
    PRIMARY KEY (Id)
);

create table users.transactions (
	Id1 int,
    Id2 int,
    Value int,
    PRIMARY KEY(Id1)
);

create table users.permanences (
	Id int,
    Day Date,
    PRIMARY KEY(Id)
);

CREATE TABLE machines.Machines (
	Id int NOT NULL AUTO_INCREMENT,
    Nom varchar(50),
    NomC varchar(20),
    Level int,
    PRIMARY KEY (Id)
);

CREATE TABLE machines.Perm (
	IdMachine int NOT NULL,
    IdUser int NOT NULL,
    Ok varchar(150),
    PRIMARY KEY (IdMachine)
);

CREATE TABLE products.Products (
	Id int,
    Nom varchar(50),
    NomC varchar(20),
    Price float,
    PRIMARY KEY (Id)
);

CREATE TABLE products.Stock (
	Id int,
    Stock int,
    Min int,
    PRIMARY KEY (Id)
);

CREATE TABLE products.Place (
	Id int,
    Row int,
    Col int,
    isPresent boolean,
    PRIMARY KEY (Id)
);

CREATE TABLE parameters.Param (
	Id int,
    Name varchar(50),
    Value varchar(50),
    Type int,
    PRIMARY KEY (Id)
);
-- Database creation
create database BankChurn;
GO

-- Tables creation
-- Demographic table
use [BankChurn]
go

CREATE TABLE demographic(
    CustomerId INT PRIMARY KEY IDENTITY(1, 1),
    Gender NVARCHAR(10),
    Age INT,
    Salary DECIMAL(8,2),
    LocationId INT,
    Churned BIT
);


-- Account table
use [BankChurn]
go

CREATE TABLE account(
    CustomerId INT,
    Tenure INT,
    Balance DECIMAL(10, 2),
    NumProducts INT,
    HasCreditCard BIT,
    IsActive BIT
);

-- Demographic table
use [BankChurn]
go

CREATE TABLE [location](
    LocationId INT PRIMARY KEY IDENTITY(1, 1),
    [Geography] NVARCHAR(15)
);
-- Create a new database
CREATE DATABASE HU_Project_2;
GO

-- Use the newly created database
USE HU_Project_2;
GO

-- Create the AvailableEvents table
CREATE TABLE AvailableEvents (
    EventID INT PRIMARY KEY IDENTITY(1,1),
    NameOfEvent NVARCHAR(255),
    StartDate DATE,
    EndDate DATE,
    Supervisor NVARCHAR(255),
    Organizer NVARCHAR(255),
	Description NVARCHAR(255)
);
GO

-- Create the Teams table
CREATE TABLE Teams (
    TeamID INT PRIMARY KEY IDENTITY(1,1),
    EventID INT,
    NameOfTeam NVARCHAR(255),
    NoOfPlayers INT,
    TeamCaptain NVARCHAR(255),
    Contact NVARCHAR(255),
    Status BIT,
	StudentID INT,
    FOREIGN KEY (EventID) REFERENCES AvailableEvents(EventID),
	FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
);
GO


-- Create the Student table
CREATE TABLE Student (
    StudentID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(255),
    Email NVARCHAR(255),
    Password NVARCHAR(255)
);
GO

-- Create the Gym table
CREATE TABLE Gym (
    GymID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(255),
    Batch NVARCHAR(255),
    BloodGroup NVARCHAR(255),
    PhoneNumber NVARCHAR(50),
    EmergencyPhoneNumber NVARCHAR(50),
    Type NVARCHAR(255),
	Fees BIT,
    Registered BIT,
	FOREIGN KEY (GymID) REFERENCES Student(StudentID)
);
GO

-- Create the Locker table

CREATE TABLE Locker (
    LockerID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(255),
    Registered BIT,
	StudentID INT,
	FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
);
GO

-- Create the Admin table
CREATE TABLE Admin (
    AdminID INT PRIMARY KEY IDENTITY(1,1),
    Email NVARCHAR(255),
    Password NVARCHAR(255)
);
GO

--for checking table data
--select * from Student
--select * from Admin
--select * from AvailableEvents
--select * from Teams
--select * from Gym
--select * from Locker

--first set this so that the StudentID can be inserted
SET IDENTITY_INSERT Student ON;

--Student Table Data
INSERT INTO Student (StudentID, Name, Email, Password)
VALUES
	(00001, 'Ahtihsam Uddin', 'au00001@st.habib.edu.pk', 'password1'),
    (00002, 'Hammad Malik', 'hm00002@st.habib.edu.pk', 'password2'),
    (00003, 'Bilal Ahmed', 'ba00003@st.habib.edu.pk', 'password3'),
    (00004, 'Mubashir Anees', 'ma00004@st.habib.edu.pk', 'password4'),
    (00005, 'Manqad Raza', 'mr00005@st.habib.edu.pk', 'password5'),
    (00006, 'Sarah Iqbal', 'si00006@st.habib.edu.pk', 'password6'),
    (00007, 'Aina shakeel', 'as00007@st.habib.edu.pk', 'password7'),
    (00008, 'Saba Nisar', 'sn00008@st.habib.edu.pk', 'password8'),
    (00009, 'Mysha Zulfiqar', 'mz00009@st.habib.edu.pk', 'password9'),
    (00010, 'Bisma Farooq', 'bf00010@st.habib.edu.pk', 'password10'),
	(22222, 'master key', '2', '2');


--Admin Table Data
SET IDENTITY_INSERT Admin ON;

INSERT INTO Admin (AdminID, Email, Password)
VALUES
    (1, 'Admin1@st.habib.edu.pk', 'password1'),
    (2, 'Admin2@st.habib.edu.pk', 'password2'),
	(11111, '1', '1');


--AvailableEvents table Data
INSERT INTO AvailableEvents (NameOfEvent, StartDate, EndDate, Supervisor, Organizer, Description)
VALUES 
    ('HU Olympiad Futsal Tournamnet', '2024-01-11', '2024-01-18', 'Tahir Khan', 'Amir Siddiqui', 'The HU Olympiad Futsal Tournament, a prestigious and exhilarating event, invites teams to showcase their prowess on the court. Starting January 20, 2024, this tournament is the perfect platform for futsal enthusiasts to compete and demonstrate their skills and teamwork. Teams are composed of five main players and two substitutes, ensuring strategic gameplay and continuous action. The event promises to be a display of agility, precision, and sportsmanship as teams from various departments come together in a quest for glory'),
    ('HU Olympid Volleyball Tournament ', '2024-01-15', '2024-01-22', 'Amir Siddiqui', 'Amir Siddiqui', 'The stage is set for the HU Olympiad Volleyball Tournament, where athleticism and strategy collide in a captivating display of high-flying action. Kicking off on January 24, 2024, this event calls upon teams of six main players and two substitutes to battle it out on the court in pursuit of victory and school-wide acclaim. As the registration deadline draws near on January 22, teams are ramping up their training, honing their serves, spikes, and blocks.')

--Rest of the tables can be populated easily from the Admin and Student Portals






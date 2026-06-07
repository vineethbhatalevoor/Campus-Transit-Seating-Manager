CREATE DATABASE campus_transit_db;
USE campus_transit_db;

show databases;
CREATE TABLE Route (
    Route_ID INT PRIMARY KEY,
    Route_Name VARCHAR(100) NOT NULL,
    Start_Point VARCHAR(100) NOT NULL,
    End_Point VARCHAR(100) NOT NULL
);

CREATE TABLE Bus (
    Bus_ID INT PRIMARY KEY,
    Plate_Number VARCHAR(20) NOT NULL,
    Capacity INT NOT NULL,
    Driver_Name VARCHAR(100) NOT NULL,
    Route_ID INT,
    FOREIGN KEY (Route_ID) REFERENCES Route(Route_ID) ON DELETE SET NULL
);

CREATE TABLE Stop (
    Stop_ID INT,
    Route_ID INT,
    Stop_Name VARCHAR(100) NOT NULL,
    Pickup_Time TIME NOT NULL,
    PRIMARY KEY (Stop_ID, Route_ID),
    FOREIGN KEY (Route_ID) REFERENCES Route(Route_ID) ON DELETE CASCADE
);

CREATE TABLE Student (
    USN VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Department VARCHAR(50) NOT NULL,
    Phone VARCHAR(15) NOT NULL
);

CREATE TABLE Registration (
    Registration_ID INT PRIMARY KEY,
    USN VARCHAR(20),
    Bus_ID INT,
    Stop_ID INT,
    Route_ID INT, 
    Semester INT NOT NULL,
    Fee_Status VARCHAR(20) DEFAULT 'Pending',
    Registration_Date DATE NOT NULL,
    FOREIGN KEY (USN) REFERENCES Student(USN) ON DELETE CASCADE,
    FOREIGN KEY (Bus_ID) REFERENCES Bus(Bus_ID) ON DELETE SET NULL,
    FOREIGN KEY (Stop_ID, Route_ID) REFERENCES Stop(Stop_ID, Route_ID) ON DELETE SET NULL
);


select * from registration;

INSERT INTO Route (Route_ID, Route_Name, Start_Point, End_Point) VALUES 
(1, 'Udupi to Bantakal (Express)', 'Udupi', 'Bantakal'),
(2, 'Manipal via Katapadi', 'Manipal', 'Bantakal');


INSERT INTO Bus (Bus_ID, Plate_Number, Capacity, Driver_Name, Route_ID) VALUES 
(101, 'KA-20-F-1234', 40, 'Satish Acharya', 1),
(102, 'KA-19-C-3848', 35, 'Wilfred', 2);


INSERT INTO Stop (Stop_ID, Route_ID, Stop_Name, Pickup_Time) VALUES 
(1, 1, 'Udupi Service Bus Stand', '07:45:00'),
(2, 1, 'Kalsanka Junction', '07:50:00'),
(3, 2, 'Tiger Circle Manipal', '08:00:00');


INSERT INTO Student (USN, Name, Department, Phone) VALUES 
('4MW24CS181', 'Vineeth Bhat', 'CSE', '7483242500'),
('4MW24CS002', 'Vishnu Prasad', 'CSE', '9880123456'),
('4MW24CS003', 'Shreyas Bhat', 'CSE', '9141112233');


INSERT INTO Registration (Registration_ID, USN, Bus_ID, Stop_ID, Route_ID, Semester, Fee_Status, Registration_Date) VALUES 
(5001, '4MW24CS181', 101, 1, 1, 4, 'Paid', '2026-05-18'),
(5002, '4MW24CS002', 101, 2, 1, 4, 'Pending', '2026-05-19'),
(5003, '4MW24CS003', 102, 3, 2, 4, 'Paid', '2026-05-20');




USE campus_transit_db;

SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

-- Wipe out database records cleanly
TRUNCATE TABLE Registration;
TRUNCATE TABLE Stop;
TRUNCATE TABLE Bus;
TRUNCATE TABLE Student;
TRUNCATE TABLE Route;

SET FOREIGN_KEY_CHECKS = 1;


INSERT INTO Route (Route_ID, Route_Name, Start_Point, End_Point) VALUES 
(1, 'Udupi to Bantakal (Express)', 'Udupi', 'Bantakal'),
(2, 'Manipal via Katapadi', 'Manipal', 'Bantakal');


INSERT INTO Bus (Bus_ID, Plate_Number, Capacity, Driver_Name, Route_ID) VALUES 
(101, 'KA-20-F-1234', 40, 'Satish Acharya', 1),
(102, 'KA-19-C-3848', 35, 'Wilfred', 2);


INSERT INTO Stop (Stop_ID, Route_ID, Stop_Name, Pickup_Time) VALUES 
(1, 1, 'Udupi Service Bus Stand', '07:45:00'),
(2, 1, 'Kalsanka Junction', '07:50:00'),
(3, 2, 'Tiger Circle Manipal', '08:00:00');

INSERT INTO Student (USN, Name, Department, Phone) VALUES  
('4MW24CS181', 'Vineeth Bhat', 'CSE', '7483242500'), 
('4MW24CS002', 'Vishnu Prasad', 'CSE', '9880123456'), 
('4MW24CS003', 'Shreyas Bhat', 'CSE', '9141112233');


INSERT INTO Registration (Registration_ID, USN, Bus_ID, Stop_ID, Route_ID, Semester, Fee_Status, Registration_Date) VALUES  
(5001, '4MW24CS181', 101, 1, 1, 4, 'Paid', '2026-05-18'), 
(5002, '4MW24CS002', 101, 2, 1, 4, 'Pending', '2026-05-19'),
(5003, '4MW24CS003', 102, 3, 2, 4, 'Paid', '2026-05-20')
AS new_reg
ON DUPLICATE KEY UPDATE Fee_Status = new_reg.Fee_Status;

SET SQL_SAFE_UPDATES = 1;



USE campus_transit_db;

SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;
ALTER TABLE Stop MODIFY COLUMN Pickup_Time VARCHAR(20) NOT NULL;
TRUNCATE TABLE Registration;
TRUNCATE TABLE Stop;
INSERT INTO Stop (Stop_ID, Route_ID, Stop_Name, Pickup_Time) VALUES 
(1, 1, 'Udupi Service Bus Stand', '07:45:00'),
(2, 1, 'Kalsanka Junction', '07:50:00'),
(3, 2, 'Tiger Circle Manipal', '08:00:00');
INSERT INTO Registration (Registration_ID, USN, Bus_ID, Stop_ID, Route_ID, Semester, Fee_Status, Registration_Date) VALUES  
(5001, '4MW24CS181', 101, 1, 1, 4, 'Paid', '2026-05-18'), 
(5002, '4MW24CS002', 101, 2, 1, 4, 'Pending', '2026-05-19'),
(5003, '4MW24CS003', 102, 3, 2, 4, 'Paid', '2026-05-20');
SET FOREIGN_KEY_CHECKS = 1;
SET SQL_SAFE_UPDATES = 1;


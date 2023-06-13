CREATE DATABASE IF NOT EXISTS eWaste;

GRANT ALL PRIVILEGES ON eWaste.* TO 'eWaste_user'@'localhost';

USE eWaste;

CREATE TABLE eWasteItems (
    ItemId INT AUTO_INCREMENT,
    UserName VARCHAR(255) NOT NULL,
    ItemType VARCHAR(255),
    ItemWeight DECIMAL(5,2),
    DateSubmitted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(ItemId),
    FOREIGN KEY(UserName) REFERENCES Users(UserName)
);

CREATE TABLE ItemTypeStats (
    ItemType VARCHAR(255),
    TotalWeight DECIMAL(5,2),
    TotalItems INT,
    PRIMARY KEY(ItemType)
);

-- Insert into eWasteItems
INSERT INTO eWasteItems (ItemID, UserName, TypeID, Weight, SubmissionDate) VALUES (1, 'Alice', 1, 100.0, '2023-05-01');
INSERT INTO eWasteItems (ItemID, UserName, TypeID, Weight, SubmissionDate) VALUES (2, 'Bob', 2, 1500.0, '2023-05-02');
INSERT INTO eWasteItems (ItemID, UserName, TypeID, Weight, SubmissionDate) VALUES (3, 'Charlie', 3, 200.0, '2023-05-03');

-- Insert into ItemTypeStats (If you chose to use this table)
INSERT INTO ItemTypeStats (TypeID, TotalWeight, TotalItems) VALUES (1, 100.0, 1);
INSERT INTO ItemTypeStats (TypeID, TotalWeight, TotalItems) VALUES (2, 1500.0, 1);
INSERT INTO ItemTypeStats (TypeID, TotalWeight, TotalItems) VALUES (3, 200.0, 1);
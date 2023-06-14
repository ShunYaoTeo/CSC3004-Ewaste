CREATE DATABASE IF NOT EXISTS service_eWaste;
GRANT ALL PRIVILEGES ON service_eWaste.* TO 'eWaste_user'@'%';
USE service_eWaste;
CREATE TABLE eWasteItems (
    ItemId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(255) NOT NULL,
    ItemType VARCHAR(255),
    ItemWeight DECIMAL(7,2),
    DateSubmitted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE ItemTypeStats (
    UserName VARCHAR(255),
    ItemType VARCHAR(255),
    TotalWeight DECIMAL(7,2),
    TotalItems INT,
    PRIMARY KEY(UserName, ItemType)
);
INSERT INTO eWasteItems (UserName, ItemType, ItemWeight) VALUES ('shunyaoteo99@gmail.com', "batteries", 100.0);
INSERT INTO eWasteItems (UserName, ItemType, ItemWeight) VALUES ('test@test.com', "resistors", 1500.0);
INSERT INTO eWasteItems (UserName, ItemType, ItemWeight) VALUES ('user1@user.com', "wires", 200.0);
INSERT INTO ItemTypeStats (UserName, ItemType, TotalWeight, TotalItems) VALUES ('shunyaoteo99@gmail.com', "batteries", 100.0, 1);
INSERT INTO ItemTypeStats (UserName, ItemType, TotalWeight, TotalItems) VALUES ('test@test.com', "resistors", 1500.0, 1);
INSERT INTO ItemTypeStats (UserName, ItemType, TotalWeight, TotalItems) VALUES ('user1@user.com', "wires", 200.0, 1);
CREATE TABLE User (
  userId SERIAL,
  username CHAR(100) NOT NULL,
  email CHAR(100) NOT NULL,
  isCarer BOOLEAN NOT NULL,
  PRIMARY KEY (userId)
);

CREATE TABLE Password (
  userId INTEGER,
  password CHAR(100) NOT NULL,
  PRIMARY KEY (userId),
  FOREIGN KEY (userId) REFERENCES User
);

CREATE TABLE Prescription (
  userId INTEGER,
  medicationId INTEGER,
  dosage CHAR(100),
  dosageUnit CHAR(100),
  frequency CHAR(100),
  frequencyUnit CHAR(100),
  PRIMARY KEY (userId, medicationId, dosage)
  FOREIGN KEY userId REFERENCES User,
  FOREIGN KEY medicationId REFERENCES Medication
);

CREATE TABLE Medication (
  medicationId SERIAL,
  medicationName CHAR(100) NOT NULL,
  description TEXT,
  imageLink CHAR(100),
  PRIMARY KEY (userId)
);

CREATE TABLE Assignment (
  patientId INTEGER,
  carerId INTEGER,
  PRIMARY KEY (patientId, carerId),
  FOREIGN KEY patientId REFERENCES User,
  FOREIGN KEY carerId REFERENCES User
);

CREATE TABLE User (
  userId SERIAL PRIMARY KEY
);

CREATE TABLE Patient (
  userId SERIAL PRIMARY KEY,
  username CHAR(100) NOT NULL,
  email CHAR(100) NOT NULL,
);

CREATE TABLE Carer (
  userId SERIAL PRIMARY KEY,
  username CHAR(100) NOT NULL,
  email CHAR(100) NOT NULL
);

CREATE TABLE Password (
  userId INTEGER PRIMARY KEY,
  password CHAR(100) NOT NULL
  FOREIGN KEY (userId) REFERENCES User
);

CREATE TABLE Prescription (
  userId INTEGER {FK},
  medicationId INTEGER {FK},
  dosage CHAR(100),
  frequency CHAR(100),
  PRIMARY KEY(userId, medicationId, dosage)
);

CREATE TABLE Medication (
  medicationId SERIAL PRIMARY KEY,
  medicationName CHAR(100) NOT NULL,
  description TEXT,
  imageLink CHAR(100)
);

CREATE TABLE Assignment (
  patientId INTEGER {FK},
  carerId INTEGER {FK},
  PRIMARY KEY(patientId, carerId)
);

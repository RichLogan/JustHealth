CREATE TABLE Client (
  username CHAR(25),
  email CHAR(100) NOT NULL UNIQUE,
  verified BOOLEAN NOT NULL DEFAULT FALSE,
  accountLocked BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(username)
);

CREATE TABLE uq8LnAWi7D (
  recordId SERIAL,
  username CHAR(25) NOT NULL,
  password CHAR(255) NOT NULL,
  isCurrent BOOLEAN,
  expiryDate DATE,
  PRIMARY KEY(recordId),
  FOREIGN KEY(username) REFERENCES Client(username) ON DELETE CASCADE
);

CREATE TABLE Prescription (
  username CHAR(25),
  medicationId INTEGER,
  dosage CHAR(100),
  dosageUnit CHAR(100),
  frequency CHAR(100),
  frequencyUnit CHAR(100),
  PRIMARY KEY (username, medicationId, dosage, dosageUnit)
  FOREIGN KEY username REFERENCES Client(username),
  FOREIGN KEY medicationId REFERENCES Medication(medicationId)
);

CREATE TABLE Medication (
  medicationId SERIAL,
  medicationName CHAR(100) NOT NULL,
  description TEXT,
  imageLink CHAR(100),
  PRIMARY KEY (medicationId)
);

CREATE TABLE Assignment (
  patientUsername INTEGER,
  carerUsername INTEGER,
  PRIMARY KEY (patientUsername, carerUsername),
  FOREIGN KEY patientUsername REFERENCES Client(username),
  FOREIGN KEY carerId REFERENCES Client(username)
);

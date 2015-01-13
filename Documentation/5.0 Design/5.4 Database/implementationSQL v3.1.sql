DROP TABLE Client CASCADE; 
DROP TABLE Patient CASCADE; 
DROP TABLE Carer CASCADE; 
DROP TABLE uq8LnAWi7D CASCADE; 
DROP TABLE deactivateReason CASCADE; 
DROP TABLE userDeactivateReason CASCADE; 
DROP TABLE Connection CASCADE; 

CREATE TABLE Client (
  username VARCHAR(25),
  email VARCHAR(100) NOT NULL UNIQUE,
  dob DATE NOT NULL,
  verified BOOLEAN NOT NULL DEFAULT FALSE,
  accountLocked BOOLEAN NOT NULL DEFAULT FALSE,
  loginattempts INTEGER NOT NULL DEFAULT 0,
  accountdeactivated BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(username)
);

CREATE TABLE Carer (
  username VARCHAR(25) NOT NULL,
  firstname VARCHAR(100) NOT NULL,
  surname VARCHAR(100) NOT NULL,
  ismale BOOLEAN NOT NULL,
  nhscarer BOOLEAN,
  FOREIGN KEY(username) REFERENCES Client(username) ON DELETE CASCADE
);

CREATE TABLE Patient (
  username VARCHAR(25) NOT NULL,
  firstname VARCHAR(100) NOT NULL,
  surname VARCHAR(100) NOT NULL,
  ismale BOOLEAN NOT NULL,
  FOREIGN KEY(username) REFERENCES Client(username) ON DELETE CASCADE
);


CREATE TABLE uq8LnAWi7D (
  username VARCHAR(25) NOT NULL,
  password VARCHAR(255) NOT NULL,
  isCurrent BOOLEAN,
  expiryDate DATE,
  PRIMARY KEY(username, password),
  FOREIGN KEY(username) REFERENCES Client(username) ON DELETE CASCADE
);

CREATE TABLE deactivateReason (
  reason VARCHAR(255),
  primary key (reason)
); 
 
 CREATE TABLE userDeactivateReason (
  id SERIAL,
  reason VARCHAR(255),
  comments VARCHAR (1000),
  primary key (id),
  foreign key (reason) references deactivateReason(reason)
);

CREATE TABLE Relationship (
  connectionid SERIAL PRIMARY KEY,
  requestor VARCHAR(25) REFERENCES Client(username),
  requestorType VARCHAR(50),
  target VARCHAR(25) REFERENCES Client(username),
  targetType VARCHAR(50),
  code INTEGER
);

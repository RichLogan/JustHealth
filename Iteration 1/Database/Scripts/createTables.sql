DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS uq8LnAWi7D;

CREATE TABLE Client (
  username CHAR(25),
  email CHAR(100) NOT NULL UNIQUE,
  verified BOOLEAN NOT NULL DEFAULT FALSE, 	
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
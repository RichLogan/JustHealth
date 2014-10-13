DROP TABLE IF EXISTS Client CASCADE;
DROP TABLE IF EXISTS uq8LnAWi7D CASCADE;

CREATE TABLE Client (
  username CHAR(25),
  firstName CHAR(100) NOT NULL,
  surname CHAR(100) NOT NULL,
  dob DATE NOT NULL,
  isMale BOOLEAN NOT NULL,
  isCarer BOOLEAN NOT NULL,
  email CHAR(100) NOT NULL UNIQUE,
  verified BOOLEAN NOT NULL DEFAULT FALSE,
  accountLocked BOOLEAN NOT NULL DEFAULT FALSE,
  loginattempts int NOT NULL DEFAULT 0,
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

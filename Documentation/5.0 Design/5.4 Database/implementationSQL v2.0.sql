CREATE TABLE Client (
  username CHAR(25),
  email CHAR(100) NOT NULL UNIQUE,
  dob DATE NOT NULL,
  verified BOOLEAN NOT NULL DEFAULT FALSE,
  accountLocked BOOLEAN NOT NULL DEFAULT FALSE,
  loginattempts INTEGER NOT NULL DEFAULT 0,
  accountdeactivated BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY(username)
);

CREATE TABLE Carer (
  username CHAR(25) NOT NULL,
  firstname CHAR(100) NOT NULL,
  surname CHAR(100) NOT NULL,
  ismale BOOLEAN NOT NULL,
  nhscarer BOOLEAN,
  FOREIGN KEY(username) REFERENCES Client(username) ON DELETE CASCADE
);

CREATE TABLE Patient (
  username CHAR(25) NOT NULL,
  firstname CHAR(100) NOT NULL,
  surname CHAR(100) NOT NULL,
  ismale BOOLEAN NOT NULL,
  FOREIGN KEY(username) REFERENCES Client(username) ON DELETE CASCADE
);


CREATE TABLE uq8LnAWi7D (
  username CHAR(25) NOT NULL,
  password CHAR(255) NOT NULL,
  isCurrent BOOLEAN,
  expiryDate DATE,
  PRIMARY KEY(username, password),
  FOREIGN KEY(username) REFERENCES Client(username) ON DELETE CASCADE
);

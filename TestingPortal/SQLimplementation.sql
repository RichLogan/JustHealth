CREATE TABLE Users (
  name CHAR(100),
  role CHAR(100),
  PRIMARY KEY(name)
);

CREATE TABLE Tests (
  iteration INTEGER NOT NULL UNIQUE,
  testid INTEGER NOT NULL UNIQUE,
  applicationType CHAR(50) NOT NULL,
  author CHAR(100) NOT NULL,
  testname CHAR(1000) NOT NULL,
  prerequisites CHAR(10000),
  teststeps CHAR(10000) NOT NULL,
  expectedresults CHAR(10000) NOT NULL,
  PRIMARY KEY (iteration, testid),
  FOREIGN KEY (author) REFERENCES Users(name) ON DELETE NO ACTION
);

CREATE TABLE Run (
  runid INTEGER NOT NULL UNIQUE,
  iteration INTEGER NOT NULL UNIQUE,
  testid INTEGER NOT NULL UNIQUE,
  tester CHAR(100) NOT NULL,
  datetime timestamp NOT NULL,
  actualresult CHAR(50) NOT NULL,
  comments CHAR(10000),
  issue INTEGER,
  FOREIGN KEY(testid) REFERENCES Tests(testid) ON DELETE CASCADE,
  FOREIGN KEY(iteration) REFERENCES Tests(iteration) ON DELETE CASCADE,
  FOREIGN KEY (tester) REFERENCES Users(name) ON DELETE NO ACTION,
  PRIMARY KEY (runid, iteration, testid)
);

CREATE TABLE TestRuns (
  iteration INTEGER NOT NULL,
  testid INTEGER NOT NULL,
  runid INTEGER NOT NULL, 
  PRIMARY KEY (runid, testid, iteration),
  FOREIGN KEY (runid) REFERENCES Run(runid) ON DELETE CASCADE,
  FOREIGN KEY (testid) REFERENCES Tests(testid) ON DELETE CASCADE,
  FOREIGN KEY (iteration) REFERENCES Tests(iteration) ON DELETE CASCADE
);
CREATE TABLE Users (
  name CHAR(100),
  role CHAR(100),
  PRIMARY KEY(name)
);

CREATE TABLE Tests (
  autoid_test SERIAL UNIQUE NOT NULL,
  iteration INTEGER NOT NULL,
  testid INTEGER NOT NULL,
  applicationType CHAR(50) NOT NULL,
  author CHAR(100) NOT NULL,
  testname CHAR(1000) NOT NULL,
  prerequisites CHAR(10000),
  teststeps CHAR(10000) NOT NULL,
  expectedresults CHAR(10000) NOT NULL,
  PRIMARY KEY (iteration, testid),
  FOREIGN KEY (author) REFERENCES Users(name) ON DELETE RESTRICT
);

CREATE TABLE Run (
  autoid_run SERIAL,
  runid INTEGER NOT NULL,
  tester CHAR(100) NOT NULL,
  datetime timestamp NOT NULL,
  actualresult CHAR(50) NOT NULL,
  comments CHAR(10000),
  issue INTEGER,
  autoid_test INTEGER NOT NULL,
  FOREIGN KEY(autoid_tests) REFERENCES Tests(autoid_test) ON DELETE CASCADE,
  FOREIGN KEY (tester) REFERENCES Users(name) ON DELETE RESTRICT,
  PRIMARY KEY (autoid_run)
);

CREATE TABLE TestRuns (
  autoid_run INTEGER NOT NULL,
  autoid_test INTEGER NOT NULL,
  FOREIGN KEY (autoid_run) REFERENCES Run(autoid_run) ON DELETE CASCADE,
  FOREIGN KEY (autoid_test) REFERENCES Tests(autoid_test) ON DELETE CASCADE
);
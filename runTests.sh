#!/bin/bash

# About
# This should run all tests and give results. It will also automatically alter API in order to point to the database, and change back when finshed.

# Usage
# Run using '$ . runTests.sh'
# Must be on kent.ac.uk network
# Line 5 in Website/justHealthServer/api.py !!!MUST!!! be the database import

# Results
# . = PASS
# F = Fail
# E = Error

function getImport {
  sed '5q;d' Website/justHealthServer/api.py
}

importStatement=`getImport`;

echo -e "-------------------------Setup-------------------------"

if [[ $importStatement == "from database import *" ]];  then
  sed -i "" -e "5s/.*/from testDatabase import */" Website/justHealthServer/api.py;
  echo "Application now pointing to TEST database"

  echo "Allowing server to restart..."
  sleep 1
  echo -ne "..1.."\\r
  sleep 1
  echo -ne "..1..2"\\r
  sleep 1
  echo -ne "..1..2..3"\\r
  sleep 1
  echo -ne "..1..2..3..4"\\r
  sleep 1
  echo -e "..1..2..3..4..5"\\r
  echo "Done!"
  runTests
elif [[ $importStatement == "from testDatabase import *" ]]; then
  echo "Application already pointing to TEST database";
  runTests
else
  echo "Something went wrong. Check DB import statement of Website/justHealthServer/api.py";
fi

echo "Reverting application to PRODUCTION database"
sed -i "" -e "5s/.*/from database import */" Website/justHealthServer/api.py;

function runTests {
  echo -e "---------------Just Health Testing Suite---------------"

  echo "Iteration 1"
  # python -m unittest discover Iteration\ 1/Test\ Cases/Testing\ Scripts/
  echo -e "\n"

  echo "Iteration 2"
  # testPath
  echo -e "\n"

  echo "Iteration 3"
  # testPath
  echo -e "\n"

  echo "Iteration 4"
  python -m unittest -v discover Iteration\ 4/Test\ Cases/
  echo -e "\n"
}

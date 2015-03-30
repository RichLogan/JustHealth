#!/bin/bash

# About
# This should run all tests and give results. It will also automatically alter the local server in order to point to the database, and change back when finshed.
# More detailed output can be added by appending -v to the test in question

# Usage
# Run using '$ . runTests.sh'
# Must be on kent.ac.uk network
# Line 5 in Website/justHealthServer/api.py !!!MUST!!! be the database import

# Results
# . = PASS
# F = Fail
# E = Error

function getImportAPI {
  sed '5q;d' Website/justHealthServer/api.py
}

function getImportGCM {
  sed '2q;d' Website/justHealthServer/gcm.py
}

importStatementAPI=`getImportAPI`;
importStatementGCM=`getImportGCM`;

echo -e "-------------------------Setup-------------------------"

if [[ $importStatementAPI == "from database import *" ]];  then
  sed -i "" -e "5s/.*/from testDatabase import */" Website/justHealthServer/api.py;
  echo "API now pointing to TEST database"
  if [[ $importStatementGCM == "from database import *" ]];  then
    sed -i "" -e "2s/.*/from testDatabase import */" Website/justHealthServer/gcm.py;
    echo "GCM now pointing to TEST database"

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

  elif [[ $importStatement == "from testDatabase import *" ]]; then
    echo "Application already pointing to TEST database";
    runTests
  else
    echo "Something went wrong. Check DB import statement of Website/justHealthServer/gcm.py";
  fi
  echo "Reverting application to PRODUCTION database"
  sed -i "" -e "5s/.*/from database import */" Website/justHealthServer/api.py;
  sed -i "" -e "2s/.*/from database import */" Website/justHealthServer/gcm.py;

elif [[ $importStatement == "from testDatabase import *" ]]; then
echo "Application already pointing to TEST database";
runTests

elif [[ $importStatement == "from testDatabase import *" ]]; then
  echo "Application already pointing to TEST database";
  runTests
else
  echo "Something went wrong. Check DB import statement of Website/justHealthServer/api.py";
fi

echo "Reverting application to PRODUCTION database"
sed -i "" -e "5s/.*/from database import */" Website/justHealthServer/api.py;
sed -i "" -e "2s/.*/from database import */" Website/justHealthServer/gcm.py;

function runTests {
  echo -e "---------------Just Health Testing Suite---------------"

  # echo "Iteration 1"
  # python -m unittest discover Iteration\ 1/Test\ Cases/Testing\ Scripts/
  # echo -e "\n"

  # echo "Iteration 2"
  # # testPath
  # echo -e "\n"

  # echo "Iteration 3"
  # # testPath
  # echo -e "\n"

  # echo "Iteration 4"
  # echo "--"
  #   echo "Search Patient Carer"
  #   python -m unittest discover Iteration\ 4/Test\ Cases/ testSearchPatientCarer.py
  
  #   echo "Create Connection"
  #   python -m unittest discover Iteration\ 4/Test\ Cases/ testCreateConnection.py
    
  #   # echo "Complete Connection"
  #   # python -m unittest discover Iteration\ 4/Test\ Cases/ testCompleteConnection.py
    
  #   # echo "Delete Connection"
  #   # python -m unittest discover Iteration\ 4/Test\ Cases/ testDeleteConnection.py
    
  #   # echo "Cancel Connection"
  #   # python -m unittest discover Iteration\ 4/Test\ Cases/ testCancelConnection.py
    
  #   # echo "Get Connections"
  #   # python -m unittest discover Iteration\ 4/Test\ Cases/ testGetConnections.py
  # echo -e "\n"

  # echo "Iteration 5"
  # python -m unittest discover Iteration\ 5/Test\ Cases/
  # echo -e "\n"
  
  echo "Iteration 8"
  echo "--"
    echo "Test Get Notifications"
    python -m unittest discover Iteration\ 8/TestCases/ testGetNotifications.py -v
}
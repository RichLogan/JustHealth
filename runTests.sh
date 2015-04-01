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

  echo -e "\n"
  echo -e "Running against local server: http://127.0.0.1:9999"
  echo -e "\n"

  echo -e "For verbose output, please append tests run with -v"
  echo -e "\n"
  echo -e "Results will be shown as:"
  echo -e ". = Pass"
  echo -e "F = Fail"
  echo -e "E = Error"

  echo -e "\n"

  echo -e "======================================================================"
  echo "Iteration 4"
  echo -e "======================================================================"

    echo "Authentication"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testAuthentication.py
    echo -e "\n"

    echo "Cancel Connection"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testCancelConnection.py
    echo -e "\n"

    echo "Complete Connection"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testCompleteConnection.py
    echo -e "\n"

    echo "Create Connection"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testCreateConnection.py
    echo -e "\n"

    echo "Deactivate Account"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testDeactivateAccount.py
    echo -e "\n"

    echo "Delete Connection"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testDeleteConnection.py
    echo -e "\n"

    echo "Get Account Info"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testGetAccountInfo.py
    echo -e "\n"

    echo "Get Connections"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testGetConnections.py
    echo -e "\n"

    echo "Registration"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testRegistration.py
    echo -e "\n"

    echo "Search Patient Carer"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 4/Test\ Cases/ testSearchPatientCarer.py
    echo -e "\n"

  echo -e "======================================================================"
  echo "Iteration 5"
  echo -e "======================================================================"

    echo "Add Appointments"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 5/Test\ Cases/ testAddAppointments.py
    echo -e "\n"

    echo "Add Medication"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 5/Test\ Cases/ testAddMedication.py
    echo -e "\n"

    echo "Add Prescription"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 5/Test\ Cases/ testAddPrescription.py
    echo -e "\n"

    echo "Delete Appointment"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 5/Test\ Cases/ testDeleteAppointments.py
    echo -e "\n"

    echo "Delete Medication"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 5/Test\ Cases/ testDeleteMedication.py
    echo -e "\n"

    echo "Delete Prescription"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 5/Test\ Cases/ testDeletePrescription.py
    echo -e "\n"
    
    echo "Get Appointment"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 5/Test\ Cases/ testGetAppointments.py
    echo -e "\n"

    echo "Get Prescriptions"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 5/Test\ Cases/ testGetPrescriptions.py
    echo -e "\n"

  echo -e "======================================================================"
  echo "Iteration 8"
  echo -e "======================================================================"

    echo "Get Notifications"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testGetNotifications.py
    echo -e "\n"

    echo "Add Reminders"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testAddReminders.py
    echo -e "\n"

    echo "Create Notification"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testCreateNotification.py
    echo -e "\n"
    
    echo "Create Prescription Instances"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testCreatePrescriptionInstances.py
    echo -e "\n"
    
    echo "Delete Reminders"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testDeleteReminders.py
    echo -e "\n"

    echo "Dismiss Notifications"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testDimissNotification.py
    echo -e "\n"

    echo "Get appointments due in 30 minutes"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testGetAppointmentsDueIn30.py
    echo -e "\n"

    echo "Get appointments due now"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testGetAppointmentsDueNow.py
    echo -e "\n"

    echo "Get minutes difference"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testGetMinutesDifference.py
    echo -e "\n"

    echo "Get Missed Prescriptions"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testGetMissedPrescriptions.py
    echo -e "\n"

    echo "Get Prescriptions Due Today"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testGetPrescriptionDueToday.py
    echo -e "\n"

    echo "Get Reminders"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 8/TestCases/ testGetReminders.py 
    echo -e "\n"

  echo -e "======================================================================"
  echo "Iteration 9"
  echo -e "======================================================================"

    echo "Add Correspondence"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 9/Test\ Cases/ testAddCorrespondence.py 
    echo -e "\n"

    echo "Check Stock Level"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 9/Test\ Cases/ testCheckStockLevel.py
    echo -e "\n"

    echo "Delete Note"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 9/Test\ Cases/ testDeleteNote.py
    echo -e "\n"

    echo "Get Correspondence"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 9/Test\ Cases/ testGetCorrespondence.py
    echo -e "\n"

    echo "Get Patient Notes"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 9/Test\ Cases/ testGetPatientNotes.py
    echo -e "\n"

    echo "Get Prescription Count"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 9/Test\ Cases/ testGetPrescriptionCount.py
    echo -e "\n"

    echo "Take Prescription"
    python -m unittest discover Iteration\ Specific\ Plans/Iteration\ 9/Test\ Cases/ testTakePrescription.py
    echo -e "\n"
}

# JustHealth

JustHealth is a University of Kent Final Year Project (CO600). 

The authors have developed a platform for facilitating the connection between patients with long term health conditions, and their carers. 

Comprehensive documentation can be found at the following places:

- Examiner's Guide
- User Documentation
- Technical Documentation
- Corpus Index

The Web application is running at http://raptor.kent.ac.uk:5000

If you'd like to run it locally (for example to run the runTests.sh script) you can do so by navigating to /Website and running 
```bash
$ pip install -r requirements.txt
```

to install dependencies and then

```bash
python runServer.py
```

to actually run the application. You must be connected to the Kent network (or through VPN) in order to reach the database.

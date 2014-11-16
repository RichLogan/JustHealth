from flask import Flask, render_template, request, redirect, url_for
from database import *
from time import ctime
app = Flask(__name__)

@app.route('/query', methods=['POST', 'GET'])
def query():
	if request.method == 'POST':
		#seach tests based on iteration number
		buildQuery = {}
		buildQuery['iteration'] = request.form['iteration']

		testsQueried = Tests.select().where(Tests.iteration == buildQuery['iteration']).order_by(Tests.testid)

		return render_template('queryTests.html', tests = testsQueried)

	elif request.method == "GET":
		buildQuery = {}
		buildQuery['iteration'] = request.args.get('iteration')

		return render_template('queryTests.html', tests = Tests.select().where(Tests.iteration == buildQuery['iteration']))

	return render_template('queryTests.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
	if request.method == 'POST':
		createTest = {}
		createTest['iteration'] = request.form['iteration']
		createTest['author'] = request.form['author']
		createTest['applicationType'] = request.form['testType']
		createTest['testname'] = request.form['testname']
		createTest['prerequisites'] = request.form['prerequisites']
		createTest['teststeps'] = request.form['testSteps']
		createTest['expectedresults'] = request.form['expectedOutcome']
		try :
			latestTest = Tests.select(Tests.testid).where(Tests.iteration==request.form['iteration']).order_by(Tests.testid.desc()).get()
			latestTestId = latestTest.testid + 1
		except Tests.DoesNotExist, e: 
			latestTestId = 1

		createATest = Tests.insert(
			iteration = createTest['iteration'],
			testid = latestTestId,
			applicationtype = createTest['applicationType'],
			author = createTest['author'],
			testname = createTest['testname'],
			prerequisites = createTest['prerequisites'],
			teststeps = createTest['teststeps'],
			expectedresults = createTest['expectedresults'])

		createATest.execute();
		return render_template('createTest.html', message="Test case has been created, thank you.")
	return render_template('createTest.html')


#loads the run test screen
@app.route('/run', methods=['POST', 'GET'])
def runTest():
	if request.method == 'GET':
		return render_template('runTest.html', test = Tests.select().where(Tests.autoid_test == request.args.get('test')).get())

@app.route('/updateTest',  methods=['POST', 'GET'])
def updateTest():
	if request.method == 'POST':
		updateTest = {}
		updateTest['autoid_test'] = request.form['autoid_test']
		updateTest['iteration'] = request.form['iteration']
		updateTest['author']= request.form['author']
		updateTest['applicationtype'] = request.form['testType']
		updateTest['testname'] = request.form['testname']
		updateTest['prerequisites'] = request.form['prerequisites']
		updateTest['teststeps'] = request.form['testSteps']
		updateTest['expectedresults'] = request.form['expectedOutcome']
		
		update = Tests.update ( 
			iteration = updateTest['iteration'],
			author = updateTest['author'],
			applicationtype = updateTest['applicationtype'],
			testname = updateTest['testname'],
			prerequisites = updateTest['prerequisites'],
			teststeps = updateTest['teststeps'],
			expectedresults = updateTest['expectedresults']
		).where ( 
			Tests.autoid_test == updateTest['autoid_test']
		)

		update.execute()

	return render_template('queryTests.html', message = 'Test updated.')
	

#loads the edit test screen
@app.route('/edit', methods=['POST', 'GET'])
def editTest():
	if request.method == 'GET':
		return render_template('editTest.html', test = Tests.select().where(Tests.autoid_test == request.args.get('test')).get())
	


#when a test run is submitted 
@app.route('/submitTest', methods=['POST', 'GET'])
def submitTest():
	submitTest = {}
	submitTest['actualresult'] = request.form['actualresult']
	submitTest['autoid_test'] = request.args.get('test')
	submitTest['comments'] = request.form['comments']
	submitTest['datetime'] = ctime()	
	submitTest['issue'] = request.form['issue']
	submitTest['tester'] = request.form['tester']

	#checks that the issue isn't blank
	if submitTest['issue'] == "" :
		submitTest['issue'] = None 

	#finds which run this should be 
	try:
		findRunNumber = Run.select(Run.runid).where(Run.autoid_test==submitTest['autoid_test']).order_by(Run.runid.desc()).get()
		runNumber = findRunNumber.runid + 1
	except Run.DoesNotExist, e:
		runNumber = 1

	submitTest['runid'] = runNumber
	
	#inserts the new test run into db
	createRun = Run.insert(
		actualresult = submitTest['actualresult'],
		autoid_test = submitTest['autoid_test'],
		comments = submitTest['comments'],
		datetime = submitTest['datetime'],
		issue = submitTest['issue'],
		tester = submitTest['tester'],
		runid = submitTest['runid']
	)

	#updates the latestresult field in the Tests table 
	updateLatestResult = Tests.update(
		latesttestresult = submitTest['actualresult']
		).where(Tests.autoid_test==submitTest['autoid_test']
	)
	
	createRun.execute()
	updateLatestResult.execute()

	#attempting to reload query tests on showing the tests that are in the same iteration as the test that has just been run
	findTest = Tests.select().join(Run).where(Run.autoid_test==submitTest['autoid_test']).get()
	findIteration = str(findTest.iteration)

	return render_template('queryTests.html', test=findIteration, message="Running of the test has been recorded, thank you.")


@app.route('/portal')
def portalHome():
  return render_template('portalHome.html')





if __name__ == "__main__":
  app.run(port=9999, debug=True)
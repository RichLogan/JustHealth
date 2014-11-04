from flask import Flask, render_template, request, redirect, url_for
from database import *
app = Flask(__name__)

@app.route('/query', methods=['POST', 'GET'])
def query():
	if request.method == 'POST':
		buildQuery = {}
		buildQuery['iteration'] = request.form['iteration']

		return render_template('queryTests.html', tests = Tests.select().where(Tests.iteration == buildQuery['iteration']))
		# except Tests.DoesNotExist, e:
		# 	return "No tests found."

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
		return "Test Created"
	return render_template('createTest.html')


@app.route('/run', methods=['POST', 'GET'])
def runTest():
	if request.method == 'GET':
		return render_template('runTest.html', test = Tests.select().where(Tests.autoid_test == request.args.get('test')).get())



@app.route('/portal')
def portalHome():
  return render_template('portalHome.html')





if __name__ == "__main__":
  app.run(port=9999, debug=True)
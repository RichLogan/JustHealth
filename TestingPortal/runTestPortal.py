from flask import Flask, render_template
app = Flask(__name__)

@app.route('/query')
def query():
  return render_template('queryTests.html')

@app.route('/create')
def create():
  return render_template('createTest.html')

@app.route('/portal')
def portalHome():
  return render_template('portalHome.html')

if __name__ == "__main__":
  app.run(port=9999, debug=True)
import flask
from flask import render_template,request
import json
import sys

app= flask.Flask(__name__)

@app.route('/')
def homePage():
    return render_template('homePage.html')

@app.route('/data')
def dataPage():
    return render_template('dataPage.html')

# @app.route('/hostSearch')
# def hostSearch():
#     return render_template('hostPage.html')

@app.route('/hostSearch',methods = ['POST', 'GET'])
def hostSearch():
   if request.method == 'POST':
      result = request.form
      print(result)

@app.route('/hostResult')
def hostResult():
    return render_template('hostResult.html')

if __name__=='__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()
    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)

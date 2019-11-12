import flask
from flask import render_template,request
import json
import sys
sys.path.append('../Backend/')
from datasource import *

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

@app.route('/hostSearch')
def hostSearch():
   return render_template('hostPage.html')

@app.route('/hostResult',methods = ['POST', 'GET'])
def hostResult():
    if request.method == 'POST':
        result = request.form
        db = DataSource()
        db.connect('qine', 'ruby434seal')
        host_id = result['id']
        host_info = db.getHostInfo(host_id)
        return render_template('hostResult.html',results=host_info)

@app.route('/overall')
def overall():
    return render_template('overallPage.html')

if __name__=='__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()
    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)

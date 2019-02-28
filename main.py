from flask import Flask, render_template,redirect,url_for,request
import cx_Oracle

from flask_sqlalchemy import SQLAlchemy
connstr = 'HRMS/HRMS@127.0.0.1:1521/ORCL'
conn = cx_Oracle.connect(connstr)
curs = conn.cursor()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=conn.cursor()
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
@app.before_first_request
def create_tables():
    db.create_all()

import models

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')  # render a template@app.route('/index.html')

@app.route('/project/create',methods=['POST'])
def AddNewProject():
    title=request.form['title']
    description=request.form['description']
    startDate=request.form['startDate']
    endDate=request.form['endDate']
    status=request.form['status']
    project=models.ProjectModel(title=title,description=description,startDate=startDate,endDate=endDate,status=status)
    project.create_record()

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(port=5001,debug=True)

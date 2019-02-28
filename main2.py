import cx_Oracle
from flask import Flask, render_template, request, url_for, redirect,flash
from models import ProjectModel
import pygal
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = cx_Oracle.connect("HRMS/HRMS@127.0.0.1:1521/ORCL")
cursor = db.cursor()
# app.config['SECRET_KEY'] = 'd369342136ecd032f8b4a930b6bb2e0e'

@app.route('/', methods=['GET'])
def home():
    cursor.arraysize = 50
    cursor.execute( 'SELECT * from projects')
    records = cursor.fetchall()
    print(records)
    return render_template('index.html',records = records)  # render a template@app.route('/index.html')


@app.route('/project/create', methods=['POST'])
def edited():

    title = request.form['title']
    description = request.form['description']
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    p_cost = request.form['cost']
    status = request.form['status']
    execute = """INSERT INTO projects(title,description,startdate,enddate,p_cost,status) VALUES
            (:title,:description, :startDate, :endDate,:cost,:status)"""
    cursor.execute(execute, {'title': title, 'description': description, 'startDate': startDate, 'endDate': endDate,
                             'cost': p_cost, 'status': status})
    db.commit()
def home():
    status_rec=cursor.fetchall()
    status=[x.status for x in status_rec]
    print(status)
    pie_chart = pygal.Pie()
    pie_chart.title ="completed vs pending projects"
    pie_chart.add("pending projects",status.count("Pending"))
    pie_chart.add("completed projects",status.count("completed"))
    pie_chart.render()
    graph=pie_chart.render_data_uri()





@app.route('/', methods=['POST'])
def add_data():

    return render_template('index.html')

@app.route('/projects/create', methods=['GET', 'POST'])
def post_data():
    flash("Record inserted successfully.....")

@app.route('/project/edit/<int:id>',methods=['POST'])
def editproject(id):
    newTitle=request.form['title']
    newDescription=request.form['description']
    newStartdate=request.form['startdate']
    newEnddate=request.form['enddate']
    newCost=request.form['p_cost']
    newStatus=request.form['status']
    updated=ProjectModel.update_by_id(id=id,newTitle=newTitle,newDescription=newDescription,newStartdate=newStartdate,
                                            newEnddate=newEnddate,newCost=newCost,newStatus=newStatus)

    if updated:
        flash("Updated Successfully")
        return redirect(url_for('home'))
    else:
        flash("No records found")
        return redirect(url_for('home'))

# @app.route('/project/delete/<int.id>',method=['POST'])
# def deletepreoject(id):
#     delete=models.ProjectModel.deleteBy

if __name__ == "__main__":
    app.run(host='localhost', port=8000, debug=True)

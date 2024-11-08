from flask import Flask, render_template, request, redirect, abort
from models import db, EmployeeModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///armazenamento.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_table():
    db.create_all()

@app.route('/armazenamento/create', methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position = position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/armazenamento')    

@app.route('/armazenamento')
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html', employees = employees)

@app.route('/armazenamento/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee = employee)
    return f"Employee with id ={id} Doesn't exist"

@app.route('/armazenamento/<int:id>/update',methods = ['GET','POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id, name=name, age=age, position = position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/armazenamento/{id}')
        return f"Employee with id = {id} Doesn't exist"
    return render_template('update.html', employee = employee)

@app.route('/armazenamento/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()

    if not employee:
         return f"Employee with id {id} does not exist.", 404
    
    if request.method == 'POST':
            db.session.delete(employee)
            db.session.commit()
            return redirect('/armazenamento')

    return render_template('delete.html', employee=employee)

app.run(host='localhost', port=5000)
from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_user

from models import Employee, Department

def register_routes(app, db):

    @app.before_request
    def create_tables():
        db.create_all()

    @app.route('/departments', methods=['GET'])
    def get_departments():
        departments = Department.query.all()
        return jsonify([department.serialize() for department in departments])
        # return employee

    @app.route('/admin', methods=['GET', 'POST'])
    def createadmin():
        # data = request.json
        # first_name = 'tega'
        # last_name = 'ali'
        # email = 't217g@gmail.com'
        # phone = '0288082082'
        # password = 'squid'
        # is_admin = True

        # new_employee = Employee(first_name=first_name, last_name=last_name, email=email,is_admin=is_admin, phone=phone)
        # new_employee.set_password(password)

        # db.session.add(new_employee)
        # db.session.commit()

        
        # return redirect(url_for('employees'))

        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        position = data.get('position')
        department_id = data.get('department_id')

        print(data)
        new_employee = Employee(first_name=first_name, last_name=last_name, email=email, department_id=department_id, phone=phone, role_id=1)
        new_employee.set_password(password)

        if new_employee:
            db.session.add(new_employee)
            db.session.commit()
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'failed'})
        
        
        # return jsonify(new_employee.serialize())
        
    
    # @app.route('/employees', methods=['POST'])
    # def create_employee():
        data = request.json
        first_name = data.get('name')
        last_name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        position = data.get('position')
        department = data.get('department')

        new_employee = Employee(first_namename=first_name, last_name=last_name, email=email, position=position, department_id=1, phone=phone, roles=1)
        new_employee.set_password(password)

        db.session.add(new_employee)
        db.session.commit()
        return jsonify(new_employee.serialize())

    @app.route('/employees', methods=['GET'])
    def get_employees():
        employees = Employee.query.all()
        return jsonify([employee.serialize() for employee in employees])
        # return employees

    @app.route('/employees/<int:employee_id>', methods=['GET', 'PUT', 'DELETE'])
    def employee_detail(employee_id):
        # data = request.json
        employee = Employee.query.get_or_404(employee_id)
        # password = data.get('password')
        # print(password)
        if request.method == 'GET':
            return jsonify(employee.serialize())
        elif request.method == 'PUT':
            data = request.json
            password = data.get('password')
            employee = Employee.query.get_or_404(employee_id)
            employee.first_name = data.get('first_name', employee.first_name)
            employee.last_name = data.get('last_name', employee.last_name)
            employee.email = data.get('email', employee.email)
            employee.phone = data.get('phone', employee.phone)
            employee.department_id = data.get('department_id', employee.department_id)
            if password :
                employee.set_password(password)
            db.session.commit()
            return jsonify(employee.serialize())
        elif request.method == 'DELETE':
            db.session.delete(employee)
            db.session.commit()
            return jsonify({'message': 'success'})
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.json
            # email = 'teg@gmail.com'
            email = data.get('email')
            password = data.get('password')

            # find the employee by email
            # print(data)
            employee = Employee.query.filter_by(email=email).first()

            if employee:
                login_user(employee)
                flash('Login successfull')
                return jsonify([employee.serialize()])
                # return redirect(url_for('dashborad'))
                # return jsonify({'message': 'login faled'})
            else: 
                flash('Invalid email or password')
                return 'failed'
        return jsonify({'message': 'login faile'})
            
                
            
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            data = request.form
            first_name = data.get('name')
            last_name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')
            position = data.get('position')
            department = data.get('department')

            if Employee.query.filter_by(email=email).first():
                flash('Email already registered.', 'danger')
                return redirect(url_for('register'))
            
            new_employee = Employee(first_namename=first_name, last_name=last_name, email=email, position=position, department=department, phone=phone)
            new_employee.set_password(password)

            db.session.add(new_employee)
            db.session.commit()

            flash('Registration successfull! Please log in.', 'succes')
            return
        




    # @app.route('/', methods=['GET', 'POST'])
    # def index():
    #     if request.method == 'GET':
    #         people = Person.query.all()
    #         return render_template('index.html', people=people)
    #     elif request.method == 'POST':
    #         name = request.form.get('name')
    #         age = int(request.form.get('age'))
    #         job = request.form.get('job')

    #         person = Person(name=name, age=age, job=job)

    #         db.session.add(person)
    #         db.session.commit()

    #         people = Person.query.all()
    #         return render_template('index.html', people=people)
        
    # @app.route('/delete/<pid>', methods=['DELETE'])
    # def delete(pid):
    #     Person.query.filter(Person.pid == pid).delete

    #     db.session.commit()
    #     people = Person.query.all()
    #     return render_template('index.html', people=people)
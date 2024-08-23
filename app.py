from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"


db = SQLAlchemy(app)




class db_attr(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    def __repr__(self):
        return 'db_attr {}'.format(db_attr.sno)
    

with app.app_context():
    db.create_all()



#taking input from the homepage form
@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    
    if request.method=='POST':
        if(request.form['name']=="" or request.form['age']=="" or request.form['role']==""):
            test = db_attr.query.all()
            return render_template('index.html', dbase = test)
        namee = request.form['name']
        agee = request.form['age']
        role = request.form['role']
        dbase = db_attr(name = namee, age = agee, desc = role)
        db.session.add(dbase)
        db.session.commit()
    test = db_attr.query.all()
    print(db_attr)
    return render_template('index.html', dbase = test)




#update entry once the update button is clicked
@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        newE = db_attr.query.filter_by(sno=sno).first()
        newE.name = request.form['name']
        newE.desc = request.form['role']
        newE.age = request.form['age']
        db.session.add(newE)
        db.session.commit()
    return redirect('/')




#delete entry once the delete button is clicked
@app.route('/delete/<int:sno>')
def delete(sno, check = True):
    if check:
        tbDel = db_attr.query.filter_by(sno=sno).first()
        db.session.delete(tbDel)
        db.session.commit()       
        return redirect('/')




#delete all entries at once
@app.route('/delete_all')
def deleteAll():
    #test = db_attr.query.all()
    db_attr.query.delete()
    db.session.commit()
    return redirect('/')




#search entry by name
@app.route('/search', methods = ['GET', 'POST'])
def search():
    t = ''
    if request.method=='POST':
        print(request.form['searched'])
        t = request.form['searched']
    dbase = db_attr.query.filter_by(name=t).all()
    return render_template('search.html', dbase=dbase)




@app.route('/add')
def print_ll():
    dbase = db_attr(name = 'samarth', age = 23, desc = 'SDE PalTech G0')
    db.session.add(dbase)
    db.session.commit()
    return 'added entry {}'.format(dbase.sno)




@app.route('/delete_first/')
def delete_first():
    data = db_attr.query.all()
    if len(data)==0:
        return redirect('/')
    print('was here outside')
    for t in data:
        sno = t.sno
        print('was here and sno = ', sno)
    return redirect('/delete/{}'.format(sno))




@app.route('/updateNow/<int:sno>')
def updateNow(sno):
    return render_template('update.html', test = db_attr.query.filter_by(sno=sno).first())


@app.route('/about/')
def about():
    return 'This is a test project made using Flask'


@app.route('/fun')
def just_for_fun():
    return render_template('test1.html')


@app.route('/fun2')
def hello_world2():
    return 'Hello, World!'


@app.route('/show')
def print_all():
    dbse = db_attr.query.all()
    print(dbse)
    return 'printed, check terminal'


if __name__=="__main__":
    app.run(debug=True)
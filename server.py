from flask import Flask, render_template,request,redirect, flash, session

from user import User
from flask_bcrypt import bcrypt
from flask import app

# bcrypt = bcrypt(app)

app = Flask(__name__)
app.secret_key = "shhhhhh"


@app.route("/")
def auth():
    return render_template("auth.html")


@app.route("/index")
def index():

    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register():
    data = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    data2 = {
        "email" : request.form['email']
    }

    user_in_db = User.check_email(data2)
    if user_in_db:
        flash('Este email ya esta registrado')
        return redirect('/')


    if not User.validate(request.form):
        return redirect('/')
    
    user_id = User.create(data)
    flash('Usuario creado con exito', 'login')
    

    # Guardamos datos en session
    session['user'] = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'id': user_id
        }

    session['user_id'] = user_id

    return redirect("/")



@app.route('/login', methods=['POST'])
def login():

    data = {
        'email' : request.form['email']
    }
    user_in_db = User.check_email(data)
    if not user_in_db:
        flash('usuario no registrado', 'login')
        return redirect('/')

    if not Bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('password incorrecto', 'login')
        return redirect('/')

    flash('Usuario ingresó con éxito', 'info')

    session['user'] = {
        'first_name': user_in_db.first_name,
        'last_name': user_in_db.last_name,
        'email': user_in_db.email,
        'id': user_in_db.id
        }



    return redirect('/index')








if __name__=="__main__":
    app.run(debug=True)

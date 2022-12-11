from flask import Flask,Blueprint, render_template, request, flash, redirect, url_for,Response
from .models import User,Form
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from flask_mail import Mail,Message
from sqlalchemy import DateTime
from datetime import datetime

class UploadFileForm(FlaskForm):
    file = FileField("file", validators=[InputRequired()])
    submit = SubmitField("signup")

app = Flask(__name__)


mail=Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME']= 'petme7062@gmail.com'
app.config['MAIL_PASSWORD']= 'etzuyxaeedsnhfnz'
app.config['MAIL_USE_SSL']= True
mail=Mail(app)







auth = Blueprint('auth', __name__)




@auth.route('/Contact',methods=['POST','GET']) 
def contact() :
    return render_template("contact.html", user=current_user,result="Success!") 

@auth.route('/',methods=['POST','GET']) 
def success() :
    if request.method =="POST" :
        msg= Message(request.form.get("subject") ,sender='petme7062@gmail.com' ,recipients=[request.form.get("email")])
        msg.body=request.form.get("message")
        mail.send(msg)
        return redirect(url_for('views.home'))
    return render_template("index.html", user=current_user,result="Success!")      
    


  





@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.form'))

    return render_template("sign_up.html", user=current_user)
app = Flask(__name__)    
app.config['UPLOAD_FOLDER'] = './static/files'
@auth.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    if request.method == 'POST':
        namepet = request.form.get('namepet')
        favmeal = request.form.get('favmeal')
        Medic = request.form.get('Medic')
        Gender = request.form.get('Gender')
        Contact= request.form.get('Contact')
        pic = request.files['file']
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        form = Form(namepet=namepet,favmeal=favmeal, Medic=Medic,Gender=Gender,Contact=Contact,img=pic.read(), name=filename, mimetype=mimetype )
        db.session.add(form)
        db.session.commit()
        
        
    
            
        # Then save the file
        flash('Form created!', category='success')
        
        return redirect(url_for('views.home'))

                
        
    return render_template("form.html",user=current_user)



@auth.route('/about_us', methods=['GET', 'POST']) 

def about() :
    return render_template('aboutus.html',user=current_user)
        
   

    

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Form,User
from sqlalchemy import desc
from .auth import *

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])

def home():
    posts = Form.query.order_by(desc(Form.date)).all()
    
    
            
    # First grab the file

    
    return render_template("index.html",user=current_user,posts=posts)

@views.route('/<int:id>')
def get_img(id):
    img = Form.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)
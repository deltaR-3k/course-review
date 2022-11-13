from flask import Blueprint,render_template,abort,redirect,url_for,request,abort,jsonify
from flask_login import login_required
from app.models import Program
from app import db

program = Blueprint('program', __name__)

@program.route('/')
def index():
    abort(403)

@program.route('/<int:program_id>/')
def view_program(program_id):
    program = Program.query.filter_by(id=program_id).first()
    if not program:
        abort(404)
    return render_template('program.html', program=program)

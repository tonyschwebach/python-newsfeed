from flask import Blueprint, request,jsonify
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api',__name__,url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  try:
    # create user object from request
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )
    # save to db
    db.add(newUser)
    db.commit()
  except:
    print(sys.exc_info()[0])
    db.rollback()
    return jsonify(message='Signup failed'),500  
  
  return jsonify(id = newUser.id)
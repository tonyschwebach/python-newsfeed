from flask import Blueprint, request,jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys

bp = Blueprint('api',__name__,url_prefix='/api')

# Route for new user
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  try:
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )
    db.add(newUser)
    db.commit()
  except:
    print(sys.exc_info()[0])
    db.rollback()
    return jsonify(message='Signup failed'),500  
  
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True
  return jsonify(id = newUser.id)

@bp.route('users/logout',methods=['POST'])
def logout():
  session.clear()
  return '',204

#  route for user login
@bp.route('/users/login',methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])
    return jsonify(message = 'Incorrect credentials'),400
  
  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'),400

  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True
  return jsonify(id = user.id)

# route for comments
@bp.route('/comments',methods=['POST'])
def comment():
  data = request.get_json()
  db = get_db()

  try:
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id'))
    db.add(newComment)
    db.commit()
  except:
    print(sys.exc_info()[0])
    db.rollback()
    return jsonify(message='Comment failed'),500
  
  return jsonify(id = newComment.id)

# route for upvote
@bp.route('posts/upvote',methods=['PUT'])
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )
    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])
    db.rollback()
    return jsonify(message='Upvote failed'),500
  
  return '',204
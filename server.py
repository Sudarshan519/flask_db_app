import time
from mysqlx import OperationalError
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
# import sshtunnel
app=Flask(__name__)

# tunnel = sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),ssh_username='SudarshanShresth',ssh_password='Asmir123',
#                                       remote_bind_address=('SudarshanShrestha.mysql.pythonanywhere-services.com',3306))

# tunnel.start()
DATABASE_URL_PYTHON ="mysql+mysqlconnector://sudarshanshresth:Asmir123@SudarshanShrestha.mysql.pythonanywhere-services.com/SudarshanShresth$default"#.format(5432)#tunnel.local_bind_port)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_PYTHON
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SQLALCHEMY_POOL_TIMEOUT'] = 300  # For example, set to 30 seconds

db = SQLAlchemy(app)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
# db.create_all()

# Members api route

def wait_for_database(max_attempts=10, interval=5):
    attempts = 0
    while attempts < max_attempts:
        print(attempts)
        try:
            db.session.execute(text('SELECT 1'))
            return True
        except OperationalError:
            attempts += 1
            time.sleep(interval)
    return False

@app.route('/')
def check_database_connection():
    if wait_for_database():
        return 'Database connected successfully!'
    else:
        return 'Failed to connect to the database'

@app.route('/members')
def members():
    return {
        "members":[
          {"name":  "Member1"},
            {"name":  "Member1"},
           {"name":  "Member1"},
        ]
    }
@app.route('/comments/')
def comments():
    comments=Comment.query.all()
    print(comments)
    return comments
    
@app.route('/add-comment')
def add_comment():
    comment=Comment(name='HEllo added')
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
if __name__=="__main__":
    app.run(debug=True)
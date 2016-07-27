import os
import MySQLdb as my
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
host = os.environ.get('HOST')
dbname = os.environ.get('DB')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')


def connect_db():
    db = my.connect(host,user,password,dbname)
    return db

@app.route("/user/list/")
def list_user():
    db = connect_db()
    cursor = db.cursor(my.cursors.DictCursor) 
    cursor.execute("select user_id, user_name, password, email, first_name, last_name from user order by user_id desc")
    users=cursor.fetchall()
    db.close()
    return render_template("table_user.html", users=users)

@app.route("/user/create/getForm/")
def get_create_user_form():
    return render_template("create_user_form.html")

@app.route("/user/create/", methods=['POST'])
def create_user():
    user_name = request.form['user_name']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    print "DEBUG: username=%s, password=%s, email=%s, firstname=%s, lastname=%s" % (user_name, password, email, first_name, last_name)
    type(user_name)
    type(password)
    type(first_name)
    type(last_name)
    type(email)
    params=[user_name, password, email, first_name, last_name]
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO user(user_name, password, email, first_name, last_name) values(%s, %s, %s, %s, %s)", params)
    db.commit()
    db.close()
    #flash("New user created successfully")
    response={"result": "New User Created Successfully"}
   # return redirect(url_for('get_create_user_form'))
    return jsonify(response)

@app.route("/user/delete/")
def delete_user():
    user_id=request.args.get("user_id")
    print "user_id=%s" % user_id
    sql = """delete from user where user_id=%s"""
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(sql, (user_id))
    db.commit()
    db.close()
    #flash("Delete user successfully")
    return jsonify({"result": "Delete user Successfully"})

@app.route("/user/get/")
def get_user():
    user_id = request.args.get("user_id")
    sql = """select user_id, user_name, first_name, last_name, email from user where user_id=%s"""
    db = connect_db()
    cursor = db.cursor(my.cursors.DictCursor)
    cursor.execute(sql, (user_id))
    user = cursor.fetchone()
    db.close()
    return render_template("get_user.html", user=user)

@app.route("/user/edit/<int:user_id>", methods=['POST'])
def edit_user(user_id):
    sql = """update user set user_name=%s, first_name=%s, last_name=%s, email=%s where user_id=%s"""
    user_name = request.form['user_name']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(sql, [user_name, first_name, last_name, email, user_id])
    db.commit()
    db.close()
    #flash("Edit user successfully")
#    return redirect(url_for('get_user', user_id=user_id))
    return jsonify({"result": "Update user Successfully"})

@app.route("/")
@app.route("/index/")
def index():
    return render_template("index.html")

with app.test_request_context():
    print url_for('index')
    print url_for('get_user', user_id='123')

if __name__ == "__main__":
    app.run(host="0.0.0.0")

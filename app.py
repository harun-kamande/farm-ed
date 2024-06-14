from flask import Flask, render_template, redirect, request, session, url_for,flash
from flask_session import Session
from db_util import get_db_connection
app=Flask(__name__)


app.config["SECRET_KEY"] = "dont tell anyone"



import sqlite3



im= "images/Kamande. - Copy.jpg"
@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html",im=im)

@app.route("/content")
def content():
    return render_template("content.html")

@app.route("/feedback",methods=['POST','GET'])
def feedback():
    return render_template("feedback.html")
1
@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/logout",methods=["POST","GET"])
def logout():
    connection=sqlite3.connect("users.db")
    cursor=connection.cursor()
    cursor.execute("SELECT username,password FROM userdetails")
    details=cursor.fetchall()

    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if username== details[0][0] and password == details[0][1]:
            return render_template("post.html")
        else:
            return render_template("landing.html")
    return render_template("landing.html")

@app.route("/create", methods=["POST","GET"])
def create():

    connection=get_db_connection()
    cursor=connection.cursor()

    if request.method=="POST":
      
      username=request.form.get("username") 
      email=request.form.get("email")
      password=request.form.get("password")  


      cursor.execute("INSERT INTO user_details(user_name,email,user_password) VALUES(%s,%s,%s)",(username,email,password))
      cursor.close()
      connection.commit()
      return render_template("post.html")
    
    else:
        return render_template("create.html")


    return render_template("create.html")

@app.route("/post",methods=["POST","GET"])
def post():
    return render_template("post.html")

@app.route("/admin")
def admin():   
        return render_template("admin.html")

@app.route("/notifications", methods=["POST","GET"])
def notifications():
    return render_template("notifications.html")
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

if __name__=="__main__":
    app.run(debug=True)

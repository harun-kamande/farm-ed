from flask import Flask, render_template, redirect, request, session, url_for,flash,make_response
from flask_session import Session
from db_util import get_db_connection
import datetime
import time
app=Flask(__name__)


app.config["SECRET_KEY"] = "dont tell anyone"






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

@app.route("/login",methods=["POST","GET"])
def logout():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")

        connection=get_db_connection()
        cursor=connection.cursor()
        cursor.execute("SELECT email,user_password FROM user_details WHERE email=%s AND user_password=%s",(email,password))
        
        user=cursor.fetchone()

        if user:
            return render_template("home.html")
        else:
            flash("WRONG PASSWORD OR EMAIL PLEASE TRY AGAIN LATER")
    
    return render_template("login.html")

@app.route("/create", methods=["POST", "GET"])
def create():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        cursor.execute("SELECT email FROM user_details WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Account is taken, please choose another email")
        else:
            cursor.execute(
                "INSERT INTO user_details (user_name, email, user_password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            flash("Account created successfully!")
            
            connection.commit()

    cursor.close()
    connection.close()

    return render_template("create.html")


@app.route("/post", methods=["POST", "GET"])
def post():
    if request.method == "POST":
        post_title = request.form.get("title")
        post_content = request.form.get("post")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO posts (title, post, date_posted, user_id) VALUES (%s, %s, %s, %s)", (post_title, post_content, datetime.datetime.now().strftime("%B %d  %Y %H:%M:%S"), 1))


        connection.commit()
        return render_template("content.html")

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

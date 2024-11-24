from flask import Flask, render_template, redirect, request, session, url_for, flash, make_response
from db_util import get_db_connection
from jinja2 import UndefinedError, TemplateNotFound
import datetime
import os
import hashlib
from models import User, session, Session, Posts, Reply
from sqlalchemy import Column, String, ForeignKey, Integer, create_engine, desc

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkamande"


@app.route("/profile")
def profile():
    email = request.cookies.get("id")
    if not email:
        # Handle the case where the email cookie is missing
        return redirect(url_for('login'))

    myprofile = session.query(User.user_name, User.date_joined, User.email).filter(
        User.email == email).all()

    return render_template("profile.html", data=myprofile)


@app.route("/firstpage", methods=["POST", "GET"])
def firstpage():
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("id", "", expires=0)

    return resp


@app.route("/", methods=["POST", "GET"])
def landing():
    return redirect(url_for('login'))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/content", methods=["POST", "GET"])
def content():

    my_email = request.cookies.get("id")
    getMyid = session.query(User).filter(User.email == my_email).one_or_none()
    my_id = getMyid.email
    if my_id:
        posts = session.query(User.id, User.user_name, Posts.title, Posts.post, Posts.date_posted, Posts.id,
                              Posts.likes, Posts.myfile).join(User, User.id == Posts.user_id).order_by(desc(Posts.likes)).all()

        replies = session.query(Reply.id, Reply.reply, Reply.post_id, User.user_name).join(
            User, User.id == Reply.user_id).all()

        return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashedpassword = hashlib.sha256(password.encode()).hexdigest()

        validateuser = session.query(User).filter(
            User.email == email, User.user_password == hashedpassword).one_or_none()
        if validateuser:
            resp = make_response(render_template("home.html"))
            resp.set_cookie("id", email)
            return resp
        else:
            flash("Wrong password or email. Please try again later.")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/create", methods=["POST", "GET"])
def create():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hashedpassword = hashlib.sha256(password.encode()).hexdigest()

        checkwhether_userExist = session.query(
            User).filter(User.email == email).one_or_none()
        if checkwhether_userExist:
            flash("Account is taken, please choose another email")

        else:
            addnewuser = User(username, email, hashedpassword,
                              datetime.datetime.now().strftime("%B %d  %Y %H:%M:%S"))
            session.add(addnewuser)
            session.commit()
            flash("Account created successfully!")
            return redirect(url_for('login'))

    cursor.close()
    connection.close()

    return render_template("new_create.html")


@app.route("/post", methods=["POST", "GET"])
def post():
    if request.method == "POST":
        post_title = request.form.get("title")
        post = request.form.get("post")

        category = request.form.get("category")

        myfile = request.files.get("myfile")

        if myfile:
            filename = myfile.filename
            upload_folder = 'static/uploads'
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, myfile.filename)
            myfile.save(file_path)

            email = request.cookies.get("id")

            user_id = session.query(User.id).filter(User.email == email).all()

            submit_a_post = Posts(
                post_title, user_id[0][0], category, post, filename)

            session.add(submit_a_post)
            session.commit()

            return render_template("post.html")
        else:
            email = request.cookies.get("id")

            user_id = session.query(User.id).filter(User.email == email).all()

            submit_a_post = Posts(post_title, user_id[0][0],
                                  category, post, "")

            session.add(submit_a_post)
            session.commit()

            return render_template("post.html")

    return render_template("post.html")


@app.route("/delete_post", methods=["POST"])
def delete_post():
    connection = get_db_connection()
    cursor = connection.cursor()
    post_id = request.form['id']

    session.query(Reply).filter(Reply.post_id == post_id).delete()
    session.query(Posts).filter(Posts.id == post_id).delete()

    session.commit()

    return redirect(url_for('content'))


@app.route("/dailyFarming", methods=["POST", "GET"])
def dailyFarming():

    connection = get_db_connection()
    cursor = connection.cursor()

    my_email = request.cookies.get("id")
    my_id = session.query(User.id).filter(User.email == my_email).all()

    posts = session.query(User.id, User.user_name, Posts.title, Posts.post, Posts.date_posted, Posts.id, Posts.likes, Posts.myfile).join(
        User, User.id == Posts.user_id).filter(Posts.category == "Dairy_farming").order_by(desc(Posts.category)).all()

    replies = session.query(Reply.id, Reply.reply, Reply.post_id, User.user_name).join(
        User, User.id == Reply.user_id).all()

    return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)


@app.route("/coffee")
def coffee():

    my_email = request.cookies.get("id")
    my_id = session.query(User.id).filter(User.email == my_email).all()

    posts = session.query(User.id, User.user_name, Posts.title, Posts.post, Posts.date_posted, Posts.id, Posts.likes, Posts.myfile).join(
        User, User.id == Posts.user_id).filter(Posts.category == "coffee").order_by(desc(Posts.likes)).all()

    replies = session.query(Reply.id, Reply.reply, Reply.post_id, User.user_name).join(
        User, User.id == Reply.user_id).all()

    if posts:
        return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)
    else:
        return "No posts in this section "


@app.route("/tea")
def tea():

    my_email = request.cookies.get("id")
    my_id = session.query(User.id).filter(User.email == my_email).all()

    posts = session.query(User.id, User.user_name, Posts.title, Posts.post, Posts.date_posted, Posts.id, Posts.likes, Posts.myfile).join(
        User, User.id == Posts.user_id).filter(Posts.category == "tea").order_by(desc(Posts.category)).all()

    replies = session.query(Reply.id, Reply.reply, Reply.post_id, User.user_name).join(
        User, User.id == Reply.user_id).all()

    if posts:
        return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)
    else:
        return "No posts in this section "


@app.route("/maize_farming")
def maize_farming():

    my_email = request.cookies.get("id")
    my_id = session.query(User.id).filter(User.email == my_email).all()

    posts = session.query(User.id, User.user_name, Posts.title, Posts.post, Posts.date_posted, Posts.id, Posts.likes, Posts.myfile).join(
        User, User.id == Posts.user_id).filter(Posts.category == "Maize_farming").order_by(desc(Posts.category)).all()

    replies = session.query(Reply.id, Reply.reply, Reply.post_id, User.user_name).join(
        User, User.id == Reply.user_id).all()

    if posts:
        return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)
    else:
        return "No posts in this section "


@app.route("/others")
def others():
    connection = get_db_connection()
    cursor = connection.cursor()

    my_email = request.cookies.get("id")
    my_id = session.query(User.id).filter(User.email == my_email).all()

    posts = session.query(
        User.id,
        User.user_name,
        Posts.title,
        Posts.post,
        Posts.date_posted,
        Posts.id,
        Posts.likes,
        Posts.myfile
    ).join(Posts, Posts.user_id == User.id).filter(
        Posts.category == 'others'
    ).order_by(
        desc(Posts.likes)
    ).all()

    replies = session.query(Reply.id, Reply.reply, Reply.post_id, User.user_name).join(
        User, User.id == Reply.user_id).all()

    if posts:
        return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)
    else:
        return "No posts in this section "


@app.route("/like", methods=["POST"])
def like():
    post_id = request.form.get("post_id")

    session.query(Posts).filter(Posts.id == post_id).update({
        Posts.likes: Posts.likes + 1
    })

    session.commit()

    return redirect(url_for('content'))


@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        post_id = request.form.get("post_id")
        post_update = request.form.get("post_update")

        session.query(Posts).filter(Posts.id == post_id).update(
            {Posts.post: post_update})
        session.commit()

        return redirect(url_for('content'))
    else:
        return redirect(url_for('content'))


@app.route("/reply", methods=["POST", "GET"])
def reply():
    if request.method == "POST":

        user_email = request.cookies.get("id")

        getId = session.query(User.id).filter(User.email == user_email).all()

        reply = request.form.get("reply")
        reply = reply.encode("utf8")
        post_id = request.form.get("post_id")

        replying = Reply(reply, post_id, getId[0][0])
        session.add(replying)
        session.commit()

        return redirect(url_for("content"))
    else:
        return redirect(url_for("content"))


'''
This errorHandler is catching an error where cookie is empty or has expired
Ive used cookie to store the email of the user,so ill need to fetch it incase i need to clarify who posted 
the content
'''


@app.errorhandler(IndexError)
def handle_index_error(error):
    return render_template('login'), 500


'''
catching an error where cookie is empty
This file is doing the same task,
'''


@app.errorhandler(UndefinedError)
def go_back_home(error):
    return redirect(url_for('login')), 500


@app.errorhandler(TemplateNotFound)
def go_home(error):
    return redirect(render_template("home.html")), 500


if __name__ == "__main__":
    app.run(debug=True)

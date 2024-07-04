from flask import Flask, render_template, redirect, request, session, url_for, flash, make_response
from db_util import get_db_connection
from jinja2 import UndefinedError
import datetime
import os


app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkamande"


@app.route("/profile")
def profile():
    email = request.cookies.get("id")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """SELECT user_name,date_joined,email FROM user_details WHERE email=%s""", (email,))
    data = cursor.fetchall()
    return render_template("profile.html", data=data)


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
    connection = get_db_connection()
    cursor = connection.cursor()

    my_email = request.cookies.get("id")
    cursor.execute("SELECT id FROM user_details WHERE email=%s", (my_email,))
    my_id = cursor.fetchall()

    cursor.execute("""
        SELECT user_details.id, user_details.user_name, posts.title, posts.post, posts.date_posted, posts.id, posts.likes, posts.myfile
        FROM posts
        INNER JOIN user_details ON posts.user_id = user_details.id
        ORDER BY posts.likes DESC
    """)
    posts = cursor.fetchall()

    cursor.execute("""
        SELECT reply.id, reply.reply, reply.post_id, user_details.user_name
        FROM reply
        INNER JOIN user_details ON reply.user_id = user_details.id
    """)
    replies = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT email, user_password FROM user_details WHERE email=%s AND user_password=%s", (email, password))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
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

        cursor.execute(
            "SELECT email FROM user_details WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Account is taken, please choose another email")
        else:
            cursor.execute(
                "INSERT INTO user_details (user_name, email, user_password,date_joined) VALUES (%s, %s, %s,%s)",
                (username, email, password,
                 datetime.datetime.now().strftime("%B %d  %Y %H:%M:%S"))
            )
            flash("Account created successfully!")

            connection.commit()
            return redirect(url_for('login'))

    cursor.close()
    connection.close()

    return render_template("new_create.html")


@app.route("/post", methods=["POST", "GET"])
def post():
    if request.method == "POST":
        post_title = request.form.get("title")
        post_content = request.form.get("post")

        category = request.form.get("category")

        myfile = request.files.get("myfile")

        connection = get_db_connection()

        if myfile:
            filename = myfile.filename
            upload_folder = 'static/uploads'
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, myfile.filename)
            myfile.save(file_path)

            connection = get_db_connection()
            cursor = connection.cursor()

            email = request.cookies.get("id")

            cursor.execute(
                "SELECT id FROM user_details WHERE email=%s", (email,))

            user_id = cursor.fetchall()

            cursor.execute("INSERT INTO posts (title, post, date_posted, user_id,category,likes,myfile) VALUES (%s, %s, %s, %s,%s,%s,%s)", (
                post_title, post_content, datetime.datetime.now().strftime("%B %d  %Y %H:%M:%S"), user_id[0][0], category, 0, filename))
            connection.commit()
            return render_template("post.html")
        else:
            cursor = connection.cursor()
            email = request.cookies.get("id")
            cursor.execute(
                "SELECT id FROM user_details WHERE email=%s", (email,))
            user_id = cursor.fetchall()

            cursor.execute("INSERT INTO posts (title, post, date_posted, user_id,category,likes) VALUES (%s, %s, %s, %s,%s,%s)", (
                post_title, post_content, datetime.datetime.now().strftime("%B %d  %Y %H:%M:%S"), user_id[0][0], category, 0))
            connection.commit()
            return render_template("post.html")

    return render_template("post.html")


@app.route("/delete_post", methods=["POST"])
def delete_post():
    connection = get_db_connection()
    cursor = connection.cursor()
    post_id = request.form['id']

    cursor.execute("DELETE FROM reply WHERE post_id=%s", (post_id,))
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('content'))


@app.route("/dailyFarming", methods=["POST", "GET"])
def dailyFarming():

    connection = get_db_connection()
    cursor = connection.cursor()

    my_email = request.cookies.get("id")
    cursor.execute("SELECT id FROM user_details WHERE email=%s", (my_email,))
    my_id = cursor.fetchall()
    cursor.execute("""
        SELECT user_details.id, user_details.user_name, posts.title, posts.post, posts.date_posted, posts.id, posts.likes, posts.myfile
        FROM posts
        INNER JOIN user_details ON posts.user_id = user_details.id
                   WHERE posts.category='Dairy_farming'
        ORDER BY posts.likes DESC
    """)

    posts = cursor.fetchall()

    cursor.execute("""
        SELECT reply.id, reply.reply, reply.post_id, user_details.user_name
        FROM reply
        INNER JOIN user_details ON reply.user_id = user_details.id
    """)
    replies = cursor.fetchall()

    connection.close()

    return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)


@app.route("/coffee")
def coffee():
    connection = get_db_connection()
    cursor = connection.cursor()

    my_email = request.cookies.get("id")
    cursor.execute("SELECT id FROM user_details WHERE email=%s", (my_email,))
    my_id = cursor.fetchall()

    cursor.execute("""
        SELECT user_details.id, user_details.user_name, posts.title, posts.post, posts.date_posted, posts.id, posts.likes, posts.myfile
        FROM posts
        INNER JOIN user_details ON posts.user_id = user_details.id
                   WHERE posts.category='coffee'
        ORDER BY posts.likes DESC
    """)
    posts = cursor.fetchall()
    cursor.execute("""
        SELECT reply.id, reply.reply, reply.post_id, user_details.user_name
        FROM reply
        INNER JOIN user_details ON reply.user_id = user_details.id
    """)
    replies = cursor.fetchall()

    cursor.close()
    connection.close()

    if posts:
        return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)
    else:
        return "No posts in this section "


@app.route("/tea")
def tea():
    connection = get_db_connection()
    cursor = connection.cursor()

    my_email = request.cookies.get("id")
    cursor.execute("SELECT id FROM user_details WHERE email=%s", (my_email,))
    my_id = cursor.fetchall()

    cursor.execute("""
        SELECT user_details.id, user_details.user_name, posts.title, posts.post, posts.date_posted, posts.id, posts.likes, posts.myfile
        FROM posts
        INNER JOIN user_details ON posts.user_id = user_details.id
                   WHERE posts.category='tea'
        ORDER BY posts.likes DESC
    """)

    posts = cursor.fetchall()

    cursor.execute("""
        SELECT reply.id, reply.reply, reply.post_id, user_details.user_name
        FROM reply
        INNER JOIN user_details ON reply.user_id = user_details.id
    """)
    replies = cursor.fetchall()
    connection.close()

    if posts:
        return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)
    else:
        return "No posts in this section "


@app.route("/maize_farming")
def maize_farming():
    connection = get_db_connection()
    cursor = connection.cursor()

    my_email = request.cookies.get("id")
    cursor.execute("SELECT id FROM user_details WHERE email=%s", (my_email,))
    my_id = cursor.fetchall()

    cursor.execute("""
        SELECT user_details.id, user_details.user_name, posts.title, posts.post, posts.date_posted, posts.id, posts.likes, posts.myfile
        FROM posts
        INNER JOIN user_details ON posts.user_id = user_details.id
                   WHERE posts.category='Maize_farming'
        ORDER BY posts.likes DESC
    """)

    posts = cursor.fetchall()

    cursor.execute("""
        SELECT reply.id, reply.reply, reply.post_id, user_details.user_name
        FROM reply
        INNER JOIN user_details ON reply.user_id = user_details.id
    """)
    replies = cursor.fetchall()
    connection.close()
    if posts:
        return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)
    else:
        return "No posts in this section "


@app.route("/others")
def others():
    connection = get_db_connection()
    cursor = connection.cursor()

    my_email = request.cookies.get("id")
    cursor.execute("SELECT id FROM user_details WHERE email=%s", (my_email,))
    my_id = cursor.fetchall()

    cursor.execute("""
        SELECT user_details.id, user_details.user_name, posts.title, posts.post, posts.date_posted, posts.id, posts.likes, posts.myfile
        FROM posts
        INNER JOIN user_details ON posts.user_id = user_details.id
                   WHERE posts.category='others'
        ORDER BY posts.likes DESC
    """)

    posts = cursor.fetchall()

    cursor.execute("""
        SELECT reply.id, reply.reply, reply.post_id, user_details.user_name
        FROM reply
        INNER JOIN user_details ON reply.user_id = user_details.id
    """)
    replies = cursor.fetchall()
    connection.close()
    if posts:
        return render_template("content.html", posts=posts, id=my_id[0][0], replies=replies)
    else:
        return "No posts in this section "


@app.route("/like", methods=["POST"])
def like():
    post_id = request.form.get("post_id")

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE posts SET likes = likes + 1 WHERE id = %s", (post_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('content'))


@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        post_id = request.form.get("post_id")
        post_update = request.form.get("post_update")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""UPDATE posts SET post=%s
                       WHERE id=%s""", (post_update, post_id))
        cursor.close()
        connection.commit()
        return redirect(url_for('content'))
    else:
        return redirect(url_for('content'))


@app.route("/reply", methods=["POST", "GET"])
def reply():
    if request.method == "POST":
        connection = get_db_connection()
        cursor = connection.cursor()

        user_email = request.cookies.get("id")
        cursor.execute(
            "SELECT id FROM user_details WHERE email=%s", (user_email,))
        user_id = cursor.fetchall()

        reply = request.form.get("reply")
        post_id = request.form.get("post_id")

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO reply(reply,post_id,user_id)
                       VALUES(%s,%s,%s)""", (reply, post_id, user_id[0][0],))
        connection.commit()
        return redirect(url_for("content"))
    else:
        return redirect(url_for("content"))


'''
This errorHandler catching an error where cookie is empty or has expired
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


if __name__ == "__main__":
    app.run(debug=True)

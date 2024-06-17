from flask import Flask, render_template, redirect, request, session, url_for, flash, make_response
from db_util import get_db_connection
import datetime


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


@app.route("/content")
def content():
    connection = get_db_connection()
    cursor = connection.cursor()

    # selecting user id
    my_email = request.cookies.get("id")
    cursor.execute("SELECT id FROM user_details WHERE email=%s", (my_email,))
    my_id = cursor.fetchall()

    cursor.execute("""
        SELECT user_details.id, user_details.user_name, posts.title, posts.post, posts.date_posted,posts.id
        FROM posts
        INNER JOIN user_details ON posts.user_id = user_details.id
                   ORDER BY posts.date_posted DESC
    """)

    posts = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("content.html", posts=posts, id=my_id[0][0])


@app.route("/feedback", methods=['POST', 'GET'])
def feedback():
    return render_template("feedback.html")


1


# Point to be explored
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

        connection = get_db_connection()
        cursor = connection.cursor()

        email = request.cookies.get("id")

        cursor.execute("SELECT id FROM user_details WHERE email=%s", (email,))

        user_id = cursor.fetchall()

        cursor.execute("INSERT INTO posts (title, post, date_posted, user_id) VALUES (%s, %s, %s, %s)", (
            post_title, post_content, datetime.datetime.now().strftime("%B %d  %Y %H:%M:%S"), user_id[0][0]))

        connection.commit()
        return redirect(url_for('content'))

    return render_template("post.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/delete_post", methods=['POST', 'GET'])
def delete_post():
    if request.method == "POST":
        post_id = request.form.get("id")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM posts WHERE id=%s", (post_id,))
        connection.commit()

        return redirect(url_for("content"))
    return render_template("content.html")


if __name__ == "__main__":
    app.run(debug=True)

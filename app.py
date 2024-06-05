from flask import Flask, render_template, redirect, request, session, url_for,flash
app=Flask(__name__)

# @app.route("/")
# def Hello():
#     return render_template("home.html")

# @app.route("/page")
# def page():
#     return f"Hello page"
# @app.route("/open")
# def open():
#     return render_template("open.html")
# @app.route("/home")
# def home():
#     return render_template("home.html")

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/content")
def content():
    return render_template("content.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
    return render_template("landing.html")

if __name__=="__main__":
    app.run(debug=True)
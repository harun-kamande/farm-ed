from flask import Flask, render_template, redirect, request, session, url_for,flash
app=Flask(__name__)
im= "images/Kamande. - Copy.jpg"
@app.route("/")
def landing():
    return render_template("landing.html")

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

@app.route("/logout")
def logout():
    return render_template("landing.html")

@app.route("/create", methods=["POST","GET"])
def create():    
    return render_template("create.html")

@app.route("/post",methods=["POST","GET"])
def post():
    return render_template("post.html")

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

if __name__=="__main__":
    app.run(debug=True)

from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/')
def index():
    resp = make_response("Cookie is set")
    resp.set_cookie("id", "hellosss")
    return "Hello world"

@app.route("/logout")
def logout():
    response=make_response("Removing a cookie")
    response.set_cookie("id","",expires=0)
    id=request.cookies.get("id")

    return response

if __name__ == "__main__":
    app.run(debug=True)




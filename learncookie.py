from flask import Flask, make_response,request
app=Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

@app.route("/cookie")
def cook():
    # Cookie setting from individual browser/ User
    res=make_response("<h1>Cookie is set</h1>")
    res.set_cookie("Id","Kamande")
    session=request.cookies.get("session")

    return (f"{res} session is {session}")
@app.route("/logout")
def getout():
    res=make_response("<h1>You are about to logout</h1>")
    res.set_cookie("Id","", expires=0)
    

    return res


@app.route("/home")
def read():

    # Getting cookies from individual web browser

    userid=request.cookies.get("Id")
    if userid==None:
        return "Nothing to see here"

    return userid



if __name__=="__main__":
    app.run(debug=True)

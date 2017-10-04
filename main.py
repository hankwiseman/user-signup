from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

@app.route("/welcome", methods=['POST'])
def welcome_screen():
    # look inside the request to figure out what the user typed
    user_name = request.form['username']
    password = request.form['password']
    verified_password = request.form['verified_password']
    email = request.form['email']

    # if the user typed nothing at all, redirect and tell them the error
    if len(user_name) < 3 or len(user_name) > 20:
        error = "The username is not between 3 and 20 characters."
        return redirect("/?error=" + error)

    if len(password) < 3 or len(password) > 20:
        error = "The password is not between 3 and 20 characters."
        return redirect("/?error=" + error)
    
    if password != verified_password:
        error = "The passwords do not match"
        return redirect("/?error=" + error)

    


    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    new_username_escaped = cgi.escape(user_name, quote=True)

    return render_template('welcome.html', username=user_name)


@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('index.html', error=encoded_error and cgi.escape(encoded_error, quote=True))

app.run()
from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

@app.route("/welcome", methods=['POST'])
def welcome_screen():
    # look inside the request to figure out what the user typed
    error = None
    user_name = request.form['username']
    password = request.form['password']
    verified_password = request.form['verified_password']
    email = request.form['email']

    # if the user typed nothing at all, redirect and tell them the error
    if len(user_name) < 3 or len(user_name) > 20:
        username_error = "The username is not between 3 and 20 characters."
        return render_template('index.html', username_error=username_error)

    if len(password) < 3 or len(password) > 20:
        password_error = "The password is not between 3 and 20 characters."
        return render_template('index.html', password_error=password_error)
    
    for letter in user_name:
        if letter == " ":
            username_error = "The username cannot contain a space"
            return render_template('index.html', username_error=username_error)
    
    for letter in password:
        if letter == " ":
            password_error = "The password cannot contain a space"
            return render_template('index.html', password_error=password_error)

    if password != verified_password:
        verify_error = "The passwords do not match"
        return render_template('index.html', verify_error=verify_error)

    if email != "":
        if len(email) < 3 or len(email) > 20:
            email_error = "The e-mail is not between 3 and 20 characters."
            return render_template('index.html', email_error=email_error)
        at_counter = 0
        per_counter = 0
        for letter in email:
            if letter == " ":
                email_error = "The e-mail cannot contain a space"
                return render_template('index.html', email_error=email_error)

            elif letter == "@":
                at_counter = at_counter + 1

            elif letter == ".":
                per_counter = per_counter + 1
        
        if at_counter != 1 or per_counter != 1:
            email_error = "The e-mail can only have one @ or space"
            return render_template('index.html', email_error=email_error)




    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    new_username_escaped = cgi.escape(user_name, quote=True)

    return render_template('welcome.html', username=user_name)


@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('index.html', error=encoded_error and cgi.escape(encoded_error, quote=True))

app.run()
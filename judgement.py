from flask import Flask, render_template, redirect, request, url_for, flash, session
import model


app = Flask(__name__)
app.secret_key = "don'ttellanyoneaaaaaaaah"

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/signup")
def signup():
    # TODO: Redirect if already signed in.
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def create_user():

    # TODO: Verify that it's an email address on the page
    email = request.form.get("email")
    # TODO: Verify passwords match on the page
    password = request.form.get("password")
    password_verify = request.form.get("password_verify")

    if password != password_verify:
        flash("The passwords don't match.")
        return redirect(url_for("signup"))

    existing_users = model.session.query(model.User).filter_by(email=email).all()
    
    if existing_users == []:
        print "No existing users with that email!"
        user = model.User(email=email, password=hash(password))
        model.session.add(user)
        model.session.commit()

        flash("User created.")
        return redirect(url_for("login"))
    else:
        flash("That email is already in use.")
        return redirect(url_for("signup"))

@app.route("/login")
def login():
    # TODO: Redirect user if already logged in.
    return render_template("login.html")
    
@app.route("/login", methods=["POST"])
def log_in_user():
    email = request.form.get("email")
    password = request.form.get("password")

     # Put into try/except clause?
    user = model.session.query(model.User).filter_by(email=email).one()
    if int(user.password) == hash(password):
        session['user_id'] = user.id
        return redirect(url_for("index"))
    else:
        flash("Email and password don't match.")
        return redirect(url_for("login"))


@app.route("/user/<int:id>")
def user():
    # TODO: stuff
    pass

if __name__ == "__main__":
    app.run(debug = True)
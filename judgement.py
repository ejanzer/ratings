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
    # TODO: redirect if already logged in?
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

@app.route("/allusers")
def all_users():
    # TODO: get all users from the database.
    # TODO: Make this happen using ajax?
    last_id = 10
    user_list = model.session.query(model.User).limit(last_id).all()
    return render_template("user_list.html", users=user_list, last_id=last_id)

@app.route("/moreusers/<int:last_id>")
def more_users(last_id):
    # TODO: make this return the next 10 users?
    user_list = model.session.query(model.User).filter(model.User.id >= last_id).limit(10).all()
    next_id = last_id + 10
    print next_id
    return render_template("user_list_partial.html", users=user_list, last_id=next_id)

@app.route("/user/<int:user_id>")
def user(user_id):
    # get the ratings for a single user
    user = model.session.query(model.User).filter_by(id=user_id).first()
    user_movies = user.ratings
    return render_template('user.html', user=user, ratings=user_movies)

@app.route("/movie/<int:movie_id>", methods=["GET"])
def movie(movie_id):
    # get the user object
    user = model.session.query(model.User).get(session.get('user_id'))
    user_rating = None
    rating_numbers = []
    prediction = None
    movie = model.session.query(model.Movie).filter_by(id=movie_id).first()
    ratings = movie.ratings

    for r in ratings:
        if r.user_id == user.id:
            user_rating = r
        rating_numbers.append(r.rating)
    avg_rating = float(sum(rating_numbers))/len(rating_numbers)
    
    if not user_rating:
        prediction = user.predict_rating(movie)
        effective_rating = prediction
        print 'effective rating ', effective_rating
    else:
        effective_rating = user_rating.rating
        print 'effective rating', effective_rating

    the_eye = model.session.query(model.User).filter_by(email='eye@gmail.com').one()
    eye_rating = model.session.query(model.Rating).filter_by(user_id=the_eye.id, movie_id=movie.id).first()
    print 'eye id ', the_eye.id
    print 'eye rating ', eye_rating

    if not eye_rating:
        eye_rating = the_eye.predict_rating(movie)
        # add to database
        new_eye_rating = model.Rating(user_id=the_eye.id, movie_id=movie.id, rating=eye_rating)
        model.session.add(new_eye_rating)
        model.session.commit()


    else:
        eye_rating = eye_rating.rating

    difference = abs(eye_rating - effective_rating)

    messages = ['I suppose you don\'t have such bad taste after all.',
    'I regret every decision that I\'ve ever made that has brought me to listen to your opinion.',
    'Words fail me, as your taste in movies has clearly failed you.', 'That movie is great. For a clown to watch. Idiot.', 'I can\'t even.']

    beratement = messages[int(difference)]
 
    return render_template('movie.html', beratement=beratement, user_id= user.id, user_rating = user_rating, average=avg_rating, prediction=prediction, movie=movie, ratings=ratings)

@app.route("/movie/<int:movie_id>", methods=["POST"])
def update_rating(movie_id):
    logged_user = session.get('user_id')
    if logged_user:
        save_rating = request.form.get('rating')
        user_rating = model.session.query(model.Rating).filter_by(user_id=logged_user, movie_id=movie_id).first()
        if user_rating:
            user_rating.rating = save_rating
            model.session.commit()
            flash('rating updated.')
        else:
            # create a new rating
            new_rating = model.Rating(user_id=logged_user, movie_id=movie_id, rating=save_rating)
            model.session.add(new_rating)
            model.session.commit()
            flash('you created a new rating.')
    return redirect(url_for('movie', movie_id=movie_id))


if __name__ == "__main__":
    app.run(debug = True)
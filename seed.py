import model
import csv
import datetime

def load_users(session):
    # use u.user
    # open a file
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            words = row[0].split('|')
            user = model.User(id=words[0], age=words[1], zipcode=words[4])
            session.add(user)
        session.commit()

def load_movies(session):

# id: integer
# name: string
# released_at: datetime
# imdb_url: string
    with open('seed_data/u.item', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            words = row[0].split('|')
            title = words[1]
            title = title.split('(')[0].strip().decode("latin-1")
            if (len(words) == 2):
                movie = model.Movie(id=words[0], name=title)
            elif (len(words) == 3):
                movie = model.Movie(id=words[0], name=title, imdb_url=words[2])
            else:
                released_year = datetime.datetime.strptime(words[2], '%d-%b-%Y')
                # print 'id :' + words[0]
                # print 'released year: %s' % released_year
                movie = model.Movie(id=words[0], name=title, released_at=released_year, imdb_url=words[3])
            session.add(movie)
        session.commit()

# id = Column(Integer, primary_key=True)
# movie_id = Column(Integer) # This needs to be a foreign key
# user_id = Column(Integer) # This needs to be a foreign key
# rating = Column(Integer)

def load_ratings(session):
    with open('seed_data/u.data', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            ratings = row[0].split()
            rating_obj = model.Rating(user_id=ratings[0], movie_id=ratings[1], rating=ratings[2])
            session.add(rating_obj)
        session.commit()

def main(session):
    load_ratings(session)
    load_users(session)
    load_movies(session)
    
if __name__ == "__main__":
    s= model.connect()
    main(s)

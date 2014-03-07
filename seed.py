import model
import csv
import datetime
import re

def load_users(session):
    # use u.user
    # open a file
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            user_id, age, gender, occupation, zipcode = row
            user = model.User(id=user_id, age=age, zipcode=zipcode)
            session.add(user)
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            session.rollback()

def load_movies(session):

# id: integer
# name: string
# released_at: datetime
# imdb_url: string
    with open('seed_data/u.item', 'rb') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            movie_id = row[0]
            title = row[1].decode("latin-1")
            title = re.sub(r'(.+)\s+\(\d{4}\)', r'\1', title)
            title = title.strip()
            if (row[2] == ''):
                released_at = None
                imdb_url = row[3]
            else:
                imdb_url = row[4]
                released_at = datetime.datetime.strptime(row[2], '%d-%b-%Y')
                            
            movie = model.Movie(id=movie_id, name=title, released_at=released_at, imdb_url=imdb_url)
            session.add(movie)

        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            session.rollback()

# id = Column(Integer, primary_key=True)
# movie_id = Column(Integer) # This needs to be a foreign key
# user_id = Column(Integer) # This needs to be a foreign key
# rating = Column(Integer)

def load_ratings(session):
    with open('seed_data/u.data', 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            user_id = int(row[0])
            movie_id = int(row[1])
            rating = int(row[2])
            rating_obj = model.Rating(user_id=user_id, movie_id=movie_id, rating=rating)
            session.add(rating_obj)
        try: 
            session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            session.rollback()

def main(session):
    load_ratings(session)
    #load_users(session)
    #load_movies(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)

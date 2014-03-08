from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)



# Movie:
# id: integer
# name: string
# released_at: datetime
# imdb_url: string

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    released_at = Column(Date, nullable=True)
    imdb_url = Column(String(64), nullable=True)

# Rating:
# id: integer
# movie_id: integer
# user_id: integer
# rating: integer

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id')) # This needs to be a foreign key
    user_id = Column(Integer, ForeignKey('users.id')) # This needs to be a foreign key
    rating = Column(Integer)

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

### End class declarations
# def connect():
#     print "Getting rid of this function."
#     return None

def similarity(user1, user2):
    """Returns the Pearson coefficient for two users."""
    # Put all user1's ratings into a dictionary with the movie_id as the key.
    user1_ratings = {}
    for rating in user1.ratings:
        user1_ratings[rating.movie_id] = rating

    paired_ratings = []

    # For all the movies that user2 has rated, check if user1 has rated them also.
    for user2_rating in user2.ratings:
        user1_rating = user1_ratings.get(user2_rating.movie_id)
        if user1_rating:
            # If so, put the two ratings into a tuple and add it to the list paired_ratings.
            pair = (user1_rating, user2_rating)
            paired_ratings.append(pair)

    # Return the Pearson coefficient for those two users, calculated in correlation.py.
    return correlation.pearson(paired_ratings)

def main():
    """In case we need this later."""
    pass

if __name__ == "__main__":
    main()

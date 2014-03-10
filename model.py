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

    def similarity(self, other):
        """Returns the Pearson coefficient for two users."""
        # Put all user1's ratings into a dictionary with the movie_id as the key.
        self_ratings = {}
        for rating in self.ratings:
            self_ratings[rating.movie_id] = rating.rating

        paired_ratings = []

        # For all the movies that other has rated, check if user1 has rated them also.
        for other_rating in other.ratings:
            self_rating = self_ratings.get(other_rating.movie_id)
            if self_rating:
                # If so, put the two ratings into a tuple and add it to the list paired_ratings.
                pair = (self_rating, other_rating.rating)
                paired_ratings.append(pair)

        
        if paired_ratings:
            # Return the Pearson coefficient for those two users, calculated in correlation.py.
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        # other rating is the list of all the ratings for the movie passed in
        other_ratings = movie.ratings
        # other users is a list of all the users who are associated with the list of other_ratings
        similarities = [(self.similarity(r.user),r) for r in other_ratings ]

        # sort the list of similarities so that the most similar other_user is at the top
        similarities.sort(reverse = True)
        similarities = [ sim for sim in similarities if sim[0] > 0]
        if not similarities:
            return None
        numerator = sum([r.rating * similarity for similarity, r in similarities])
        denominator = sum([similarity[0] for similarity in similarities])
        return numerator/denominator



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


def main():
    """In case we need this later."""
    pass

if __name__ == "__main__":
    main()

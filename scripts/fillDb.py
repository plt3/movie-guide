import json

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

with open("../uniqueMovies.json") as f:
    movList = json.load(f)

# can add echo=True for logging
engine = create_engine("sqlite:///../movies.db")
Session = sessionmaker(bind=engine)

session = Session()
Base = declarative_base()

# association tables for many-to-many relationships

movie_directors = Table(
    "movie_directors",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("director_id", Integer, ForeignKey("directors.id")),
)

movie_actors = Table(
    "movie_actors",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("actor_id", Integer, ForeignKey("actors.id")),
)

movie_countries = Table(
    "movie_countries",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("country_id", Integer, ForeignKey("countries.id")),
)

# classes representing database tables we will directly interact with


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    runtime = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    review = Column(String, nullable=False)
    see = Column(Boolean, nullable=False)

    directors = relationship(
        "Director",
        secondary=movie_directors,
        back_populates="movies",
    )
    actors = relationship(
        "Actor",
        secondary=movie_actors,
        back_populates="movies",
    )
    countries = relationship(
        "Country",
        secondary=movie_countries,
        back_populates="movies",
    )

    def __repr__(self):
        return f"<Movie(id={self.id}, title={self.title}, see={self.see})>"


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    movies = relationship(
        "Movie",
        secondary=movie_directors,
        back_populates="directors",
    )

    def __repr__(self):
        return f"<Director(id={self.id}, name={self.name})>"


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    movies = relationship(
        "Movie",
        secondary=movie_actors,
        back_populates="actors",
    )

    def __repr__(self):
        return f"<Actor(id={self.id}, name={self.name})>"


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    movies = relationship(
        "Movie",
        secondary=movie_countries,
        back_populates="countries",
    )

    def __repr__(self):
        return f"<Country(id={self.id}, name={self.name})>"


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    directorsMap = {}
    actorsMap = {}
    countriesMap = {}
    counter = 0

    for mov in movList:
        counter += 1

        movObj = Movie(
            title=mov["title"],
            runtime=mov.get("runtime"),
            year=mov.get("date"),
            rating=mov.get("rating"),
            review=mov["review"],
            see=mov["see"],
        )

        # only create a new director/actor/country object if they don't already exist
        for director in mov.get("directors", []):
            if director not in directorsMap:
                dirObj = Director(name=director)
                movObj.directors.append(dirObj)
                directorsMap[director] = dirObj
            else:
                movObj.directors.append(directorsMap[director])

        for actor in mov.get("actors", []):
            if actor not in actorsMap:
                actObj = Actor(name=actor)
                movObj.actors.append(actObj)
                actorsMap[actor] = actObj
            else:
                movObj.actors.append(actorsMap[actor])

        for country in mov.get("countries", []):
            if country not in countriesMap:
                countObj = Country(name=country)
                movObj.countries.append(countObj)
                countriesMap[country] = countObj
            else:
                movObj.countries.append(countriesMap[country])

        session.add(movObj)

        # commit every 1000 inserts
        if counter % 1000 == 0:
            session.commit()
            print(f"Committed {counter} so far.")

    session.commit()
    print(f"All done, {counter} movies committed.")

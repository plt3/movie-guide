# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


class Actor(models.Model):
    name = models.CharField(unique=True, max_length=100)

    # i think i got this working with through instead of db_table
    movies = models.ManyToManyField("Movie", db_table="movie_actors")

    class Meta:
        db_table = "actors"
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("actorDetail", kwargs={"pk": self.id})

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(unique=True, max_length=50)

    movies = models.ManyToManyField("Movie", db_table="movie_countries")

    class Meta:
        db_table = "countries"
        verbose_name_plural = "countries"
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("countryDetail", kwargs={"pk": self.id})

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(unique=True, max_length=100)

    movies = models.ManyToManyField("Movie", db_table="movie_directors")

    class Meta:
        db_table = "directors"
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("directorDetail", kwargs={"pk": self.id})

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    runtime = models.CharField(blank=True, max_length=20)
    year = models.IntegerField(blank=True)
    rating = models.FloatField(blank=True)
    review = models.TextField()
    see = models.BooleanField(default=False)

    # going back to this line and removing the ManyToManyFields in the other classes
    # would mean that you can't see/edit an actor's movies in the admin interface, but
    # also means that adding a completely new actor/director/country automatically
    # assigns them to the movie you're on without having to specify it
    # directors = models.ManyToManyField(Director, related_name="movies", db_table="movie_directors")

    directors = models.ManyToManyField(
        Director,
        through=Director.movies.through,
        blank=True,
    )
    actors = models.ManyToManyField(
        Actor,
        through=Actor.movies.through,
        blank=True,
    )
    countries = models.ManyToManyField(
        Country,
        through=Country.movies.through,
        blank=True,
    )

    class Meta:
        db_table = "movies"
        # sort movies from best to worst, can't think of a case where I don't want this
        ordering = ["-rating"]

    def getStars(self):
        if self.rating == 1.0:
            return "BOMB"
        elif not self.rating:
            return "N/A"
        else:
            return "★" * int(self.rating) + (
                " ½" if str(self.rating).endswith(".5") else ""
            )

    def get_absolute_url(self):
        return reverse("movieDetail", kwargs={"pk": self.id})

    def __str__(self):
        return self.title

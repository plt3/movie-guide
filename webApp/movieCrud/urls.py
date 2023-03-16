from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("movie/<int:pk>/", views.MovieDetailView.as_view(), name="movieDetail"),
    path(
        "director/<int:pk>/", views.DirectorDetailView.as_view(), name="directorDetail"
    ),
    path("actor/<int:pk>/", views.ActorDetailView.as_view(), name="actorDetail"),
    path("country/<int:pk>/", views.CountryDetailView.as_view(), name="countryDetail"),
]

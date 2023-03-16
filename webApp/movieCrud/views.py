from django.core.paginator import EmptyPage, Paginator
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from movieCrud.models import Actor, Country, Director, Movie

PER_PAGE = 20


class HomeListView(ListView):
    model = Movie
    template_name = "movieCrud/home.html"
    paginate_by = PER_PAGE

    def get_queryset(self):
        searchQuery = self.request.GET.get("q")
        searchType = self.request.GET.get("type", "title")

        if searchQuery:
            if searchType == "actor":
                return Actor.objects.filter(name__icontains=searchQuery)
            elif searchType == "director":
                return Director.objects.filter(name__icontains=searchQuery)
            elif searchType == "country":
                return Country.objects.filter(name__icontains=searchQuery)
            elif searchType == "year":
                try:
                    return Movie.objects.filter(year=searchQuery)
                except ValueError:
                    return Movie.objects.none()
            elif searchType == "rating":
                try:
                    return Movie.objects.filter(rating=searchQuery)
                except ValueError:
                    return Movie.objects.none()
            elif searchType == "review":
                return Movie.objects.filter(review__icontains=searchQuery)
            else:
                return Movie.objects.filter(title__icontains=searchQuery)
        else:
            if searchType == "actor":
                return Actor.objects.all()
            elif searchType == "director":
                return Director.objects.all()
            elif searchType == "country":
                return Country.objects.all()
            else:
                return Movie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["searchQuery"] = self.request.GET.get("q", "")
        searchType = self.request.GET.get("type", "title")
        context["searchType"] = searchType
        context["isMovieObjs"] = searchType in ["title", "year", "rating", "review"]

        return context

    def get(self, *args, **kwargs):
        objectList = self.get_queryset()

        # redirect to detail page if only one result found
        if len(objectList) == 1:
            return redirect(objectList[0])
        else:
            return super(HomeListView, self).get(*args, **kwargs)


class MovieDetailView(DetailView):
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movObj = context["movie"]
        if movObj.see:
            try:
                context["referenceId"] = (
                    Movie.objects.filter(title__iexact=movObj.review).first().id
                )
            except AttributeError:
                try:
                    context["referenceId"] = [
                        mov
                        for mov in Movie.objects.filter(title__iexact=movObj.title)
                        if mov.id != movObj.id
                    ][0].id
                except IndexError:
                    pass

        return context


class DirectorDetailView(DetailView):
    model = Director
    template_name = "movieCrud/ADC_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pager = Paginator(context["object"].movies.all(), PER_PAGE)
        page = self.request.GET.get("page", 1)

        context["paginator"] = pager
        context["headingLine"] = "Movies by " + context["object"].name + ":"

        try:
            context["pageObj"] = pager.page(page)
        except EmptyPage:
            raise Http404("No objects found on this page.")

        return context


class ActorDetailView(DetailView):
    model = Actor
    template_name = "movieCrud/ADC_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pager = Paginator(context["object"].movies.all(), PER_PAGE)
        page = self.request.GET.get("page", 1)

        context["paginator"] = pager
        context["headingLine"] = "Movies with " + context["object"].name + ":"

        try:
            context["pageObj"] = pager.page(page)
        except EmptyPage:
            raise Http404("No objects found on this page.")

        return context


class CountryDetailView(DetailView):
    model = Country
    template_name = "movieCrud/ADC_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pager = Paginator(context["object"].movies.all(), PER_PAGE)
        page = self.request.GET.get("page", 1)

        context["paginator"] = pager
        context["headingLine"] = context["object"].name + " movies:"

        try:
            context["pageObj"] = pager.page(page)
        except EmptyPage:
            raise Http404("No objects found on this page.")

        return context

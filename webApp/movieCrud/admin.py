from django.contrib import admin

from .models import Actor, Country, Director, Movie


class MovieAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "runtime",
        "year",
        "review",
        "rating",
        "directors",
        "actors",
        "countries",
        "see",
    ]
    autocomplete_fields = ["directors", "actors", "countries"]
    readonly_fields = ["see"]
    list_display = ("title", "year", "rating", "runtime", "see")
    search_fields = ["title"]
    view_on_site = True


class ADCAdmin(admin.ModelAdmin):
    fields = ["name", "movies"]
    autocomplete_fields = ["movies"]
    list_display = ["name"]
    search_fields = ["name"]
    view_on_site = True


admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ADCAdmin)
admin.site.register(Director, ADCAdmin)
admin.site.register(Country, ADCAdmin)

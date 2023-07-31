from django.contrib import admin
from .models import Videos, Favorites

# Register your models here.
@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'view_counts', 'favorites_counts')

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'user_src', 'add_time')
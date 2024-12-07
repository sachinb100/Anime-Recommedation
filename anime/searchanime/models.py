from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Anime(models.Model):
    title = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre)
    description = models.TextField(default="No description available")

    def __str__(self):
        return self.title
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_genres = models.ManyToManyField(Genre)
    watched_anime = models.ManyToManyField(Anime)

    def __str__(self):
        return f"{self.user.username}'s preferences"

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreferences, Genre, Anime



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        # Extract the password from the validated data and hash it
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['id', 'title', 'genres']

class UserPreferencesSerializer(serializers.ModelSerializer):
    favorite_genres = GenreSerializer(many=True, read_only=False)
    watched_anime = AnimeSerializer(many=True, read_only=False)

    class Meta:
        model = UserPreferences
        fields = ['favorite_genres', 'watched_anime']

from rest_framework import serializers
from django.contrib.auth.models import User
# from django.apps import apps
from .models import UserPreferences, Genre, Anime
# from .models import Anime, UserPreference
# from .models import UserPreference

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password']

# class AnimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = apps.get_model('searchanime', 'Anime')  # Dynamically get the Anime model
#         fields = ['id', 'title', 'genre', 'popularity']

# class AnimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Anime
#         fields = ['title', 'genre', 'popularity']

# class UserPreferenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPreference
#         fields = ['favorite_genre']

# class AnimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Anime
#         fields = ['id', 'title', 'genre', 'popularity']

# class UserPreferenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPreference
#         fields = ['favorite_genre']

# class AnimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = None  # temporarily set model to None

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         from .models import Anime  
#         self.Meta.model = Anime

# class UserPreferenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = apps.get_model('searchanime', 'UserPreference')  # Dynamically load the UserPreference model
#         fields = ['favorite_genre']


# class UserPreferenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = None  # Temporarily set the model to None

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Import the UserPreference model inside the class to avoid circular import
#         from .models import UserPreference  # This import is delayed
#         self.Meta.model = UserPreference



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
# class AnimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Anime
#         fields = ['title', 'genres', 'description']

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

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, AnimeSerializer, UserPreferencesSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import UserPreferences, Genre, Anime
import requests
from django.contrib.auth import authenticate, login
from django.conf import settings

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            password = request.data.get('password') 
            user.set_password(password)
            user.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class AnimeSearchView(APIView):
    def get(self, request):
        # Retrieve search query from request
        name = request.query_params.get('name')
        genre = request.query_params.get('genre')
        
        # AniList API query
        query = """
        query ($name: String, $genre: String) {
            Page {
                media(search: $name, genre: $genre, type: ANIME) {
                    title {
                        romaji
                    }
                    description
                    genres
                }
            }
        }
        """
        variables = {'name': name, 'genre': genre}
        url = 'https://graphql.anilist.co'
        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()
        media_list = data['data']['Page']['media']
        for media in media_list:
            # Extract title, description, and genres
            title = media['title']['romaji']
            description = media.get('description', 'No description available')
            genres = media.get('genres', [])

            # Save genres to the database (create them if they don't exist)
            genre_objects = []
            for genre_name in genres:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                genre_objects.append(genre)

            anime, created = Anime.objects.get_or_create(
                title=title,
                defaults={'description': description}
            )
            anime.genres.set(genre_objects)  
            anime.save()

        return Response(data, status=status.HTTP_200_OK)

class AnimeRecommendationView(APIView):
    def get(self, request):
        user_instance = User.objects.get(username="sac")
        try:
            preferences = UserPreferences.objects.get(user=user_instance)
        except UserPreferences.DoesNotExist:
            # If preferences don't exist, create a new one with default values
            preferences = UserPreferences.objects.create(user=user_instance)

        access_token = settings.ACCESS_TOKEN
        headers = {
                    'Authorization': f'Bearer {access_token}'
                }
        # Fetch anime recommendations based on user preferences
        favorite_genres = preferences.favorite_genres.all()
        watched_anime = preferences.watched_anime.all()

        query = """
        query GetAnimeRecommendations($genreIds: [String]) { Media(genre_in: $genreIds) { id title { romaji english native } recommendations { edges { node { id  rating  }   } } } }
        """
        variables={  "genreIds":"Romance"}
        #response = requests.post('https://graphql.anilist.co', json={'query': query})
        response = requests.post(
                        'https://graphql.anilist.co',
                        json={'query': query,'variables':variables},
                        headers=headers
                    )

        data = response.json()
        return Response(data, status=status.HTTP_200_OK)


class UserPreferencesView(APIView):
    # permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated

    def get(self, request):
        # Get user preferences if they exist
        try:
            preferences = UserPreferences.objects.get(user=request.user)
            serializer = UserPreferencesSerializer(preferences)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserPreferences.DoesNotExist:
            return Response({"detail": "Preferences not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Create or update user preferences
        # Data should include favorite_genres and watched_anime lists of IDs
        data = request.data
        try:
            preferences = UserPreferences.objects.get(user=request.user)
            serializer = UserPreferencesSerializer(preferences, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserPreferences.DoesNotExist:
            # If preferences do not exist, create new ones
            data['user'] = request.user.id
            serializer = UserPreferencesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # This endpoint allows the user to fully update their preferences
        data = request.data
        try:
            preferences = UserPreferences.objects.get(user=request.user)
            serializer = UserPreferencesSerializer(preferences, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserPreferences.DoesNotExist:
            return Response({"detail": "Preferences not found."}, status=status.HTTP_404_NOT_FOUND)

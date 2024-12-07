from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
     # Anime search endpoint
    path('anime/search/', views.AnimeSearchView.as_view(), name='anime_search'),

    # Recommendations based on user preferences
    path('anime/recommendations/', views.AnimeRecommendationView.as_view(), name='anime_recommendations'),

    # User preferences management (e.g., favorite genre)
    path('user/preferences/', views.UserPreferencesView.as_view(), name='user_preferences'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('anime/search/', views.AnimeSearchView.as_view(), name='anime_search'),
    path('anime/recommendations/', views.AnimeRecommendationView.as_view(), name='anime_recommendations'),
    path('user/preferences/', views.UserPreferencesView.as_view(), name='user_preferences'),
]
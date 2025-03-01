from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api import views
from api.views import ListBooks, DetailBooks, DetailAuthors, ListAuthors, DetailCategories, ListCategories, \
    LogoutAPIVIEW, CustomAuthToken

urlpatterns = [

    path('list_books', ListBooks.as_view(), name='books'),
    path('<int:pk>/books', DetailBooks.as_view(), name='books'),

    path('list_authors', ListAuthors.as_view(), name='authors'),
    path('<int:pk>/authors', DetailAuthors.as_view(), name='authors'),

    path('list_categories', ListCategories.as_view(), name='categories'),
    path('<int:pk>/categories', DetailCategories.as_view(), name='categories'),

    path('upload/', views.ImageViewSet.as_view(), name='upload'),

    path('token', obtain_auth_token, name='api_token_auth'),
    path('token/logout', LogoutAPIVIEW.as_view(), name='api_token_auth_logout'),
    path('token/custom', CustomAuthToken.as_view(), name='custom_api_token_auth'),



]

from django.urls import path
from .views import ListReposLanguages

urlpatterns = [
    path('list_languages/', ListReposLanguages.as_view(), name='list_languages')
]
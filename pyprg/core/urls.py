from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('author/', views.authors, name='list-authors')
]

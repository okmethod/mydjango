from django.urls import path
from . import views

urlpatterns = [
    path('reversi', views.reversi, name='reversi'),

]

from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('game',   views.GameModelViewSet)

urlpatterns = [
    path('', views.home, name='reversi_home'),
    path('game/<int:pk>/', views.game_room, name='reversi_game_room'),
    path('api/', include(router.urls)),
]

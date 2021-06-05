from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('game',   views.GameModelViewSet)
router.register('record', views.GameRecordViewSet)

urlpatterns = [
    path('', views.home, name='reversi_home'),
    path('game/<int:pk>/', views.game, name='reversi_game'),
    path('api/', include(router.urls)),
]

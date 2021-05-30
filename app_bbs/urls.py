from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/unpublish/', views.post_unpublish, name='post_unpublish'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:pk>/comment/allow/', views.comment_allow, name='comment_allow'),
    path('post/<int:pk>/comment/exclude/', views.comment_exclude, name='comment_exclude'),
    path('post/<int:pk>/comment/remove/', views.comment_remove, name='comment_remove'),

]

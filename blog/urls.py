from django.urls import path
from . import views
from .templatetags.post_tag import latest_post

urlpatterns = [
    path('', views.post_list, name='home'),
    path('about/', views.about, name='about'),
    path('detail/<int:post_id>', views.post_detail, name='detail'),
    path('new_post', views.Create_Post, name='new_post'),
    path('detail/<int:post_id>/update/', views.Update_Post, name='post-update'),
    path('detail/<int:post_id>/delete/', views.Delete_Post, name='post-delete'),
]
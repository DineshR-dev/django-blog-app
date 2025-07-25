"""
urls.py

Defines URL patterns for the blog app:
- Maps views for posts, authentication, dashboard, and password management
"""

from django.urls import path
from . import views

app_name = 'blog'

# URL patterns for the blog app
urlpatterns = [
    path("",views.index,name="index"),
    path('details/<str:slug>',views.details,name='details'),
    path('about',views.about,name='about'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('reset_password/<uidb64>/<token>', views.reset_password, name='reset_password'),
    path('logout',views.logout,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('new_post',views.new_post,name='new_post'),
    path('edit_post/<int:post_id>',views.edit_post,name='edit_post'),
    path('delete_post/<int:post_id>',views.delete_post,name='delete_post'),
    path('publish_post/<int:post_id>',views.publish_post,name='publish_post'),
]
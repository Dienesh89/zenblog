# urls.py for the home
from django.contrib import admin
from django.urls import path
from home import views
from home.views import handle_404

urlpatterns = [
    path('', views.index, name = "homepage"),  
    # signup and login
    path('signup/', views.signup, name = "signup"),
    path('login/', views.login, name = "login"),
    # about ,contact ,etc.
    path('single_post/', views.single_post, name = "single_post"),
    path('about/', views.about, name = "about"),
    path('category/', views.category, name = "category"),
    path('contact/', views.contact, name = "contact"),
    path('contact_submit/', views.contact_submit, name = "contact"),
    # handle signup login and logout
    path('handleSignup/', views.handleSignup, name = "handleSignup"),
    path('handleLogin/', views.handleLogin, name = "handleLogin"),
    path('logout/', views.logout, name = "logout"),
    # related to uploading post
    path('upload-post/',views.upload_post,name="upload_post"),
    path('edit-post/<str:slug>/', views.edit_post, name='edit_post'),
    path('post-images/',views.post_images),
    # related to showing the post to the user
    path('get-post',views.get_post),
    path('post/<str:slug>',views.show_post),
    # search
    path('search/',views.search),
    # category
    path('category/<str:category>',views.category)

]

handler404 = 'home.views.handle_404'
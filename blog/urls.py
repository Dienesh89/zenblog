from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from home.views import handle_404

handler404 = handle_404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    # signup and login
    path('signup/', include('home.urls')),
    path('login/', include('home.urls')),
    # about ,contact ,etc.
    path('single_post/', include('home.urls')),
    path('about/', include('home.urls')),
    path('category/', include('home.urls')),
    path('contact/', include('home.urls')),
    path('contact_submit/', include('home.urls')),
    # handle signup login and logout
    path('handleSignup/', include('home.urls')),
    path('handleLogin/', include('home.urls')),
    path('logout/',include('home.urls')),
    # related to uploading post
    path('upload-post/',include('home.urls')),
    path('edit-post/<str:slug>/', include('home.urls')),
    path('post-images/',include('home.urls')),
    # related to showing the post to the user
    path('get-post',include('home.urls')),
    path('post/<str:slug>',include('home.urls')),
    # search
    path('search/',include('home.urls')),
    # category
    path('category/<str:category>',include('home.urls')),
    
    # connecting to media
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from post.views import PostView

from user.views import UserView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sign_up', UserView.sign_up),
    path('sign_in', UserView.sign_in),

    path('post', PostView.as_view()),
    path('post/<int:id>', PostView.as_view()),
    path('post/detail/<int:id>', PostView.detail),
    path('post/like/<int:id>', PostView.like),
    path('post/search', PostView.search),
    path('post/comment/<int:id>', PostView.comment)
    # path('login', UserView)
]

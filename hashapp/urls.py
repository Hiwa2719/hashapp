"""hashapp URL Configuration

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
from django.urls import path, include
from sha256 import views as ShaViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', ShaViews.UserLoginView.as_view(), name='login'),
    path('register/', ShaViews.RegisterView.as_view(), name='register'),
    path('logout/', ShaViews.LogoutView.as_view(), name='logout'),
    path('account/', ShaViews.AccountView.as_view(), name='account'),
    path('delete-account/<int:pk>/', ShaViews.DeleteAccountView.as_view(), name='delete-account'),
    path('', include('sha256.urls')),
]

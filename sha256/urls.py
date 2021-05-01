from django.urls import path

from . import views


app_name = 'sha256'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('hash-gen/', views.HashGenerator.as_view(), name='hash-gen'),
    path('hash-list/', views.HashListView.as_view(), name='hash-list'),
]

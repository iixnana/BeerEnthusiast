from django.urls import path
from . import views

app_name = 'brewerytrip'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('<int:brewery_id>/', views.debug, name='debug'),
]

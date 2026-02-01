from django.urls import path
from . import views

urlpatterns = [
    path("slider/", views.SliderListView.as_view(), name="slider_api"),
]

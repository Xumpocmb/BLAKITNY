from django.urls import path
from . import views

urlpatterns = [
    path("slider/", views.SliderListView.as_view(), name="slider_api"),
    path("company-details/", views.CompanyDetailsView.as_view(), name="company_details_api"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("slider/", views.SliderListView.as_view(), name="slider_api"),
    path("company-details/", views.CompanyDetailsView.as_view(), name="company_details_api"),
    path("site-logo/", views.SiteLogoView.as_view(), name="site_logo_api"),
    path("social-networks/", views.SocialNetworkListView.as_view(), name="social_networks_api"),
    path("delivery-payment/", views.DeliveryPaymentView.as_view(), name="delivery_payment_api"),
    path("about-us/", views.AboutUsView.as_view(), name="about_us_api"),
]

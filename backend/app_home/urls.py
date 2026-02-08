from django.urls import path
from . import views

urlpatterns = [
    path("slider/", views.SliderListView.as_view(), name="slider_api"),
    path("company-details/", views.CompanyDetailsView.as_view(), name="company_details_api"),
    path("site-logo/", views.SiteLogoView.as_view(), name="site_logo_api"),
    path("social-networks/", views.SocialNetworkListView.as_view(), name="social_networks_api"),
    path("delivery-payment/", views.DeliveryPaymentView.as_view(), name="delivery_payment_api"),
    path("delivery-options/", views.DeliveryOptionListView.as_view(), name="delivery_options_api"),
    path("stores/", views.StoreListView.as_view(), name="stores_api"),
    path("phone-numbers/", views.PhoneNumberListView.as_view(), name="phone_numbers_api"),
    path("about-us/", views.AboutUsView.as_view(), name="about_us_api"),
    path("feedback/", views.FeedbackCreateView.as_view(), name="feedback_api"),
]

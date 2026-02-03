from rest_framework.response import Response
from rest_framework import generics
from .models import Slider, CompanyDetails
from .serializers import SliderSerializer, CompanyDetailsSerializer


class SliderListView(generics.ListAPIView):
    """
    API endpoint that returns active slider images
    """
    queryset = Slider.objects.filter(is_active=True)
    serializer_class = SliderSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"sliders": serializer.data})


class CompanyDetailsView(generics.RetrieveAPIView):
    """
    API endpoint that returns company details
    """
    queryset = CompanyDetails.objects.all()
    serializer_class = CompanyDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"company_details": serializer.data})

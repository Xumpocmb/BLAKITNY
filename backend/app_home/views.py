from rest_framework.response import Response
from rest_framework import generics
from .models import Slider
from .serializers import SliderSerializer


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

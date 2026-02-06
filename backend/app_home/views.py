from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Slider, CompanyDetails, SiteLogo, SocialNetwork, DeliveryPayment, AboutUs, Feedback
from .serializers import SliderSerializer, CompanyDetailsSerializer, SiteLogoSerializer, SocialNetworkSerializer, DeliveryPaymentSerializer, AboutUsSerializer, FeedbackSerializer


class SliderListView(generics.ListAPIView):
    """
    API endpoint that returns active slider images
    """
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
    serializer_class = CompanyDetailsSerializer

    def get_object(self):
        # Получаем первую запись из модели CompanyDetails
        return CompanyDetails.objects.first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({"company_details": serializer.data})
        else:
            # Возвращаем пустой ответ, если запись не найдена
            return Response({"company_details": None})


class SiteLogoView(generics.RetrieveAPIView):
    """
    API endpoint that returns site logo
    """
    permission_classes = [AllowAny]
    serializer_class = SiteLogoSerializer

    def retrieve(self, request, *args, **kwargs):
        logo_instance = self.get_object()
        serializer = self.get_serializer(logo_instance)

        # Если логотип не установлен, возвращаем текстовое значение
        if not logo_instance.logo:
            return Response({"site_name": "BLAKITNY"})
        else:
            return Response({"logo": serializer.data})

    def get_object(self):
        # Получаем или создаем единственный экземпляр логотипа
        return self.queryset.model.load()

    @property
    def queryset(self):
        from .models import SiteLogo
        return SiteLogo.objects.all()


class SocialNetworkListView(generics.ListAPIView):
    """
    API endpoint that returns social networks
    """
    permission_classes = [AllowAny]
    queryset = SocialNetwork.objects.filter(is_active=True)
    serializer_class = SocialNetworkSerializer


class DeliveryPaymentView(generics.RetrieveAPIView):
    """
    API endpoint that returns delivery and payment information
    """
    permission_classes = [AllowAny]
    serializer_class = DeliveryPaymentSerializer

    def get_object(self):
        # Получаем или создаем единственный экземпляр информации о доставке и оплате
        return self.queryset.model.load()

    @property
    def queryset(self):
        from .models import DeliveryPayment
        return DeliveryPayment.objects.all()


class AboutUsView(generics.RetrieveAPIView):
    """
    API endpoint that returns 'About Us' information
    """
    permission_classes = [AllowAny]
    serializer_class = AboutUsSerializer

    def get_object(self):
        # Получаем или создаем единственный экземпляр информации "О нас"
        return self.queryset.model.load()

    @property
    def queryset(self):
        from .models import AboutUs
        return AboutUs.objects.all()


class FeedbackCreateView(APIView):
    """
    API endpoint for creating feedback entries
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Ваше сообщение успешно отправлено!"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

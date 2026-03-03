from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Slider, CompanyDetails, SiteLogo, SocialNetwork, DeliveryPayment, AboutUs, Feedback, DeliveryOption, PhoneNumber, Store
from .serializers import SliderSerializer, CompanyDetailsSerializer, SiteLogoSerializer, SocialNetworkSerializer, DeliveryPaymentSerializer, AboutUsSerializer, FeedbackSerializer, DeliveryOptionSerializer, PhoneNumberSerializer, StoreSerializer


class SliderListView(generics.ListAPIView):
    """
    API endpoint that returns active slider images
    """
    permission_classes = [AllowAny]
    queryset = Slider.objects.filter(is_active=True)
    serializer_class = SliderSerializer

    def list(self, request, *args, **kwargs):
        """
        Возвращает список активных изображений для слайдера.
        
        Args:
            request: HTTP-запрос
            
        Returns:
            Response: JSON-ответ с массивом слайдеров
        """
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
        """
        Возвращает первый объект реквизитов компании.
        
        Returns:
            CompanyDetails: Объект с реквизитами компании или None
        """
        # Получаем первую запись из модели CompanyDetails
        return CompanyDetails.objects.first()

    def retrieve(self, request, *args, **kwargs):
        """
        Возвращает информацию о реквизитах компании.
        
        Args:
            request: HTTP-запрос
            
        Returns:
            Response: JSON-ответ с информацией о компании
        """
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
        """
        Возвращает информацию о логотипе сайта.
        
        Args:
            request: HTTP-запрос
            
        Returns:
            Response: JSON-ответ с информацией о логотипе сайта
        """
        logo_instance = self.get_object()
        serializer = self.get_serializer(logo_instance)

        # Если логотип не установлен, возвращаем текстовое значение
        if not logo_instance.logo:
            return Response({"site_name": "BLAKITNY"})
        else:
            return Response({"logo": serializer.data})

    def get_object(self):
        """
        Возвращает единственный экземпляр логотипа сайта.
        
        Returns:
            SiteLogo: Объект логотипа сайта
        """
        # Получаем или создаем единственный экземпляр логотипа
        return self.queryset.model.load()

    @property
    def queryset(self):
        """
        Возвращает queryset для модели SiteLogo.
        
        Returns:
            QuerySet: QuerySet для модели SiteLogo
        """
        from .models import SiteLogo
        return SiteLogo.objects.all()


class SocialNetworkListView(generics.ListAPIView):
    """
    API endpoint that returns social networks
    """
    permission_classes = [AllowAny]
    queryset = SocialNetwork.objects.filter(is_active=True)
    serializer_class = SocialNetworkSerializer

    def list(self, request, *args, **kwargs):
        """
        Возвращает список активных социальных сетей.
        
        Args:
            request: HTTP-запрос
            
        Returns:
            Response: JSON-ответ с массивом социальных сетей
        """
        return super().list(request, *args, **kwargs)


class DeliveryPaymentView(generics.RetrieveAPIView):
    """
    API endpoint that returns delivery and payment information
    """
    permission_classes = [AllowAny]
    serializer_class = DeliveryPaymentSerializer

    def get_object(self):
        """
        Возвращает единственный экземпляр информации о доставке и оплате.
        
        Returns:
            DeliveryPayment: Объект с информацией о доставке и оплате
        """
        # Получаем или создаем единственный экземпляр информации о доставке и оплате
        return self.queryset.model.load()

    @property
    def queryset(self):
        """
        Возвращает queryset для модели DeliveryPayment.
        
        Returns:
            QuerySet: QuerySet для модели DeliveryPayment
        """
        from .models import DeliveryPayment
        return DeliveryPayment.objects.all()


class AboutUsView(generics.RetrieveAPIView):
    """
    API endpoint that returns 'About Us' information
    """
    permission_classes = [AllowAny]
    serializer_class = AboutUsSerializer

    def get_object(self):
        """
        Возвращает единственный экземпляр информации "О нас".
        
        Returns:
            AboutUs: Объект с информацией "О нас"
        """
        # Получаем или создаем единственный экземпляр информации "О нас"
        return self.queryset.model.load()

    @property
    def queryset(self):
        """
        Возвращает queryset для модели AboutUs.
        
        Returns:
            QuerySet: QuerySet для модели AboutUs
        """
        from .models import AboutUs
        return AboutUs.objects.all()


class DeliveryOptionListView(generics.ListAPIView):
    """
    API endpoint that returns active delivery options
    """
    permission_classes = [AllowAny]
    queryset = DeliveryOption.objects.filter(is_active=True)
    serializer_class = DeliveryOptionSerializer

    def list(self, request, *args, **kwargs):
        """
        Возвращает список активных вариантов доставки.
        
        Args:
            request: HTTP-запрос
            
        Returns:
            Response: JSON-ответ с массивом вариантов доставки
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"delivery_options": serializer.data})


class StoreListView(generics.ListAPIView):
    """
    API endpoint that returns all stores
    """
    permission_classes = [AllowAny]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class PhoneNumberListView(generics.ListAPIView):
    """
    API endpoint that returns active phone numbers
    """
    permission_classes = [AllowAny]
    queryset = PhoneNumber.objects.filter(is_active=True)
    serializer_class = PhoneNumberSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"phone_numbers": serializer.data})


class FeedbackCreateView(APIView):
    """
    API endpoint for creating feedback entries
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Создает новую запись обратной связи.
        
        Args:
            request: HTTP-запрос с данными обратной связи
            
        Returns:
            Response: JSON-ответ с результатом операции
        """
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Ваше сообщение успешно отправлено!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

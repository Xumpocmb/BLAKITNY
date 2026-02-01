from django.test import TestCase
from .models import Category, Subcategory, Fabric, Product
from .serializers import ProductSerializer, ProductListSerializer


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", description="Test Description")
        self.subcategory = Subcategory.objects.create(
            name="Test Subcategory",
            description="Test Description",
            category=self.category
        )
        self.fabric = Fabric.objects.create(name="Test Fabric")

    def test_product_binding_field(self):
        """Test that the binding field can be added to a product"""
        product = Product.objects.create(
            category=self.category,
            subcategory=self.subcategory,
            name="Test Product",
            description="Test Description",
            binding="Твердый переплет",  # Hard binding in Russian
            fabric_type=self.fabric
        )

        self.assertEqual(product.binding, "Твердый переплет")
        self.assertIsInstance(product.binding, str)

    def test_product_serializer_includes_binding(self):
        """Test that the product serializer includes the binding field"""
        product = Product.objects.create(
            category=self.category,
            subcategory=self.subcategory,
            name="Test Product",
            description="Test Description",
            binding="Мягкий переплет",  # Soft binding in Russian
            fabric_type=self.fabric
        )

        serializer = ProductSerializer(product)
        self.assertIn('binding', serializer.data)
        self.assertEqual(serializer.data['binding'], "Мягкий переплет")

    def test_product_list_serializer_includes_binding(self):
        """Test that the product list serializer includes the binding field"""
        product = Product.objects.create(
            category=self.category,
            subcategory=self.subcategory,
            name="Test Product",
            description="Test Description",
            binding="Спиральный переплет",  # Spiral binding in Russian
            fabric_type=self.fabric
        )

        serializer = ProductListSerializer(product)
        self.assertIn('binding', serializer.data)
        self.assertEqual(serializer.data['binding'], "Спиральный переплет")

    def test_product_picture_title_field(self):
        """Test that the picture_title field can be added to a product"""
        product = Product.objects.create(
            category=self.category,
            subcategory=self.subcategory,
            name="Test Product",
            description="Test Description",
            binding="Твердый переплет",
            picture_title="Красивый узор",  # Beautiful pattern in Russian
            fabric_type=self.fabric
        )

        self.assertEqual(product.picture_title, "Красивый узор")
        self.assertIsInstance(product.picture_title, str)

    def test_product_serializer_includes_picture_title(self):
        """Test that the product serializer includes the picture_title field"""
        product = Product.objects.create(
            category=self.category,
            subcategory=self.subcategory,
            name="Test Product",
            description="Test Description",
            picture_title="Узор цветов",  # Flower pattern in Russian
            fabric_type=self.fabric
        )

        serializer = ProductSerializer(product)
        self.assertIn('picture_title', serializer.data)
        self.assertEqual(serializer.data['picture_title'], "Узор цветов")

    def test_product_list_serializer_includes_picture_title(self):
        """Test that the product list serializer includes the picture_title field"""
        product = Product.objects.create(
            category=self.category,
            subcategory=self.subcategory,
            name="Test Product",
            description="Test Description",
            picture_title="Геометрический дизайн",  # Geometric design in Russian
            fabric_type=self.fabric
        )

        serializer = ProductListSerializer(product)
        self.assertIn('picture_title', serializer.data)
        self.assertEqual(serializer.data['picture_title'], "Геометрический дизайн")

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Subcategory, Fabric, Product, ProductImage
from .serializers import ProductSerializer, ProductListSerializer, ProductImageSerializer


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


class ProductImageModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", description="Test Description")
        self.subcategory = Subcategory.objects.create(
            name="Test Subcategory",
            description="Test Description",
            category=self.category
        )
        self.fabric = Fabric.objects.create(name="Test Fabric")
        self.product = Product.objects.create(
            category=self.category,
            subcategory=self.subcategory,
            name="Test Product",
            description="Test Description",
            binding="Твердый переплет",
            picture_title="Красивый узор",
            fabric_type=self.fabric
        )

    def test_product_image_creation(self):
        """Test that a product image can be created and associated with a product"""
        # Create a simple image file for testing
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )

        product_image = ProductImage.objects.create(
            product=self.product,
            image=image,
            is_active=True
        )

        self.assertEqual(product_image.product, self.product)
        self.assertTrue(product_image.is_active)
        self.assertIsNotNone(product_image.image)

    def test_product_image_serializer(self):
        """Test that the product image serializer works correctly"""
        # Create a simple image file for testing
        image = SimpleUploadedFile(
            name='test_image2.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )

        product_image = ProductImage.objects.create(
            product=self.product,
            image=image,
            is_active=True
        )

        serializer = ProductImageSerializer(product_image)
        self.assertIn('id', serializer.data)
        self.assertIn('image', serializer.data)
        self.assertIn('is_active', serializer.data)
        self.assertIn('created_at', serializer.data)
        self.assertEqual(serializer.data['is_active'], True)

    def test_product_serializer_includes_images(self):
        """Test that the product serializer includes the images field"""
        # Create a simple image file for testing
        image = SimpleUploadedFile(
            name='test_product_image.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )

        product_image = ProductImage.objects.create(
            product=self.product,
            image=image,
            is_active=True
        )

        serializer = ProductSerializer(self.product)
        self.assertIn('images', serializer.data)
        self.assertEqual(len(serializer.data['images']), 1)
        self.assertEqual(serializer.data['images'][0]['id'], product_image.id)
        self.assertEqual(serializer.data['images'][0]['is_active'], True)

    def test_product_list_serializer_includes_images(self):
        """Test that the product list serializer includes the images field"""
        # Create a simple image file for testing
        image = SimpleUploadedFile(
            name='test_list_image.jpg',
            content=b'test image content',
            content_type='image/jpeg'
        )

        product_image = ProductImage.objects.create(
            product=self.product,
            image=image,
            is_active=True
        )

        serializer = ProductListSerializer(self.product)
        self.assertIn('images', serializer.data)
        self.assertEqual(len(serializer.data['images']), 1)
        self.assertEqual(serializer.data['images'][0]['id'], product_image.id)
        self.assertEqual(serializer.data['images'][0]['is_active'], True)

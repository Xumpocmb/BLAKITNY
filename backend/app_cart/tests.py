from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from app_catalog.models import Category, Subcategory, Size, Product, ProductVariant
from app_cart.models import Cart, CartItem


class CartTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test category, subcategory, size, and product
        self.category = Category.objects.create(name='Test Category', is_active=True)
        self.subcategory = Subcategory.objects.create(name='Test Subcategory', category=self.category, is_active=True)
        self.size = Size.objects.create(name='M', is_active=True)
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            subcategory=self.subcategory,
            is_active=True
        )
        
        # Create test product variant
        self.product_variant = ProductVariant.objects.create(
            product=self.product,
            size=self.size,
            price=100.00,
            is_active=True
        )
        
        # Create API client
        self.client = APIClient()
        
        # Authenticate using JWT token
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        
    def test_cart_creation(self):
        """Test that a cart is created for a user"""
        cart, created = Cart.objects.get_or_create(user=self.user)
        self.assertTrue(created)
        self.assertEqual(cart.user, self.user)
        
    def test_add_to_cart(self):
        """Test adding items to cart"""
        response = self.client.post('/api/cart/add/', {
            'product_variant_id': self.product_variant.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 201)
        
        # Check that cart item was created
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        cart_item = cart.items.first()
        self.assertEqual(cart_item.product_variant, self.product_variant)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.total_price, 200.00)  # 2 * 100
        
    def test_get_cart(self):
        """Test retrieving cart details"""
        # Add an item to cart first
        cart, created = Cart.objects.get_or_create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product_variant=self.product_variant,
            quantity=3
        )
        
        # Get cart details
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['total_items'], 3)
        self.assertEqual(float(data['total_price']), 300.00)
        
    def test_update_cart_item(self):
        """Test updating cart item quantity"""
        # Add an item to cart first
        cart, created = Cart.objects.get_or_create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product_variant=self.product_variant,
            quantity=1
        )
        
        # Update quantity
        response = self.client.put(f'/api/cart/update/{cart_item.id}/', {
            'quantity': 5
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Refresh from db
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)
        
    def test_remove_from_cart(self):
        """Test removing item from cart"""
        # Add an item to cart first
        cart, created = Cart.objects.get_or_create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product_variant=self.product_variant,
            quantity=2
        )
        
        # Remove item
        response = self.client.delete(f'/api/cart/remove/{cart_item.id}/')
        self.assertEqual(response.status_code, 204)
        
        # Check that item was removed
        self.assertEqual(cart.items.count(), 0)
        
    def test_clear_cart(self):
        """Test clearing entire cart"""
        # Add items to cart
        cart, created = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(
            cart=cart,
            product_variant=self.product_variant,
            quantity=2
        )
        
        # Clear cart
        response = self.client.delete('/api/cart/clear/')
        self.assertEqual(response.status_code, 204)
        
        # Check that all items were removed
        self.assertEqual(cart.items.count(), 0)
from django.test import TestCase
from django.contrib.auth.models import User
from app_home.models import DeliveryOption
from app_catalog.models import Category, Subcategory, Size, Product, ProductVariant
from app_cart.models import Cart, CartItem
from app_order.models import Order, OrderItem
from app_order.logic import create_order_from_cart, update_order_status, get_user_orders, get_order_details, cancel_order


class OrderLogicTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Создаем вариант доставки
        self.delivery_option = DeliveryOption.objects.create(
            name='Доставка курьером',
            is_active=True
        )

        # Создаем товары
        self.category = Category.objects.create(name='Тестовая категория', is_active=True)
        self.subcategory = Subcategory.objects.create(
            name='Тестовая подкатегория', 
            category=self.category, 
            is_active=True
        )
        self.size = Size.objects.create(name='M', is_active=True)
        self.product = Product.objects.create(
            name='Тестовый товар',
            category=self.category,
            subcategory=self.subcategory,
            is_active=True
        )
        self.product_variant = ProductVariant.objects.create(
            product=self.product,
            size=self.size,
            price=100.00,
            is_active=True
        )

        # Создаем корзину и добавляем товар
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product_variant=self.product_variant,
            quantity=2
        )

    def test_create_order_from_cart(self):
        """Тест создания заказа из корзины"""
        order = create_order_from_cart(
            user=self.user,
            cart=self.cart,
            delivery_option_id=self.delivery_option.id,
            first_name='Иван',
            last_name='Иванов',
            email='ivan@example.com',
            phone='+79991234567',
            address='ул. Тестовая, д. 1'
        )

        # Проверяем, что заказ создан
        self.assertIsInstance(order, Order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.first_name, 'Иван')
        self.assertEqual(order.last_name, 'Иванов')
        self.assertEqual(order.email, 'ivan@example.com')
        self.assertEqual(order.phone, '+79991234567')
        self.assertEqual(order.address, 'ул. Тестовая, д. 1')
        self.assertEqual(order.delivery_option, self.delivery_option)
        self.assertEqual(order.total_amount, 200.00)  # 2 шт. * 100 руб.
        self.assertEqual(order.status, 'pending')

        # Проверяем, что элементы заказа созданы
        self.assertEqual(order.order_items.count(), 1)
        order_item = order.order_items.first()
        self.assertEqual(order_item.product_variant, self.product_variant)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, 100.00)

        # Проверяем, что корзина очищена
        self.assertEqual(self.cart.items.count(), 0)

    def test_update_order_status(self):
        """Тест обновления статуса заказа"""
        order = create_order_from_cart(
            user=self.user,
            cart=self.cart,
            delivery_option_id=self.delivery_option.id,
            first_name='Иван',
            last_name='Иванов',
            email='ivan@example.com',
            phone='+79991234567',
            address='ул. Тестовая, д. 1'
        )

        # Обновляем статус заказа
        success = update_order_status(order.id, 'confirmed')
        self.assertTrue(success)

        # Проверяем, что статус обновился
        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')

    def test_cancel_order(self):
        """Тест отмены заказа"""
        order = create_order_from_cart(
            user=self.user,
            cart=self.cart,
            delivery_option_id=self.delivery_option.id,
            first_name='Иван',
            last_name='Иванов',
            email='ivan@example.com',
            phone='+79991234567',
            address='ул. Тестовая, д. 1'
        )

        # Отменяем заказ
        success = cancel_order(order.id)
        self.assertTrue(success)

        # Проверяем, что статус стал cancelled
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')

    def test_get_user_orders(self):
        """Тест получения заказов пользователя"""
        # Создаем первого пользователя и его заказ
        order1 = create_order_from_cart(
            user=self.user,
            cart=self.cart,
            delivery_option_id=self.delivery_option.id,
            first_name='Иван',
            last_name='Иванов',
            email='ivan@example.com',
            phone='+79991234567',
            address='ул. Тестовая, д. 1'
        )

        # Создаем второго пользователя и его корзину для второго заказа
        user2 = User.objects.create_user(username='testuser2', password='testpass')
        cart2 = Cart.objects.create(user=user2)
        cart_item2 = CartItem.objects.create(
            cart=cart2,
            product_variant=self.product_variant,
            quantity=1
        )

        order2 = create_order_from_cart(
            user=user2,
            cart=cart2,
            delivery_option_id=self.delivery_option.id,
            first_name='Петр',
            last_name='Петров',
            email='petr@example.com',
            phone='+79997654321',
            address='ул. Тестовая, д. 2'
        )

        # Получаем заказы первого пользователя
        user_orders = get_user_orders(self.user)
        self.assertEqual(user_orders.count(), 1)
        self.assertIn(order1, user_orders)
        self.assertNotIn(order2, user_orders)

    def test_get_order_details(self):
        """Тест получения деталей заказа"""
        order = create_order_from_cart(
            user=self.user,
            cart=self.cart,
            delivery_option_id=self.delivery_option.id,
            first_name='Иван',
            last_name='Иванов',
            email='ivan@example.com',
            phone='+79991234567',
            address='ул. Тестовая, д. 1'
        )

        # Получаем детали заказа
        retrieved_order = get_order_details(order.id)
        self.assertEqual(retrieved_order.id, order.id)
        self.assertEqual(retrieved_order.first_name, 'Иван')
        self.assertEqual(retrieved_order.last_name, 'Иванов')
        self.assertEqual(retrieved_order.email, 'ivan@example.com')
        self.assertEqual(retrieved_order.phone, '+79991234567')
        self.assertEqual(retrieved_order.address, 'ул. Тестовая, д. 1')
        self.assertEqual(retrieved_order.delivery_option, self.delivery_option)
        self.assertEqual(retrieved_order.total_amount, 200.00)
        self.assertEqual(retrieved_order.status, 'pending')
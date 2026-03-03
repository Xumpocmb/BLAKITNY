from django.test import TestCase
from .models import Store


class StoreTestCase(TestCase):
    def test_store_creation(self):
        """Тест создания магазина"""
        store = Store.objects.create(
            city="Москва",
            address="ул. Тверская, д. 1",
            phone="+74951234567",
            work_schedule="Пн-Вс: 10:00-20:00"
        )
        self.assertEqual(store.city, "Москва")
        self.assertEqual(store.address, "ул. Тверская, д. 1")
        self.assertEqual(store.phone, "+74951234567")
        self.assertEqual(store.work_schedule, "Пн-Вс: 10:00-20:00")
        self.assertEqual(str(store), "Москва, ул. Тверская, д. 1")

    def test_store_without_phone(self):
        """Тест создания магазина без телефона"""
        store = Store.objects.create(
            city="Санкт-Петербург",
            address="Невский проспект, д. 2",
            work_schedule="Пн-Вс: 09:00-21:00"
        )
        self.assertEqual(store.city, "Санкт-Петербург")
        self.assertEqual(store.address, "Невский проспект, д. 2")
        self.assertIsNone(store.phone)
        self.assertEqual(store.work_schedule, "Пн-Вс: 09:00-21:00")

    def test_store_ordering(self):
        """Тест сортировки магазинов"""
        store1 = Store.objects.create(
            city="Москва",
            address="ул. Арбат, д. 10",
            work_schedule="Пн-Вс: 10:00-20:00"
        )
        store2 = Store.objects.create(
            city="Санкт-Петербург",
            address="Невский проспект, д. 5",
            work_schedule="Пн-Вс: 09:00-21:00"
        )
        store3 = Store.objects.create(
            city="Москва",
            address="Тверская ул., д. 1",
            work_schedule="Пн-Вс: 10:00-20:00"
        )

        stores = Store.objects.all()
        # Проверяем, что сортировка происходит по городу, затем по адресу
        self.assertEqual(stores[0].city, "Москва")
        self.assertEqual(stores[0].address, "Тверская ул., д. 1")
        self.assertEqual(stores[1].address, "ул. Арбат, д. 10")
        self.assertEqual(stores[2].city, "Санкт-Петербург")
from django.db import models
from datetime import timedelta
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    emaile = models.EmailField()
    password = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f'Username: {self.name}, email: {self.emaile}, age: {self.age}'

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date_order = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.id} by {self.client.name}"


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def create_client(name, email, phone_number, address):
    return Client.objects.create(name=name, email=email, phone_number=phone_number, address=address)

def create_product(name, description, price, quantity):
    return Product.objects.create(name=name, description=description, price=price, quantity=quantity)

def create_order(client, products, total_amount):
    order = Order.objects.create(client=client, total_amount=total_amount)
    order.products.set(products)
    return order


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f'Name: {self.name}, email: {self.email}'

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'Title if {self.title}'


class Photo(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


def get_recent_orders(client_instance):
    """
    Возвращает список заказанных клиентом товаров из всех его заказов с сортировкой по времени.
    :param client_instance: Экземпляр клиента.
    :return: Список товаров.
    """
    end_date = timezone.now()
    start_date_7_days = end_date - timedelta(days=7)
    start_date_30_days = end_date - timedelta(days=30)
    start_date_365_days = end_date - timedelta(days=365)

    # Получаем заказы клиента за последние 7 дней
    recent_orders_7_days = Order.objects.filter(order_date__range=(start_date_7_days, end_date), client=client_instance)

    # Получаем заказы клиента за последние 30 дней
    recent_orders_30_days = Order.objects.filter(order_date__range=(start_date_30_days, end_date), client=client_instance)

    # Получаем заказы клиента за последний год
    recent_orders_365_days = Order.objects.filter(order_date__range=(start_date_365_days, end_date), client=client_instance)

    # Объединяем товары из всех заказов
    all_items = set()
    for order in recent_orders_7_days | recent_orders_30_days | recent_orders_365_days:
        all_items.update(order.items.all())

    return list(all_items)
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Name of category')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Pictures')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True, blank=True,
                               verbose_name='Category',
                               related_name='subcategories')

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://cdn1.ozone.ru/s3/multimedia-0/6073071648.jpg'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Category: pk={self.pk}, title={self.title}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Name of product')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Price')
    quantity = models.IntegerField(default=0, verbose_name='Quantity')
    description = models.TextField(default='Soon...', verbose_name='Content')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.FloatField(verbose_name='Size')
    color = models.CharField(max_length=40, verbose_name='Color')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return 'https://cdn1.ozone.ru/s3/multimedia-0/6073071648.jpg'
        else:
            return 'https://cdn1.ozone.ru/s3/multimedia-0/6073071648.jpg'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Product: pk={self.pk}, title={self.title}, price={self.price}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Picture'
        verbose_name_plural = 'Pictures'


class Review(models.Model):
    text = models.TextField(verbose_name='Typing')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


# Produktga like bosish
class FavouriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Person')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Favourite product'
        verbose_name_plural = 'Favourite products'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Customer')
    name = models.CharField(max_length=200, verbose_name='Name of customer')
    user_name = models.CharField(max_length=200, verbose_name='Name of customer', default='')
    last_name = models.CharField(max_length=200, verbose_name='Lastname of customer', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Customer')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of order')
    shipping = models.BooleanField(default=True, verbose_name='Shipping')

    def __str__(self):
        return str(self.pk) + ' '

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    # Zakazga chiqqan produktlarni pulini xisoblidi
    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])  # Produktlar summasi umumiysi
        return total_price

    # Zakazga chiqqan produktlarni sonini xisoblidi
    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])  # Produktlar sonini umumiysi
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Product')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Order')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Quantity')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product in order'
        verbose_name_plural = 'Product in orders'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    phone = PhoneNumberField(max_length=200, verbose_name='Phone number')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Address of shipping'
        verbose_name_plural = 'Address of shippings'




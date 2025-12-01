from .models import Product, OrderProduct, Order, Customer


# Savatga qoshish va udalit qilish uchun javob beradigan class

class CartForAuthenticatedUser:
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user

        if product_id and action:
            self.add_or_delete(product_id, action)

    # Savatdagi malumotlarni qaytaradi
    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(
            user=self.user
        )
        order, created = Order.objects.get_or_create(
            customer=customer)  # Oldin registerdan otkan bolsa savatini olib beradi! Bomasa yaratadi!
        order_products = order.orderproduct_set.all()  # Zakaz qilingan produktlani ovoladi hamasini

        cart_total_quantity = order.get_cart_total_quantity  # Hamma produktlani sonini oladi
        cart_total_price = order.get_cart_total_price  # Hamma produktlani summasini yigadi!

        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'order': order,
            'products': order_products
        }

    def add_or_delete(self, product_id, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity > 0:
            order_product.quantity += 1
            product.quantity -= 1
        else:
            order_product.quantity -= 1
            product.quantity += 1

        product.save()
        order_product.save()

        if order_product.quantity <= 0:  # Agar 0 dan tushib ketsa savat tozalanib qoladi !
            order_product.delete()

    def clear(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for product in order_products:
            product.delete()
        order.delete()


def get_cart_data(request):
    cart = CartForAuthenticatedUser(request)
    cart_info = cart.get_cart_info()

    return {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'cart_total_price': cart_info['cart_total_price'],
        'order': cart_info['order'],
        'products': cart_info['products']
    }

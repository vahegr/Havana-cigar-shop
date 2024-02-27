from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from account.models import User


class Category(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.id, self.slug])


class StateOfProduct(models.Model):
    title = models.CharField(max_length=100)


class Product(models.Model):
    category = models.ManyToManyField(Category)
    state_of_product = models.ManyToManyField(StateOfProduct)
    image = models.ImageField(upload_to='product/images')
    title = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    single_cigar_price = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    description = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    allowed = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return f'{self.title} - {self.price}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=250)
    email_address = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=250)
    post_code = models.CharField(max_length=250)
    total_price = models.DecimalField(max_digits=60, decimal_places=2, default=0)
    details_text = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.created_at}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    state_of_product = models.CharField(max_length=100)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=60, decimal_places=2)

    def __str__(self):
        return f'{self.product.title} - {self.state_of_product} - {self.quantity} - {self.price}'

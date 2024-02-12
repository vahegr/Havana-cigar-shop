from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('videos:category detail', args=[self.id, self.slug])


class Product(models.Model):
    category = models.ManyToManyField(Category)
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

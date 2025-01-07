from django.db import models


from main.models import CommonModel


class Category(CommonModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category', null=True, blank=True)


    class Meta:
        db_table = 'items_category'
        verbose_name ='category'
        verbose_name_plural='categories'
        ordering = ('id',)

    def __str__(self):
        return self.name
    

class Brand(CommonModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand', null=True, blank=True)


    class Meta:
        db_table = 'items_brand'
        verbose_name ='brand'
        verbose_name_plural='brands'
        ordering = ('id',)

    def __str__(self):
        return self.name
    


class Color(CommonModel):
    color = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'items_color'
        verbose_name ='color'
        verbose_name_plural='colors'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class CustomSpecification(CommonModel):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    value = models.TextField()

    class Meta:
        db_table = 'items_specification'
        verbose_name ='specification'
        verbose_name_plural='specifications'
        ordering = ('-id',)

    def __str__(self):
        return self.name
    




class Product(CommonModel):
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    mainimage = models.ImageField(upload_to='products',blank=True, null=True)
    regular_price = models.FloatField()
    sale_price = models.FloatField(blank=True, null=True)
    offer_percentage = models.IntegerField(blank=True, null=True)
    video = models.FileField(upload_to='products', blank=True, null=True)
    specifications = models.ManyToManyField(CustomSpecification, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.FloatField(default=0)
    stock = models.IntegerField(default=0, blank=True, null=True)
    delivery_title = models.CharField(max_length=100, blank=True, null=True)
    delivery_duration = models.CharField(max_length=100, blank=True, null=True)
    garantee_title = models.CharField(max_length=100, blank=True, null=True)
    garantee_time = models.CharField(max_length=100, blank=True, null=True)
    sales_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'items_product'
        verbose_name ='product'
        verbose_name_plural='products'
        ordering = ('-id',)

    def __str__(self):
        return self.name




class Option(CommonModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE, blank=True, null=True)  # E.g., 'Purple'
    ram = models.CharField(max_length=50, blank=True, null=True)  # e.g., '8GB'
    storage = models.CharField(max_length=50, blank=True, null=True)  # e.g., '128GB'
    regular_price = models.FloatField()
    sale_price = models.FloatField()
    stock = models.IntegerField(default=0)  # Available stock for this variant

    class Meta:
        db_table = 'items_option'
        verbose_name ='option'
        verbose_name_plural='options'
        ordering = ('id',)

    def __str__(self):
        return self.name
    



class ProductImage(CommonModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    variant = models.ManyToManyField(Option, blank=True, null=True, related_name="images")
    image = models.ImageField(upload_to='product_images')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "items_productimages"
        verbose_name = "productimage"
        verbose_name_plural = "productimages"
        ordering = ["id"]

    def __str__(self):
        return self.alt_text
    


class Ram(CommonModel):
    value = models.CharField(max_length=50)

    class Meta:
        db_table = 'items_ram'
        verbose_name ='ram'
        verbose_name_plural='rams'
        ordering = ('-id',)

    def __str__(self):
        return self.value
    

class Storage(CommonModel):
    value = models.CharField(max_length=50)

    class Meta:
        db_table = 'items_storage'
        verbose_name ='storage'
        verbose_name_plural='storages'
        ordering = ('-id',)

    def __str__(self):
        return self.value


class IconImage(CommonModel):
    image = models.ImageField(upload_to="products")
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "items_iconimages"
        verbose_name = "iconimage"
        verbose_name_plural = "iconimages"
        ordering = ["id"]

    def __str__(self):
        return self.name
    


class Spec(CommonModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(IconImage, on_delete=models.CASCADE)
    detail = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "items_specs"
        verbose_name = "spec"
        verbose_name_plural = "specs"
        ordering = ["id"]

    def __str__(self):
        return self.detail
    



from distutils.command.upload import upload
from unicodedata import category
from django.db import models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=230,default='',null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to = "products/")

    @staticmethod
    def get_all_products_by_id(ids):
        return Product.objects.filter(id__in = ids) #to match a list we use id__in
        #this means all the ids that list contains are filtered out and returned

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_category_by_id(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)

        else:
            return Product.get_all_products()

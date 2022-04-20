import email
from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    address1 = models.CharField(max_length=250, default="", blank=True)
    address2 = models.CharField(max_length=250, default="", blank=True)
    address3 = models.CharField(max_length=250, default="", blank=True)

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False

    @staticmethod
    def user_name(id):
        print("id",id)
        



    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True
        return False

    @staticmethod
    def get_customers_by_id(customer_id):
        return Customer.objects.filter(id = customer_id)

    @staticmethod
    def get_address_by_id(customer_id):
        if Customer.objects.filter(id = customer_id):
            return Customer.address1

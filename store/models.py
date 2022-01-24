from django.db import models
import datetime
# Create your models here.

class Category(models.Model):
	name=models.CharField(max_length=20)

	def __str__(self):
		return self.name

	
class Product(models.Model):
	name=models.CharField(max_length=256)
	price=models.IntegerField(default=0)
	category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
	description=models.CharField(max_length=300,default='',null=True,blank=True)
	image=models.ImageField(upload_to='upload/productimg/')


class Customer(models.Model):
	first_name=models.CharField(max_length=30)
	last_name=models.CharField(max_length=30)
	phone=models.IntegerField()
	email=models.EmailField()
	password=models.CharField(max_length=400)

	def __str__(self):
		return self.first_name


class Order(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
	quantity=models.IntegerField(default=1)
	price=models.IntegerField()
	address=models.CharField(max_length=250,default="",blank=True)
	phone=models.CharField(max_length=25)
	date=models.DateField(default=datetime.datetime.today)
	status=models.BooleanField(default=False)

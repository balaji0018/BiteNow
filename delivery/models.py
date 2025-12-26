from django.db import models

# Create your models here.
class customers(models.Model):
    username = models.CharField( max_length=10)
    password = models.CharField( max_length=15)
    email = models.CharField( max_length=20)
    mobile = models.CharField( max_length=10)
    address = models.CharField( max_length=50)

def __str__(self):
    return self.username


class Restaurant(models.Model):
    name = models.CharField(max_length = 20)
    picture = models.URLField(max_length = 200, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6ElrC4JMiIAw6G9T2aDFN0lXyL-g7zbZRaw&s')
    cuisine = models.CharField(max_length = 200)
    rating = models.FloatField()

class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name = "items")
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    price = models.FloatField()
    vegeterian = models.BooleanField(default=False)
    picture = models.URLField(max_length = 400, default='https://www.indiafilings.com/learn/wp-content/uploads/2024/08/How-to-Start-Food-Business.jpg')

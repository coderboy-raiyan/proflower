from django.db import models
from django.contrib.auth.models import User
from .constants import RATINGS
from cloudinary.models import CloudinaryField
# Create your models here.


class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=500, unique=True, null=True)

    def __str__(self) -> str:
        return self.slug


class FlowerModel(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField()
    image = CloudinaryField('image')
    quantity = models.IntegerField(default = 0)
    categories = models.ManyToManyField(
        CategoryModel, related_name="flowers")
    borrowing_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.title


class ReviewModel(models.Model):
    flower = models.ForeignKey(
        FlowerModel, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="reviews", on_delete=models.CASCADE)
    content = models.TextField()
    ratings = models.IntegerField(choices=RATINGS)
    timestamps = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username

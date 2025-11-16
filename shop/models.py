from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from django.db.models import Model


# Create your models here
class CustomUserManager(BaseUserManager):
    def create_user(self,email, password=None, **kwargs):
        if not email:
            raise ValueError("Emailni kiriting ")
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_superuser",True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be True is_staff")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be True is_superuser")

        return self.create_user(email=email, password=password, **kwargs)

class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=80)
    message = models.TextField()

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.first_name

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=3)
    quantity = models.IntegerField(default=1)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_first_image(self):
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return "https://amur-gidravlika.ru/wp-content/uploads/2022/07/product-not-found-262.jpg"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title



class Gallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

class Like(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='likes')

    def __str__(self):
        return f"{self.user.email} - {self.product.title}"

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"


class Comment(models.Model):
    product = models.ForeignKey(
        Product,on_delete=models.CASCADE,related_name='comments'
    )
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product.title}"




from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryImage


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', default='placeholder', transformation=[
  {'gravity': "face", 'height': 200, 'width': 200, 'crop': "thumb"},
  {'radius': "max"},
  {'fetch_format': "auto"}])


    def __str__(self):
        return f'{self.user.username} Profile'

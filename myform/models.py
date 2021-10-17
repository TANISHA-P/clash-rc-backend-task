from django.db import models
from django.contrib.auth.models import User

gen = (
    ('M','MALE'),
    ('F','FEMALE'),
    ('O','Other'),
    ('N','Prefer not say')
)
# Create your models here.
class Registration(models.Model):
    user_info = models.OneToOneField(User,on_delete = models.CASCADE)
    bday = models.DateField()
    mobile = models.IntegerField()
    gender = models.CharField(choices = gen, max_length = 1)
    

    def __str__(self):
        return f"{self.user_info.username}"
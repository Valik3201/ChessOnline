from django.contrib.auth.models import  AbstractUser
from django.db import models
from django.conf import settings
from datetime import datetime
# Create your models here.

class Game(models.Model):
    white_player= models.IntegerField(blank=True)
    black_player=models.IntegerField()
    win_color=models.CharField(max_length=20)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    def __str__(self):
        return (str(self.date)+' - white player(%s), black player(%s),win -%s'%(self.white_player,
                                                                           self.black_player,
                                                                           self.win_color))



class User(AbstractUser):
    avatar = models.ImageField(blank=True,upload_to='avatars')
    rating=models.IntegerField(default=1200)
    games=models.ManyToManyField(Game,blank=True)
    followers=models.ManyToManyField('self',blank=True)
    following=models.ManyToManyField('self',blank=True)
    victorys=models.IntegerField(default=0)
    defeats=models.IntegerField(default=0)
    draws=models.IntegerField(default=0)








# Create your models here.














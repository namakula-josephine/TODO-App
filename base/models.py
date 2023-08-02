from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True,null=True)
    time =models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering =['complete']
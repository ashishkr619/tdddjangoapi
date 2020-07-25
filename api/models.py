from django.db import models
from django.contrib.auth import get_user_model




class Content(models.Model):
  title = models.CharField(max_length=30,default="Title")
  owner = models.ForeignKey(get_user_model(),related_name="content",on_delete=models.CASCADE)
  body = models.TextField(max_length=300,default="New body")
  summary = models.CharField(max_length=60,default="Summary")
  category = models.ManyToManyField('Category',related_name='category')

  def __str__(self):
    return str(self.title)


class Category(models.Model):
  title = models.CharField(max_length=30,default="category")

  def __str__(self):
    return self.title

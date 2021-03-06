from django.db import models

# Create your models here.

class ArticleGen(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    time = models.DateTimeField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

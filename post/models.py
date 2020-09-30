from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


# Create your models here.
from article.utils import unique_slug_generator


class Article(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    time = models.DateTimeField()
    slug = models.SlugField(max_length=250, null=True, blank=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender = Article)


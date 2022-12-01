from django.conf import settings
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django.template.defaultfilters import slugify
import os
from django.core.files.uploadedfile import SimpleUploadedFile


User = settings.AUTH_USER_MODEL

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

TYPE_CHOICES = [
    ('Student', 'Student'),
    ('Educator', 'Educator'),
]


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("articles_detail", kwargs={"slug": self.slug})


class Article(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('ArticleSeries', slugify(self.slug), instance)
        return None

    title = models.CharField(max_length=255)
    updated_on = models.DateTimeField(auto_now=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.IntegerField(choices=STATUS, default=1)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default='Generic')
    slug = AutoSlugField(populate_from=lambda instance: instance.title,
                         unique_with=['author', 'created_on', 'category'],
                         slugify=lambda value: value.replace(' ', '-'))
    image = models.ImageField(
        null=True, blank=True, default='default/no_image.jpg', upload_to=image_upload_to, max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles_detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=User)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.comment, self.author)

    def get_absolute_url(self):
        return reverse("article_list")

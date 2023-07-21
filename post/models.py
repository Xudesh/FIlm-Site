from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.conf import settings

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT'
        PUBLISHED = 'PB', 'PUBLISHED'
    
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique_for_date='publish')
    image = models.ImageField(upload_to='images/')
    video = models.FileField( upload_to='video/' ,validators=[FileExtensionValidator(allowed_extensions=['mp4'])], null=True)
    publish = models.DateTimeField(default=timezone.now,)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)

    release_date  = models.CharField(max_length=4, null=True) 
    country = models.CharField(max_length=100, null=True)
    genre = models.CharField(max_length=100, null=True)
    budget = models.IntegerField(null=True)
    actors = models.CharField(max_length=200, null=True)
    nomination = models.CharField(max_length=150, blank=True)

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse(
            'post_detail',
            args=[
                self.publish.day,
                self.publish.month,
                self.publish.year,
                self.slug
            ]
        )
    

class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    email = models.EmailField()
    
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def __str__(self):
        return self.name
    


    
class Profile(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/images/')
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Пользователь {self.user.username}'
    
    @property
    def full_name(self):
        return f'{self.user.username} - {self.date_of_birth}'
    

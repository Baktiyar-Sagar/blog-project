from django.db import models
from ckeditor.fields import RichTextField 
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add= True)
    update_at = models.DateTimeField(null=True, blank=True)
    liked_users = models.ManyToManyField(User, related_name= 'liked_posts')
    view_count = models.PositiveBigIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # Only update "update_at" if the object already exists (i.e., is being updated)
        if self.pk:
            self.update_at = timezone.now()
        super().save(*args, **kwargs)

    def was_updated(self):
        """Return True if the post was updated after creation."""
        if self.update_at:
            return self.update_at > self.created_at
        return False
    
    def __str__(self):
        return f"Title: {self.title} ,By - {self.author}"
    

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    update_at = models.DateTimeField (auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
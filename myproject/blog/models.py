from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# Category model for blog post categories
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Post model for blog posts
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    img_url = models.ImageField(null=True,upload_to='blog/posts/images') # provides a path to the blog post images
    create_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # foreign key to Category model
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # foreign key to User model
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Automatically generate slug from title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    # Property to get the formatted image URL to handle both local and external URLs
    @property
    def formatted_url(self):
        if self.img_url.__str__().startswith(('http://','https://')):
            return self.img_url
        
        return self.img_url.url
    
    # Method to get the absolute URL for the view blog post 
    def get_absolute_url(self):
        return reverse('blog:details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
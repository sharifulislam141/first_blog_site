from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Blog(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_author')
    blog_title = models.CharField(max_length=260,verbose_name="Put a title")
    slug = models.SlugField(max_length=264,unique=True)
    blog_content =models.TextField(verbose_name='What is on your mind? ')
    blog_image =models.ImageField(upload_to='blog_image', verbose_name='Image')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.blog_image:
            img_path = self.blog_image.path
            img = Image.open(img_path)

            # Calculate new width and height based on 1.5:1 aspect ratio
            width, height = img.size
            new_width = width
            new_height = int(width * 2 / 3)  # 1.5:1 ratio

            # Resize the image while maintaining aspect ratio
            if height > new_height:
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the resized image
            img.save(img_path)
    def __str__(self):
        return self.blog_title
    
class Comment(models.Model):
    blog= models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_comment')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    comment = models.TextField(max_length=200)
    comment_date =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment

class Likes(models.Model):
    blog =models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='liked_blog')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='liked_user')
    def __str__(self):
        return self.user +"likes"+self.blog

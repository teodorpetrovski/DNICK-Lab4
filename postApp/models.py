from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Author(models.Model):
    name=models.CharField(max_length=30)
    surname=models.CharField(max_length=30)
    profile_picture=models.ImageField(upload_to="profile_images/", null=True, blank=True)
    profession=models.CharField(max_length=30)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name+" "+self.surname


class Interest(models.Model):
    name=models.CharField(max_length=30)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name=models.CharField(max_length=30)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    title=models.CharField(max_length=30)
    content=models.TextField()
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    createdOn=models.DateTimeField(auto_now_add=True)
    updatedOn=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class File(models.Model):
    file=models.FileField(upload_to='files/',null=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)


class Comment(models.Model):
    content=models.TextField()
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    createdOn=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class BlockedUser(models.Model):
    blocked_user=models.ForeignKey(Author,on_delete=models.CASCADE,related_name="blocked_user")
    blocking_user=models.ForeignKey(Author,on_delete=models.CASCADE,related_name="blocking_user")
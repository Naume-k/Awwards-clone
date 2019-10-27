from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
import numpy as np


class Profile(models.Model):
    firstname = models.CharField(max_length =30)
    lastname = models.CharField(max_length =30)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to = 'profile_photos/', null=True)
    bio = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    # followers = models.ManyToManyField(User, blank=True, related_name='user_followers')

    @classmethod
    def get_all_awwardproj_users(cls):
        awwardproj_users = cls.objects.all()
        return awwardproj_users

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def update_profile(cls,id,value):
        cls.objects.filter(id = id).update(user_id = new_user)

    @classmethod
    def search_by_profile(cls,username):
        certain_user = cls.objects.filter(user__username__icontains = username)
        return certain_user

def __str__(self):
        return self.user



class Project(models.Model):
    image = models.ImageField(upload_to = 'images/')
    project_name = models.CharField(max_length =10)
    project_url = models.CharField(max_length =50)
    location = models.CharField(max_length =10)
    profile = models.ForeignKey(Profile, null = True,related_name='project')
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    user= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-pk']

    def save_project(self):
        self.save()
    
    @classmethod
    def get_project(cls, profile):
        project = Project.objects.filter(Profile__pk = profile)
        return project
    
    @classmethod
    def get_all_projects(cls):
        project = Project.objects.all()
        return project

    @classmethod
    def search_by_profile(cls,search_term):
        projo = cls.objects.filter(profile__name__icontains=search_term)
        return projo

    @classmethod
    def get_profile_projects(cls, profile):
        project = Project.objects.filter(profile__pk = profile)
        return project

    @classmethod
    def find_project_id(cls, id):
        identity = Project.objects.get(pk=id)
        return identity

    def average_rating(self):
        all_ratings = list(map(lambda x: x.design_rating, self.rate_set.all()))
        all_ratings = list(map(lambda x: x.content_rating, self.rate_set.all()))
        all_ratings = list(map(lambda x: x.usability_rating, self.rate_set.all()))
        return np.mean(all_ratings)



class Comments(models.Model):
    comment = models.CharField(max_length = 250)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    commented_project = models.ForeignKey(Project, on_delete=models.CASCADE, null = True)

    def save_comments(self):
        self.save()

    def delete_comments(self):
        self.delete()
    
    def update_comment(self):
        self.update()

def __str__(self):
        return self.posted_by


class Rate(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10,'10'),
    )
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    rater=models.ForeignKey(User,on_delete=models.CASCADE)
    design_rating = models.IntegerField(choices=RATING_CHOICES,null=True)
    usability_rating=models.IntegerField(choices=RATING_CHOICES,null=True)
    content_rating=models.IntegerField(choices=RATING_CHOICES,null=True)

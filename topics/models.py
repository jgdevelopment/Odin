from django.db import models
from django.contrib.auth.models import User
import django.utils.text
from django.utils.text import slugify
import re

class Subject(models.Model):
    # eg. biology, chemistry, algebra 2
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    
    @classmethod
    def create(cls, name):
        slug = slugify(name)
        return cls(name=name, slug=slug)
        
    def __unicode__(self):
        return name
    
class Topic(models.Model):
    # eg. rational functions, dna transcription
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject)
    slug = models.SlugField()
    
    @classmethod
    def create(cls, title, subject):
        slug = slugify(title)
        return cls(name=title, subject=subject, slug=slug)
        
    def __unicode__(self):
        return name

# should be abstract but can't due to limitation.. will be slower,
# fix later if noticeably slow
class UserContributedInfo(models.Model):
    # username of the submitting user
    user = models.CharField(max_length=20)
    topic = models.ForeignKey(Topic)
    
    def vote_count():
        count = 0
        for vote in Vote.objects.filter(info=self):
            count = count + vote.amount
        return count
    
class Vote(models.Model):
    # username of the voting user
    user = models.CharField(max_length=20)
    # voting weight (eg. +1 or -1)
    amount = models.IntegerField()
    # information being voted on
    info = models.ForeignKey(UserContributedInfo)

class VocabWord(UserContributedInfo):
    word = models.CharField(max_length=100)
    definition = models.CharField(max_length=500)
    
class Link(UserContributedInfo):
    url = models.URLField()
    description = models.CharField(max_length=500)
    
class PracticeProblem(UserContributedInfo):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    
class Information(UserContributedInfo):
    # eg. "Identifying the roots of a rational function"
    subtopic = models.CharField(max_length=150)
    info = models.TextField()
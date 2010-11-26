from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Sequence(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return unicode(self.name)

class Track(models.Model):
    name = models.TextField()
    sequence = models.ForeignKey(Sequence)

    def __unicode__(self):
        return unicode(self.name)

class Gene(models.Model): # really more like an annotation
    name = models.TextField()
    sequence = models.ForeignKey(Sequence)
    track = models.ForeignKey(Track)

    def fullname(self):
        return "%s - %s - %s" % (unicode(self.sequence), unicode(self.track), unicode(self.name))

    def medname(self):
        return "%s - %s" % (unicode(self.sequence), unicode(self.name))

    def shortname(self):
        return unicode(self.name)

    def __unicode__(self):
        return self.medname()

class Article(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=300)
    url = models.URLField()
    genes = models.ManyToManyField(Gene)
    date = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())

    def __unicode__(self):
        return unicode(self.title)

class Vote(models.Model):
    article = models.ForeignKey(Article)
    user = models.ForeignKey(User)
    vote = models.SmallIntegerField(choices=((1, 'up'), (-1, 'down')))

    def is_upvote(self):
        return self.vote==1

    def is_downvote(self):
        return self.vote==-1

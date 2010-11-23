from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=300)
    url = models.URLField()
    genes = models.ManyToManyField('genenews_main.Gene')

    def __unicode__(self):
        return unicode(self.title)

class Sequence(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return unicode(self.name)

class Gene(models.Model):
    name = models.TextField()
    sequence = models.ForeignKey(Sequence)

    def fullname(self):
        return "%s - %s" % (unicode(self.sequence), unicode(self.name))

    def __unicode__(self):
        return unicode(self.name)

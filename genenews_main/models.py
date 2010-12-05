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

    def get_score(self):
        score = self.vote_set.filter(vote=1).count() - self.vote_set.filter(vote=-1).count()
        return score

class Vote(models.Model):
    article = models.ForeignKey(Article)
    user = models.ForeignKey(User)
    vote = models.SmallIntegerField(choices=((1, 'up'), (-1, 'down')))
    date = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())

    def is_upvote(self):
        return self.vote==1

    def is_downvote(self):
        return self.vote==-1

    def __unicode__(self):
        return "%s voted %s on %s" % (unicode(self.user), 'up' if self.is_upvote() else 'down', unicode(self.article))

def type_to_date(type='all'):
    if type == 'all':
        return datetime.datetime.utcfromtimestamp(0)
    elif type == 'year':
        return datetime.datetime.now() - datetime.timedelta(days=365)
    elif type == 'month':
        return datetime.datetime.now() - datetime.timedelta(days=30)
    elif type == 'day':
        return datetime.datetime.now() - datetime.timedelta(days=1)

def get_user_score(user, type='all'):
    score = 0
    date = type_to_date(type)
    for article in user.article_set.filter(date__gte=date):
        score += article.vote_set.filter(vote=1).count()
        score -= article.vote_set.filter(vote=-1).count()
    return score

class LeaderboardManager(models.Manager):
    def update(self, exclude_zero=True, type='all'):
        if type == 'all':
            types = ['year', 'month', 'day', 'all']
        else:
            types = [type]

        for t in types:
            tempentries = []
            for user in User.objects.all():
                if not exclude_zero or user.article_set.filter(date__gte=type_to_date(type)).count():
                    tempentries.append((get_user_score(user=user, type=t), user))
            tempentries.sort()
            tempentries.reverse()
            self.filter(type=t).delete()
            for index, temp in enumerate(tempentries):
                lbcache = self.create(user=temp[1], score=temp[0], rank=index+1, type=t) # already deleted other objects, so ok to create

class LeaderboardCache(models.Model):
    objects = LeaderboardManager()
    user = models.ForeignKey(User)
    score = models.IntegerField()
    rank = models.IntegerField()
    type = models.CharField(choices=(('all','all time'), ('year', 'last year'), ('month','last month'), ('day', 'last day')), max_length=10, default='all')

    def __unicode__(self):
       return "%s is ranked %s with %s points over %s" % (self.user, self.rank, self.score, self.type)

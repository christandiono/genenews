from django.contrib import admin
from genenews.genenews_main.models import Article, Sequence, Gene, Track, Vote, LeaderboardCache

admin.site.register(Article)
admin.site.register(Sequence)
admin.site.register(Gene)
admin.site.register(Track)
admin.site.register(Vote)
admin.site.register(LeaderboardCache)

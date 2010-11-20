from django.forms import ModelForm

from genenews_main.models import Article

class SubmissionForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('user')

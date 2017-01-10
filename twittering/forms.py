from django import forms

class HandleForm(forms.Form):
    target_handle = forms.CharField(label='target handle', max_length=15)
    number_of_tweets = forms.IntegerField(label='number of tweets')
from django import forms

# creating a form
from django.forms import RadioSelect


class YAMAPy(forms.Form):
    yt_vid_url = forms.URLField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Paste your video link here', 'class': 'url-field'}))
    file_type = forms.CharField(initial='0', label='', widget=forms.Select(
        choices=[('0', 'Video'), ('1', 'Audio')], attrs={'class': 'dropdown-field'}))

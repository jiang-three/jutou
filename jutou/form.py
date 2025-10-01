from django import forms

from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text', 'image']
        labels = {'text': '', 'image': '上传图片'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
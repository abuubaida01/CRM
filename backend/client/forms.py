from .models import Client, Comment, ClientFile
from django import forms


class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'description')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)


class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ("file",)

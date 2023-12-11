from .models import Lead, Comment, LeadFile
from django import forms


class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name', 'email', 'description', 'priority', 'status',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)



class LeadFileForm(forms.ModelForm):
    
    class Meta:
        model = LeadFile
        fields = ("file",)

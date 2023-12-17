from django import forms
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget



cat = [
  ('General', '⚫ General'),
  ('Channel', '🔴 Channel'),
  ('Masjid & Madrasa', '🟢 Masjid & Madrasa'),
  ('Organization', '🔵 Organization'),
  ('Brand', '🟠 Brand'),
] 



class ProfileModelForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        label="Phone Number (will not be displayed)",
        widget=PhoneNumberPrefixWidget(initial='PK'),
        required=False, 
    )
    slogan = forms.CharField(
        max_length=80,
        label='Slogan or Favorite Line',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Leave an inspiring Line for other users (max 80 characters)'
        })
    )
    profession = forms.CharField(
        max_length=60,
        label='Profession',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Tell us what you do and how you make a difference as a valuable Sefarz user.'}))

    cur_add = forms.CharField(
        max_length=100,
        label='Location (e.g. City, Country)',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Street/Block, Area, Karachi, Pakistan'
        })
    )
    picture = forms.ImageField(
        widget=forms.FileInput(attrs={'type': 'file', 'accept': 'image/*' , 'style': 'width: 50em; height: auto;'}),
        required=False,
        label='Profile Picture (800 x 800 pixels)',
    )
    intro = forms.CharField(
        max_length=250,
        label='About (max 250 characters)',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us a little about yourself',
            'rows': 2,
            'cols': 30
        })
    )
    bank_details = forms.CharField(
        max_length=700,
        label='Bank Details (will not be displayed)',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Provide your Bank Details or Patreon Link for Support, if you are going to create PVC',
            'rows': 1,
            'cols': 30
        })
    )

    email_notif = forms.BooleanField( 
        label='Email Notification',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'type': 'checkbox',
            'id': 'flexCheckDefault',
        })
    )

    cat = forms.CharField(
        label='Profile Category', 
        required=False, 
        widget=forms.Select(choices=cat, attrs={'placeholder': 'Select Profile Category'})
        )


    class Meta:
        model = Profile
        fields = [
            'picture',
            'slogan',
            'intro',
            'profession',
            'phone_number',
            'cur_add',
            'bank_details',
            'email_notif',
            'cat',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, field in enumerate(self.fields):
            self.fields[field].widget.attrs['class'] = f'field{i+1}'
            self.fields[field].widget.attrs['id'] = f'field{i+1}'

    # def clean_picture(self):
    #     ALLOWED_IMAGE_TYPES = ['picture/jpeg', 'picture/png', 'picture/jpg']
    #     image = self.cleaned_data.get('image')
    #     if image:
    #         content_type = image.content_type
    #         if content_type not in ALLOWED_IMAGE_TYPES:
    #             message = f"This file type ({content_type}) is not supported. Please upload a JPEG, PNG, or jpg file."
    #             raise ValidationError(message)
    #     return image
    # def save(self, commit=True):
    #     instance = super().save(commit=False)

    #     # Handle file upload
    #     picture = self.cleaned_data.get('picture')
    #     if picture:
    #         instance.picture = picture.name.split('/')[-1]

    #     if commit:
    #         instance.save()

    #     return instance
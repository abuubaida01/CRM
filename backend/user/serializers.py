from rest_framework import serializers
from user.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from user.utils import Util
from django.core.mail import send_mail
from decouple import config
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


INFO_EMAIL = config('INFO_EMAIL', cast=str, default='famior01@gmail.com')


class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  
  class Meta:
    model = User
    fields=['email', 'username', 'full_name', 'religion', 'gender', 'date_of_birth', 'password', 'password2']
    extra_kwargs= {
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password') #attrs or data 
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password don't match")
    return attrs

  def create(self, validated_data):
    validated_data.pop('password2', None)  # Remove password2 from the data
    return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
      model = User
      fields = ['email', 'password']

  def validate(self, data):
      email = data.get('email')
      password = data.get('password')

      user = authenticate(username=email, password=password)

      if not user:
          raise AuthenticationFailed('Invalid email or password')

      # You can add additional validation logic here if needed

      return data

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Passwords don't match")
    user.set_password(password)
    user.save()
    return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
  
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')

    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      token = PasswordResetTokenGenerator().make_token(user)
      link = 'http://localhost:8000/user/reset/'+uid+'/'+token

      subject = f"Jani verify your Email Address!"
      message = f'Click Following Link to Reset Your Password {link}'
      from_email = f"{INFO_EMAIL}"
      recipient_list = [user.email]
      send_mail(subject, message, from_email, recipient_list, fail_silently=False)

      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
  
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):

    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')

      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password don't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


class ChangeUserDetailSerializer(serializers.ModelSerializer):
  username = serializers.CharField(max_length=100, required=False)
  date_of_birth = serializers.DateField(required=False)
  full_name = serializers.CharField(max_length=100, required=False)
  religion = serializers.CharField(max_length=100, required=False)

  class Meta:
      model = User  # Replace with the actual User model
      fields = ['username', 'full_name', 'date_of_birth', 'religion']

  def validate(self, attrs):
      if 'religion' in attrs:
        new_religion = attrs['religion']
        user = self.context['user']

        if user.religion == 'Islam' and new_religion != 'Islam':
            raise serializers.ValidationError("You can't convert from Islam to any other religion.")
      return attrs


class listUserSerializer(serializers.ModelSerializer):
  class Meta:
      model = User  # Replace with the actual User model
      fields = ['username', 'full_name', 'date_of_birth', 'religion', 'gender', 'email']





# class ChangeUserDetailSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=100, required=False)
#     date_of_birth = serializers.DateField(required=False)
#     full_name = serializers.CharField(max_length=100, required=False)
#     religion = serializers.CharField(max_length=100, required=False)

#     class Meta:
#       fields = ['username', 'full_name', 'date_of_birth', 'religion']

#     def validate(self, attrs):
#       username = attrs.get('username')
#       full_name = attrs.get('full_name')
#       date_of_birth = attrs.get('date_of_birth')
#       religion = attrs.get('religion')

#       user = self.context.get('user')
#       print('user religion: \t', user.religion)
#       user.save()
#       return attrs

    # def validate_username(self, value):
    #     validator = UnicodeUsernameValidator()
    #     try:
    #         validator(value)
    #     except ValidationError as e:
    #         raise serializers.ValidationError(e)
        
    #     return value

    # def validate(self, data):
        
    #     if 'religion' in data:
    #         new_religion = data['religion']
    #         user = self.context['request'].user

    #         if user.religion == 'Islam' and new_religion != 'Islam':
    #             raise serializers.ValidationError("You can't convert from Islam to any other religion.")

    #     return data

    # def update(self, instance, validated_data):
    #     # Update the user instance with the validated data
    #     if 'username' in validated_data:
    #         instance.username = validated_data['username']
    #     if 'date_of_birth' in validated_data:
    #         instance.date_of_birth = validated_data['date_of_birth']
    #     if 'full_name' in validated_data:
    #         instance.full_name = validated_data['full_name']
    #     if 'religion' in validated_data:
    #         instance.religion = validated_data['religion']
        
    #     instance.save()
    #     return instance
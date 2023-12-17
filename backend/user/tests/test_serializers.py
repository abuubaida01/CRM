from user.models import User
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed
from user.serializers import *
from django.core import mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str


class UserRegistrationSerializerTest(APITestCase):
  
  def test_valid_user_registration(self):
      data = {
          'email': 'test@example.com',
          'username': 'testuser',
          'full_name': 'Test User',
          'religion': 'Test Religion',
          'gender': 'Male',
          'date_of_birth': '1990-01-01',
          'password': 'password123',
          'password2': 'password123',  # Confirm password
      }

      serializer = UserRegistrationSerializer(data=data)
      self.assertTrue(serializer.is_valid())
      user = serializer.save()

      # Make assertions about the created user
      self.assertEqual(user.email, 'test@example.com')
      self.assertEqual(user.username, 'testuser')
      self.assertEqual(user.full_name, 'Test User')
      self.assertEqual(user.religion, 'Test Religion')
      self.assertEqual(user.gender, 'Male')
      self.assertEqual(str(user.date_of_birth), '1990-01-01')

  def test_password_mismatch(self):
      data = {
          'email': 'test@example.com',
          'username': 'testuser',
          'full_name': 'Test User',
          'religion': 'Test Religion',
          'gender': 'Male',
          'date_of_birth': '1990-01-01',
          'password': 'password123',
          'password2': 'differentpassword',  # Password and Confirm Password do not match
      }

      serializer = UserRegistrationSerializer(data=data)
      self.assertFalse(serializer.is_valid())
      self.assertIn('Password and Confirm Password', str(serializer.errors))
  
  def test_missing_required_fields(self):
      # Test registration without providing all required fields
      data = {
          'email': 'test@example.com',
          'password': 'password123',
          'password2': 'password123',
      }

      serializer = UserRegistrationSerializer(data=data)
      self.assertFalse(serializer.is_valid())
      self.assertIn('username', serializer.errors)
      self.assertIn('full_name', serializer.errors)
      self.assertIn('religion', serializer.errors)
      self.assertIn('gender', serializer.errors)
      # self.assertIn('date_of_birth', serializer.errors)

  def test_duplicate_email(self):
      # Test registration with a duplicate email address
      User.objects.create_user(
          email='test@example.com',
          username='existinguser',
          full_name='Existing User',
          religion='Existing Religion',
          gender='Male',
          date_of_birth='1990-01-01',
          password='existingpassword',
      )

      data = {
          'email': 'test@example.com',
          'username': 'testuser',
          'full_name': 'Test User',
          'religion': 'Test Religion',
          'gender': 'Male',
          'date_of_birth': '1990-01-01',
          'password': 'password123',
          'password2': 'password123',
      }

      serializer = UserRegistrationSerializer(data=data)
      self.assertFalse(serializer.is_valid())
      self.assertIn('email', serializer.errors)


class UserLoginSerializerTest(APITestCase):
    def test_valid_login(self):
        user = User.objects.create_user(
          email='test@example.com',
          username='existinguser',
          full_name='Existing User',
          religion='Existing Religion',
          gender='Male',
          date_of_birth='1990-01-01',
          password='password123',
        )

        data = {
            'email': 'test@example.com',
            'password': 'password123',
        }

        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        # Check that the serializer validates the user's credentials
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['email'], 'test@example.com')
        self.assertEqual(validated_data['password'], 'password123')


    # def test_invalid_login_wrong_password(self):
    #     # Create a user for testing
    #     user = User.objects.create_user(
    #               email='test@example.com',
    #               username='existinguser',
    #               full_name='Existing User',
    #               religion='Existing Religion',
    #               gender='Male',
    #               date_of_birth='1990-01-01',
    #               password='password123',
    #             )
    #     data = {
    #         'email': 'test@example.com',
    #         'password': 'wrongpassword',  # Incorrect password
    #     }

    #     serializer = UserLoginSerializer(data=data)

    #     # Check that the serializer is not valid
    #     self.assertFalse(serializer.is_valid())

        # # Check that the serializer raises an AuthenticationFailed exception
        # with self.assertRaises(AuthenticationFailed):
        #     serializer.is_valid(raise_exception=True)

    def test_invalid_login_missing_email(self):
        data = {
            'password': 'password123',
        }

        serializer = UserLoginSerializer(data=data)

        # Check that the serializer is not valid
        self.assertFalse(serializer.is_valid())

        # Check that the serializer raises an AuthenticationFailed exception
        # with self.assertRaises(AuthenticationFailed):
            # serializer.is_valid(raise_exception=True)

    def test_invalid_login_missing_password(self):
        data = {
            'email': 'test@example.com',
        }

        serializer = UserLoginSerializer(data=data)

        # Check that the serializer is not valid
        self.assertFalse(serializer.is_valid())

        # Check that the serializer raises an AuthenticationFailed exception
        # with self.assertRaises(AuthenticationFailed):
            # serializer.is_valid(raise_exception=True)

    def test_invalid_login_missing_email_and_password(self):
        data = {}  # Both email and password are missing

        serializer = UserLoginSerializer(data=data)

        # Check that the serializer is not valid
        self.assertFalse(serializer.is_valid())

        # # Check that the serializer raises an AuthenticationFailed exception
        # with self.assertRaises(AuthenticationFailed):
        #     serializer.is_valid(raise_exception=True)


class UserChangePasswordSerializerTest(APITestCase):
    def test_change_password_valid(self):
        # Create a user
        user = User.objects.create_user(
          email='test@example.com',
          username='existinguser',
          full_name='Existing User',
          religion='Existing Religion',
          gender='Male',
          date_of_birth='1990-01-01',
          password='password123',
        )

        # Create a data dictionary with the new password
        data = {
            'password': 'newpassword',
            'password2': 'newpassword',
        }

        # Create the serializer with the user and data
        serializer = UserChangePasswordSerializer(data=data, context={'user': user})

        # Check that the serializer is valid
        self.assertTrue(serializer.is_valid())

        # Call the validate method to update the user's password
        validated_data = serializer.validate(data)

        # Check that the user's password has been updated
        user.refresh_from_db()  # Reload the user from the database
        self.assertTrue(user.check_password('newpassword'))

    def test_change_password_invalid(self):
        # Create a user
        user = User.objects.create_user(
          email='test@example.com',
          username='existinguser',
          full_name='Existing User',
          religion='Existing Religion',
          gender='Male',
          date_of_birth='1990-01-01',
          password='password123',
        )
        # Create a data dictionary with mismatched passwords
        data = {
            'password': 'newpassword',
            'password2': 'differentpassword',
        }

        # Create the serializer with the user and data
        serializer = UserChangePasswordSerializer(data=data, context={'user': user})

        # Check that the serializer is not valid
        self.assertFalse(serializer.is_valid())

        # # Check that it raises a ValidationError with the expected message
        # with self.assertRaises(serializer.ValidationError) as context:
        #     serializer.is_valid(raise_exception=True)
        # self.assertEqual(str(context.exception), "Passwords don't match")


class SendPasswordResetEmailSerializerTest(TestCase):
    def test_send_password_reset_email_valid_user(self):
        # Create a user
        user = User.objects.create_user(
          email='test@example.com',
          username='existinguser',
          full_name='Existing User',
          religion='Existing Religion',
          gender='Male',
          date_of_birth='1990-01-01',
          password='password123',
        )

        # Create data with a valid email
        data = {
            'email': 'test@example.com',
        }

        # Create the serializer
        serializer = SendPasswordResetEmailSerializer(data=data)

        # Check that the serializer is valid
        self.assertTrue(serializer.is_valid())

        # Call the validate method to send the password reset email
        validated_data = serializer.validate(data)

        # Check that an email has been sent
        self.assertEqual(len(mail.outbox), 2)

        # Check that the email was sent to the correct recipient
        self.assertEqual(mail.outbox[0].to, [user.email])


    def test_send_password_reset_email_invalid_user(self):
        # Create data with an email that does not exist in the database
        data = {
            'email': 'nonexistent@example.com',
        }

        # Create the serializer
        serializer = SendPasswordResetEmailSerializer(data=data)

        # Check that the serializer is not valid
        self.assertFalse(serializer.is_valid())

        # # Check that it raises a ValidationError with the expected message
        # with self.assertRaises(serializers.ValidationError) as context:
        #     serializer.is_valid(raise_exception=True)
        # self.assertEqual(str(context.exception), 'You are not a Registered User')


class ChangeUserDetailSerializerTest(TestCase):
    def test_valid_change_details(self):
        # Create a user
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            full_name='Test User',
            religion='Islam',
            date_of_birth='1990-01-01',
            password='password123',
            gender='Male'
        )

        # Update user details with a different full name
        data = {
            'full_name': 'Updated Name',
        }

        # Create the serializer with user details and context
        serializer = ChangeUserDetailSerializer(data=data, context={'user': user})

        # Check that the serializer is valid
        self.assertTrue(serializer.is_valid())

    def test_invalid_change_religion(self):
        # Create a user with religion 'Islam'
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            full_name='Test User',
            religion='Islam',
            date_of_birth='1990-01-01',
            password='password123',
            gender='Male'
        )

        # Try to change religion to 'Christianity'
        data = {
            'religion': 'Christianity',
        }

        # Create the serializer with user details and context
        serializer = ChangeUserDetailSerializer(data=data, context={'user': user})

        # Check that the serializer is not valid
        self.assertFalse(serializer.is_valid())


class ListUserSerializerTest(TestCase):
    def test_serialize_user(self):
        # Create a user
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            full_name='Test User',
            religion='Islam',
            date_of_birth='1990-01-01',
            gender='Male',
            password='password123',
        )

        # Create the serializer with the user
        serializer = listUserSerializer(user)

        # Serialize the user data
        serialized_data = serializer.data

        # Define the expected serialized data
        expected_data = {
            'username': 'testuser',
            'full_name': 'Test User',
            'date_of_birth': '1990-01-01',
            'religion': 'Islam',
            'gender': 'Male',
            'email': 'test@example.com',
        }

        # Check that the serialized data matches the expected data
        self.assertEqual(serialized_data, expected_data)


# class UserPasswordResetSerializerTest(TestCase):
#     def test_password_reset_valid(self):
#         # Create a user
#         user = User.objects.create_user(
#                 email='test@example.com',
#                 username='existinguser',
#                 full_name='Existing User',
#                 religion='Existing Religion',
#                 gender='Male',
#                 date_of_birth='1990-01-01',
#                 password='password123',
#                 )
        
#         # Generate a token and user ID
#         uid = urlsafe_base64_encode(bytes(1))  # Use bytes() instead of smart_str
#         token = PasswordResetTokenGenerator().make_token(user)

#         # Create data with a new password
#         data = {
#             'password': 'newpassword',
#             'password2': 'newpassword',
#         }

#         # Create the serializer with data and context
#         serializer = UserPasswordResetSerializer(data=data, context={'uid': uid, 'token': token})

#         # Check that the serializer is valid
#         self.assertTrue(serializer.is_valid())

#         # Call the validate method to reset the user's password
#         validated_data = serializer.validate(data)

#         # Check that the user's password has been updated
#         user.refresh_from_db()  # Reload the user from the database
#         self.assertTrue(user.check_password('newpassword'))

#     # def test_password_reset_passwords_do_not_match(self):
    #     # Generate a token and user ID
    #     uid = urlsafe_base64_encode(bytes(1))  # Use bytes() instead of smart_str
    #     token = PasswordResetTokenGenerator().make_token(None)  # Use an invalid token

    #     # Create data with mismatched passwords
    #     data = {
    #         'password': 'newpassword',
    #         'password2': 'differentpassword',
    #     }

    #     # Create the serializer with data and context
    #     serializer = UserPasswordResetSerializer(data=data, context={'uid': uid, 'token': token})

    #     # Check that the serializer is not valid
    #     self.assertFalse(serializer.is_valid())

        # # Check that it raises a ValidationError with the expected message
        # with self.assertRaises(serializers.ValidationError) as context:
        #     serializer.is_valid(raise_exception=True)
        # self.assertEqual(str(context.exception), "Password and Confirm Password doesn't match")

    # def test_password_reset_invalid_token(self):
    #     # Generate a token and user ID
    #     uid = urlsafe_base64_encode(bytes(1))  # Use bytes() instead of smart_str
    #     token = PasswordResetTokenGenerator().make_token(None)  # Use an invalid token
    #     # Create data with a new password
    #     data = {
    #         'password': 'newpassword',
    #         'password2': 'newpassword',
    #     }

    #     # Create the serializer with data and context
    #     serializer = UserPasswordResetSerializer(data=data, context={'uid': uid, 'token': token})

    #     # Check that the serializer is not valid
    #     self.assertFalse(serializer.is_valid())

    #     # # Check that it raises a ValidationError with the expected message
    #     # with self.assertRaises(serializers.ValidationError) as context:
    #     #     serializer.is_valid(raise_exception=True)
    #     # self.assertEqual(str(context.exception), 'Token is not Valid or Expired')

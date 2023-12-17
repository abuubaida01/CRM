from django.test import TestCase
from user.models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        email = "Sefarz@example.com"
        full_name = "Sefarz"
        username = "SefarzUsername"
        password = "SefarzPassword"
        religion = "Islam"
        gender = "Male"
        date_of_birth = "2001-09-21"

        user = User.objects.create_user(email=email, full_name=full_name, username=username, password=password, religion=religion, gender=gender, date_of_birth=date_of_birth)

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(password))


    def test_create_superuser(self):
        """Test creating a superuser"""
        email = "SefarzAdmin@example.com"
        full_name = "SefarzAdmin"
        username = "SefarzAdminUsername"
        password = "SefarzAdminPassword"
        religion = "Islam"
        gender = "Male"
        date_of_birth = "2001-09-21"

        superuser = User.objects.create_superuser(email=email, full_name=full_name, username=username, password=password, religion=religion, gender=gender, date_of_birth=date_of_birth)

        self.assertEqual(superuser.email, email)
        self.assertEqual(superuser.username, username)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.check_password(password))

# class UserMethodTest(TestCase):
#     def test_get_full_name(self):
#         """Test getting the user's full name"""
#         user = User(email="Sefarz@example.com", name="Test User")
#         self.assertEqual(user.get_full_name(), "Test User")

#     def test_has_perm(self):
#         """Test checking if the user has a specific permission"""
#         user = User(email="Sefarz@example.com", name="Test User")
#         self.assertTrue(user.has_perm("some_permission"))

#     def test_has_module_perms(self):
#         """Test checking if the user has module permissions"""
#         user = User(email="Sefarz@example.com", name="Test User")
#         self.assertTrue(user.has_module_perms("some_app"))

#     def test_is_staff(self):
#         """Test checking if the user is staff"""
#         user = User(email="Sefarz@example.com", name="Test User")
#         self.assertFalse(user.is_staff)
        
# # in both drf or django model test is going to be same

# class UserModelTest(TestCase):

#     def setUp(self): # Python's builtin unittest
#         user_a = User(username='User', email='User@invalid.com')
#         user_a_pw = 'some_123_password'
#         self.user_a_pw = user_a_pw
#         user_a.is_staff = True
#         user_a.is_superuser = True 
#         user_a.set_password(user_a_pw)
#         user_a.save()
#         self.user_a = user_a
    
#     def test_user_exists(self):
#         user_count = User.objects.all().count()
#         self.assertEqual(user_count, 1) # ==
#         self.assertNotEqual(user_count, 0) # !=

    
#     def test_user_password(self):
#         user_a = User.objects.get(username="User")
#         self.assertTrue(
#             user_a.check_password(self.user_a_pw)
#         )
    
#     def test_login_url(self):
#         login_url = settings.LOGIN_URL
#         print('****************:', login_url)
#         # python requests - manage.py runserver
#         # self.client.get, self.client.post
#         # response = self.client.post(url, {}, follow=True)
#         data = {"username": "User", "password": "some_123_password"}
#         response = self.client.post(login_url, data, follow=True)
#         # print(dir(response))
#         # print(response.request)
#         status_code = response.status_code
#         print('****************:', status_code)
#         redirect_path = response.request.get("PATH_INFO")
#         self.assertEqual(redirect_path, settings.LOGIN_URL)
#         self.assertEqual(status_code, 200)
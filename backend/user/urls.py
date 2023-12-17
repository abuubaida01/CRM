from django.urls import path
from django.contrib.auth.decorators import login_required
app_name = 'user'
from .views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserRegistrationView, UserPasswordResetView, ChangeUserDetailView,listUserDetailsApi,VerifyEmailView, DeleteUserAPI



urlpatterns = [
    # path('update/<int:pk>/', login_required(views.UserUpdateView.as_view()), name='user-update'),
    path('getuserD/', listUserDetailsApi.as_view()),
    path('changeUserD/', ChangeUserDetailView.as_view()),

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify/<token>/', VerifyEmailView.as_view(), name='verify-email'),

    path('login/', UserLoginView.as_view(), name='login'),

    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('reswordEmail/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path("delete/", DeleteUserAPI.as_view(), name='Delete_User'),
    
]



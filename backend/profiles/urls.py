from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
  # myprofile,
  ProfileListAPI,
  ProfileDetailViewAPI,
  ProfileUpdateAPI,
  FollowerListAPI,
  FollowingListAPI,
  
  UserVuzerAPI,
  NearMeListAPI,
  OrgListAPIView,
  BrandListAPIView,
  MListAPIView,
  ChannelListAPIView,

  # SavadsListAPI,
  # OrgVideosListAPI,
  # PVCVideosAPI,
  # FAMListAPI,
  remove_followerAPI,
  popular,  
  FollowUnfollowAPI,
  )

app_name = 'profiles'  # in case we need to use the namespace in the future
urlpatterns = [
  path('<str:pk>/', ProfileDetailViewAPI.as_view(), name='profile-detail-view'),

  path('allp', ProfileListAPI.as_view(), name='all-profiles'),
  path('Organizations', OrgListAPIView.as_view(), name='all-orgs'),
  path('Channels', ChannelListAPIView.as_view(), name='all-cha'),
  path('M&M', MListAPIView.as_view(), name='all-mm'),
  path('Brands', BrandListAPIView.as_view(), name='all-b'),
  path('<str:pk>/nearme', NearMeListAPI.as_view(), name='near_me'),

  path('update', ProfileUpdateAPI.as_view(), name='profile_update'), 
  path('<str:pk>/follow', FollowUnfollowAPI.as_view(), name='follow-unfollow-profile'),
  path('<str:pk>/removefollower', remove_followerAPI.as_view(), name='remove-follower'),

  path('<str:pk>/followers', FollowerListAPI.as_view(), name='followers'),
  path('<str:pk>/following', FollowingListAPI.as_view(), name='following'),

  # Profile Posts
  # path('<str:pk>/pvc', PVCVideosAPI.as_view() ,name='pvc'),
  # path('<str:pk>/ads', SavadsListAPI.as_view() ,name='ads'),
  # path('<str:pk>/fam', FAMListAPI.as_view(), name='fam'),
  # path('<str:pk>/org', OrgVideosListAPI.as_view() ,name='org'),

  path("search", UserVuzerAPI.as_view(), name='search-user'),
]

######### Internal ######### 
from .models import Profile
from .forms import ProfileModelForm
from .forms import ProfileModelForm
from user.models import User
from django.contrib.auth import get_user_model



######### External #########
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProfileModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from user.models import User
from django.contrib.auth import get_user_model
from notifications.signals import notify
from django.contrib import messages
from django.core.mail import send_mail
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponseRedirect
from itertools import chain
from decouple import config
from user.models import User
ABSOLUTE_PATH = config('ABSOLUTE_PATH', cast=str, default='/app')
PRODUCTION = config('PRODUCTION', cast=bool, default=False)
INFO_EMAIL = config('INFO_EMAIL', cast=str, default='famior01@gmail.com')


################################ Rest Framwork ###############################
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.utils.decorators import method_decorator
from rest_framework.response import Response
############################### Functions & Classes ################################

# class PVCVideosAPI(generics.ListAPIView):
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         profile = get_object_or_404(Profile, user__username=pk)

#         if self.request.user.is_authenticated:
#             if self.request.user.gender == 'Male' and self.request.user != profile.user:
#                 pvc_videos = pvc.objects.filter(creator=profile, gender__iexact="Male")
#             elif self.request.user.gender == "Female" and self.request.user != profile.user:
#                 pvc_videos = pvc.objects.filter(creator=profile, gender__iexact='Female')
#             else:
#                 pvc_videos = pvc.objects.filter(creator=profile)
#         else:
#             pvc_videos = pvc.objects.filter(creator=profile, gender__iexact="Male")

#         return pvc_videos

#     def list(self, request, pk):
#         queryset = self.get_queryset()
#         serializer = PVCSerializer(queryset, many=True)
#         return Response(serializer.data)

# class FAMListAPI(generics.ListAPIView):
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         profile = get_object_or_404(Profile, user__username=pk)
#         return FAM.objects.filter(creator=profile)

#     def list(self, request, pk):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

# class OrgVideosListAPI(generics.ListAPIView):
#     serializer_class = OrgSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         profile = get_object_or_404(Profile, user__username=pk)
#         return Org.objects.filter(org_name=profile)

#     def list(self, request, pk):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

# class SavadsListAPI(generics.ListAPIView):
#     serializer_class = SavadsSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         profile = get_object_or_404(Profile, user__username=pk)
#         return Savads.objects.filter(creator=profile, activated=True, verified=True).order_by('-created')

#     # def list(self, request, pk):
#     #     queryset = self.get_queryset()
#     #     serializer = self.get_serializer(queryset, many=True)
#     #     return Response(serializer.data)

class ProfileDetailViewAPI(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        profile = get_object_or_404(Profile, user__username=pk)
        serializer = ProfileSerializer(profile)
        context = {}
        
        context['profiles'] = serializer.data

        pvc_ = pvc.objects.filter(creator=profile).all()
        org = Org.objects.filter(org_name=profile).all()
        fam = FAM.objects.filter(creator=profile).all()
        ads = Savads.objects.filter(creator=profile, activated=True, verified=True).order_by('-created')

        pvc_count, fam_count, org_count, ads_count = pvc_.count(), fam.count(), org.count(), ads.count()


        if pvc_count >= org_count and pvc_count >= fam_count and pvc_count >= ads_count:
            context['pvc_videos'] = [pvc_.values()]
            context['run_pvc'] = True
        elif org_count >= pvc_count and org_count >= fam_count and org_count >= ads_count:
            context['org_videos'] = [org.values()]
            context['run_org'] = True
        elif fam_count >= pvc_count and fam_count >= org_count and fam_count >= ads_count:
            context['zp'] = [fam.values()]
            context['run_fam'] = True
        else:
            context['all_ads'] = [ads.values()]
            context['run_ads'] = True

        return Response(context, status=status.HTTP_200_OK)


        # return Response(serializer.data)

class FollowerListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, username=pk)

        followers_profiles = Profile.objects.filter(following=user).exclude(user=user)
        view_profile = Profile.objects.get(user=user)

        followers_serializer = ProfileSerializer(followers_profiles, many=True)
        view_profile_serializer = ProfileSerializer(view_profile)

        # data = {
        #     'followers_profiles': followers_serializer.data,
        #     'view_profile': view_profile_serializer.data,
        # }

        return Response(followers_serializer.data, status=status.HTTP_200_OK)

class FollowingListAPI(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        check_p = Profile.objects.get(user=self.request.user)
        print("check Profile,", check_p)
        if check_p.user.username == self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
            user = User.objects.get(username=pk)
            profile = Profile.objects.get(user=user)
            all_users = profile.get_following()
            following_profiles = Profile.objects.filter(user__in=all_users).exclude(user=user)
            print(following_profiles)
            return following_profiles
        else:
            return Profile.objects.none()  # Return an empty queryset if conditions are not met

class ProfileListAPI(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return recommend_profiles(self.request, general=True)
        else:
            # Return a list of general profiles for unauthenticated users
            return Profile.objects.filter(user__gender__iexact='Male').exclude(user__is_superuser=True).filter(cat='General').order_by('?')[:200]

class OrgListAPIView(generics.ListAPIView):
  serializer_class = ProfileSerializer

  def get_queryset(self):
      if self.request.user.is_authenticated:
          return recommend_profiles(self.request, org=True)
      else:
          # Return a list of general profiles for unauthenticated users
          return Profile.objects.filter(cat='Organization').exclude(user__is_superuser=True).order_by('?')[:200]

class ChannelListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return recommend_profiles(self.request, channel=True)
        else:
            # Return a list of general profiles for unauthenticated users
            return Profile.objects.filter(cat='Channel').exclude(user__is_superuser=True).order_by('?')[:200]

class MListAPIView(generics.ListAPIView):
  serializer_class = ProfileSerializer

  def get_queryset(self):
      if self.request.user.is_authenticated:
          return recommend_profiles(self.request, mm=True)
      else:
          # Return a list of general profiles for unauthenticated users
          return Profile.objects.filter(cat='Masjid & Madrasa').exclude(user__is_superuser=True).order_by('?')[:200]

class BrandListAPIView(generics.ListAPIView):
  serializer_class = ProfileSerializer

  def get_queryset(self):
      if self.request.user.is_authenticated:
          return recommend_profiles(self.request, brand=True)
      else:
          # Return a list of general profiles for unauthenticated users
          return Profile.objects.filter(cat='Brand').exclude(user__is_superuser=True).order_by('?')[:200]

from collections import OrderedDict
def recommend_profiles(request, channel=False, org=False, brand=False, mm=False, general=False):
  '''
  Here, if user interact with objects of any type of user, then he will be recommended that user, e.g. if user interact with the Org object, but the profile is pvc_channel of that object, then user will be recommended with that pvc_channel on channel page
  '''
  if request.user.is_authenticated:
    user = request.user
    my_profile = Profile.objects.get(user=user)
    reported_user_ids = my_profile.reported_user().values_list('reported_profile__id', flat=True)

    # suggest profile which is followed by his following
    all_users = my_profile.get_following()
    following_profiles = Profile.objects.filter(user__in=all_users).exclude(user=user)
    all_folls_foll_users = [p.get_following_ids() for p in following_profiles]
    all_folls_foll_users_ids = [id for qs in all_folls_foll_users for id in qs.values_list('id', flat=True)]
    ff_profiles = Profile.objects.filter(user__id__in=all_folls_foll_users_ids).all()
    print('\n******* FF_profiles: ', ff_profiles, '\n') if not PRODUCTION else None

    # suggest user whose pvc has been liked or committed by this user 
    liked_pvc = pvc.objects.filter(likes__user=user).all()
    liked_pvc_creator = list(dict.fromkeys([p.creator.user.id for p in liked_pvc ]))
    pvc_profiles = Profile.objects.filter(user__id__in=liked_pvc_creator).all()
    print(pvc_profiles, '\t**********Reco Based on PVC like') if not PRODUCTION else None

    liked_org = Org.objects.filter(org_upvotes__user=user).all()
    liked_org_creator = list(dict.fromkeys([ p.org_name.user.id for p in liked_org ]))
    org_profiles = Profile.objects.filter(user__id__in=liked_org_creator).all()
    print(org_profiles, '\t**********Reco Based on ORG upvote') if not PRODUCTION else None

    liked_fam = FAM.objects.filter(upvotes__user=user).all()
    liked_fam_creator = list(dict.fromkeys([ p.creator.user.id for p in liked_fam ]))
    fam_profiles = Profile.objects.filter(user__id__in=liked_fam_creator).all()
    print(fam_profiles, '\t**********Reco Based on FAM upvote') if not PRODUCTION else None

    # suggest user who is in same city   
    if my_profile.cur_add:

      if len(my_profile.cur_add.split(',')) == 1: # if karachi, then show all karachiest 
          address = my_profile.cur_add.split(',')[0:1]
      elif len(my_profile.cur_add.split(',')) == 2: # if karachi, sindh, then show all karachiest
          address = my_profile.cur_add.split(',')[0:1]
      else:
          address = my_profile.cur_add.split(',')[:-2] # if more then two then without last two wrods
      profile_location = Q()
      if len(address) == 1:
        profile_location |= Q(cur_add__icontains=address[0].strip())
      else:
        for add in address:
          profile_location |= Q(cur_add__icontains=purify_sentesnse(add.strip()))
      
      local_profile = Profile.objects.filter(
        profile_location).exclude(id=my_profile.id).all().order_by('?')[0:500]
      print(local_profile, '\t********** local_profile') if not PRODUCTION else None
    else:
      local_profile = Profile.objects.none()
    print('\n', local_profile, '\t**********Local Profile\n') if not PRODUCTION else None



    rec_profiles = fam_profiles | org_profiles | pvc_profiles | ff_profiles | local_profile
    rec_profiles = rec_profiles.exclude(Q(user=user) | Q(user__id__in=reported_user_ids) | Q(reported=True) | Q(user__is_superuser=True) | Q(restricted=True)).exclude(pk__in=my_profile.get_following_ids().values_list('id', flat=True)).distinct()
    print('\n', rec_profiles, '\t**********Recommended Profiles\n') if not PRODUCTION else None

    rec_profiles = rec_profiles.exclude(Q(user=user) | Q(user__id__in=reported_user_ids) | Q(reported=True) | Q(user__is_superuser=True) | Q(restricted=True)).exclude(pk__in=my_profile.get_following_ids().values_list('id', flat=True))[:200]
    print('\n', rec_profiles, '\t**********Filtered Recommended Profiles\n') if not PRODUCTION else None

    # will statisfy all thos newbies or those who have not been recommended anything, will recommenda random object, later we will slice
    rest_people= Profile.objects.all().exclude(Q(user=user) | Q(user__id__in=reported_user_ids) | Q(reported=True) | Q(user__is_superuser=True) | Q(pk__in=rec_profiles.values_list('pk', flat=True)) | Q(pk__in=my_profile.get_following_ids().values_list('id', flat=True))).order_by('?')[:200]
    print(rest_people, '\t**********Rest People') if not PRODUCTION else None
    

    all_recom = rec_profiles | rest_people


    if channel: 
      promoted = all_recom.filter(cat__iexact="Channel", promote=True)
      pvc_channels = all_recom.filter(cat__iexact='Channel')[0:400]
      combined = OrderedDict.fromkeys(list(promoted) + list(pvc_channels))
      return combined

    if mm:
      promoted = all_recom.filter(cat__iexact='Masjid & Madrasa', promote=True)
      mm_profiles = all_recom.filter(cat='Masjid & Madrasa')[0:400]
      combined = OrderedDict.fromkeys(list(promoted)+list(mm_profiles))
      print("\n\n\t*** Masjid & Madrasa Rec ***\t= ", combined) if not PRODUCTION else None
      return combined

    if brand: 
      promoted = all_recom.filter(cat__iexact='Brand', promote=True)
      b_profiles = all_recom.filter(cat__iexact='Brand')[0:400]
      combined = OrderedDict.fromkeys(list(promoted)+list(b_profiles))
      print("\n\n\t*** Brands Rec ***\t= ", combined) if not PRODUCTION else None
      return combined

    if org:
      promoted = all_recom.filter(cat__iexact='Organization', promote=True)
      org_profiles = all_recom.filter(cat__iexact='Organization')[0:400]
      combined = OrderedDict.fromkeys(list(promoted)+list(org_profiles))
      print("\n\n\t*** Organizations Rec ***\t= ", combined) if not PRODUCTION else None
      return combined

    if general:
      promoted = all_recom.filter(cat__iexact='General', promote=True)
      general_profiles = all_recom.filter(user__gender__iexact=user.gender, cat='General')[0:400]
      combined = OrderedDict.fromkeys(list(promoted)+list(general_profiles))
      print("\n\n\t*** General Rec ***\t= ", combined) if not PRODUCTION else None
      return combined

class NearMeListAPI(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        check_p = Profile.objects.get(user=self.request.user)
        if check_p.user.username == self.kwargs.get('pk'):
            pk = self.kwargs.get('pk')
            user = User.objects.get(username=pk)
            profile = Profile.objects.get(user=user)

            if not profile.cur_add:
                return Response({"Message": "You need to Add Your Address"})  
            elif len(profile.cur_add.split(',')) == 1:
                address = profile.cur_add.split(',')[0:1]
            elif len(profile.cur_add.split(',')) == 2:
                address = profile.cur_add.split(',')[0:1]
            else:
                address = profile.cur_add.split(',')[:-2]

            profile_location = Q()
            if len(address) == 1:
                profile_location |= Q(cur_add__icontains=address[0].strip())
            else:
                for add in address:
                    profile_location |= Q(cur_add__icontains=add.strip())

            near_me = Profile.objects.filter(profile_location).order_by('?')[:500]

            return near_me
        else:
            return Profile.objects.none()  # Return an empty queryset

def popular(request):
  popular = Profile.objects.exclude(Q(reported=True) | Q(restricted=True)).exclude(user__is_superuser=True)
  context = {}
  context['popular_pro'] = popular
  return render(request, "profiles/popular.html", context)

class FollowUnfollowAPI(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, pk):
      my_profile = Profile.objects.get(user=request.user)  
      user = User.objects.get(username=pk)
      obj = Profile.objects.get(user=user)
      data = {}
      if obj.user in my_profile.following.all():
        my_profile.following.remove(obj.user)
        data['status'] = 'Follow'
        return Response(data)  

      else:
        my_profile.following.add(obj.user)
        recipient = User.objects.get(username=pk)
        recipent_profile = Profile.objects.get(user=recipient)
        data['status'] = 'UnFollow'
        notify.send(request.user, recipient=recipient, verb="Started following you",description= True)
        # if recipient.username == 'Sefarz': # if admin is followed, then don't notify
        # return JsonResponse(data, safe=False)   # just turn email_notif=False
        if recipent_profile.email_notif:
          send_mail(
            f"{my_profile.user.full_name} started following you",
            f"Dear {recipent_profile.user.full_name}, \n\n{my_profile.user.full_name} started following you. check your profile sellbata.com/profile/{recipent_profile.user.username}/followers \n\nRegards,\nTeam Sefarz",
            f"{INFO_EMAIL}",
            [f"{recipient.email}"],
            fail_silently=False,
          )
        return Response(data)  

class remove_followerAPI(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self, request, pk):
    user = User.objects.get(username=pk)
    print("User", user)
    profile = Profile.objects.get(user=user)
    profile.following.remove(self.request.user)
    message = 'Removed Follower'
    return Response({'message': message}, status=status.HTTP_200_OK)

class ProfileUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserSearch(ListView):

#   def get(self, request, *args, **kwargs):
#     profiles = Profile.objects.all().exclude(reported=True).exclude(user__is_superuser=True)
#     query = self.request.GET.get('query').strip()
#     category = self.request.GET.get("category").strip()
#     print("\n***** Category=",category)
#     if query:
#         if request.user.is_authenticated and category == 'General':
#             profile_list = Profile.objects.filter(Q(user__username__iexact=query) | Q(user__full_name__icontains=query)).exclude(Q(user=request.user) | Q(reported=True) | Q(user__is_superuser=True))
#         elif request.user.is_authenticated:
#           profile_list = Profile.objects.filter(Q(user__username__iexact=query) | Q(user__full_name__icontains=query)).exclude(Q(user=request.user) | Q(reported=True) | Q(user__is_superuser=True)).filter(cat=f'{category}')
#         else:
#             profile_list = Profile.objects.filter(Q(user__username__iexact=query) | Q(user__full_name__icontains=query)).exclude(Q(reported=True) | Q(user__is_superuser=True)).filter(cat=f'{category}')
                
#         context = {
#             'search_list': profile_list,
#             'all_profiles': profiles,
#         }
#         if category=='Channel':
#           return render(request, "profiles/channels.html", context)
#         elif category=='Masjid & Madrasa':
#           return render(request, "profiles/Masjid&Madrasa.html", context)
#         elif category=='Brand':
#           return render(request, "profiles/brands.html", context)
#         elif category=='Organization':
#           return render(request, "profiles/organizations.html", context)
#         else: #general
#           return render(request, "profiles/profile_list.html", context)

#     else:
#         return redirect(request.META.get('HTTP_REFERER'))



class UserVuzerAPI(generics.ListAPIView):
    serializer_class = ProfileSerializer  # Set the serializer class here
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.GET.get('query').strip()
        category = self.request.GET.get('category').strip()

        profiles = Profile.objects.all().exclude(reported=True).exclude(user__is_superuser=True)

        filter_kwargs = Q(user__username__iexact=query) | Q(user__full_name__icontains=query)

        if self.request.user.is_authenticated:
            filter_kwargs &= ~Q(user=self.request.user) & ~Q(reported=True) & ~Q(user__is_superuser=True)
            if category == 'General':
                filter_kwargs &= Q(cat=category)
            else:
                filter_kwargs &= Q(cat=category)

        profile_list = Profile.objects.filter(filter_kwargs)
        return profile_list

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'search_list': serializer.data,
        }
        return Response(data)


# class SendAllProfiles(ListView):
#   model = Profile
#   template_name = 'profiles/profile_list.html'
  
#   def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       context['all_Profiles'] = json.dumps(list(Profile.objects.values()))
#       return context



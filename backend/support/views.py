######### Internal ######### 
from .models import Sugg2Savior, ReportUser
from profiles.models import Profile
# from .forms import SefarzMembersForm

######### External ######### 
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from notifications.signals import notify
from django.http import JsonResponse
# from .forms import SaviorMembersForm
from decouple import config

ABSOLUTE_PATH = config('ABSOLUTE_PATH', cast=str, default='/app')
PRODUCTION = config('PRODUCTION', cast=bool)
TESTING = config('TESTING', cast=bool)
# Create your views here.

####################### Rest Framwork #############################
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, filters
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import *
from django.contrib.auth.decorators import login_required


############################### Functions & Classes ################################
class Sugg2SaviorAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.is_authenticated:
            sugg = request.data.get('suggestion')
            profile = Profile.objects.get(user=request.user)

            if sugg:
                suggvar = Sugg2Savior.objects.create(savior_adviser=profile, suggestion=sugg)
                suggvar.save()
                response_data = {
                    'message': 'Your suggestion has been sent to the sellbata, we will check it out. Thanks for your suggestion!'
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    'message': 'You have sent nothing :)'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class ReportUserAPI(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    problem = request.data.get('problem')
    username = request.data.get('username')
    reporter_pro = Profile.objects.get(user=request.user)
    reported_pro= Profile.objects.get(user__username=username)

    # Check if the same user has been reported 10 times
    num_reports = ReportUser.objects.filter(reported_profile=reported_pro).count()
    if num_reports >= 10:
      reported_pro.reported = True
      notify.send(request.user, recipient=reported_pro.user, verb="Your account Has been deactivated, means you can't post, comments, like, upvote, downvote, pay, report, and follow, we will look reports agains you and will let you know about our final decision")
      reported_pro.save()
      return Response({"message": "Your account has been Restricted"})
      

    if reported_pro.reported_profile.filter(reporter_profile=reporter_pro).exists():
      data = {"Message": "You have already reported this user"}
      return Response(data)
    
    elif  problem:
      report_user = ReportUser.objects.create(reporter_profile=reporter_pro, reported_profile=reported_pro, problem=problem)
      report_user.save()
      reported_pro.following.remove(reporter_pro.user)
      reported_pro.save()
      data = {'message': f"You have reported {reported_pro.user.full_name} for {problem}, We are sorry for this inconvenience, we will check it out."}
      return Response(data)

    
    else:
      messages=  f'You have reported nothing :)'
      return Response({"Message": messages})

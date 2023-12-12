from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile
from django.contrib.auth.decorators import login_required
from .forms import SignupForm


def signup(request):

  if request.method=='POST':
    form = SignupForm(request.POST)
    
    if form.is_valid():
      user = form.save()

      team = Team.objects.create(name='The Team Name', created_by=user)
      team.members.add(user)
      team.save()

      Userprofile.objects.create(user=user, active_team=team)


      return redirect('/log-in/')

  else: 
    form = SignupForm()
  
  return render(request, 'userprofile/signup.html', context={
    'form': form,
  })


from team.models import Team 

@login_required
def my_account(request):
  at = Userprofile.objects.get(user=request.user).active_team
  return render(request, 'userprofile/myaccount.html', {'team': at})
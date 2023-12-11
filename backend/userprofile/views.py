from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile
from django.contrib.auth.decorators import login_required



def signup(request):

  if request.method=='POST':
    form = UserCreationForm(request.POST)
    
    if form.is_valid():
      user = form.save()
      userprofile= Userprofile.objects.create(user=user)

      team = Team.objects.create(name='The Team Name', created_by=request.user)
      team.members.add(request.user)
      team.save()


      return redirect('/log-in/')

  else: 
    form = UserCreationForm()
  
  return render(request, 'userprofile/signup.html', context={
    'form': form,
  })


from team.models import Team 

@login_required
def my_account(request):
  team = Team.objects.filter(created_by=request.user)[0]
  return render(request, 'userprofile/myaccount.html', {'team': team})
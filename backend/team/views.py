from django.shortcuts import render, get_object_or_404, redirect
from .models import Team 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TeamForm
from userprofile.models import Userprofile

@login_required
def edit_team(request, pk):
  team = get_object_or_404(Team, created_by=request.user, pk=pk)
  
  if request.method == 'POST':
    form =TeamForm(request.POST, instance=team)
    print("\n===========in the post...")

    if form.is_valid():
      form.save()
      messages.success(request, 'The changes has been saved!' )
      return redirect('my_account')
  else:
    print("\n===========in the post...")
    form = TeamForm(instance=team)

  return render(request, 'team/edit_team.html', {'team': team, 'form': form})



@login_required
def team_detail(request,pk):
  team = get_object_or_404(Team, members__in=[request.user], pk=pk)
  return render(request, 'team/detail.html', {'team': team})


@login_required
def list_team(request):
  teams = Team.objects.filter(members__in=[request.user])
  return render(request, 'team/team_lists.html', {'teams': teams})


@login_required
def team_activate(request, pk):
  team = Team.objects.filter(members__in=[request.user]).get(pk=pk)
  userprofile = Userprofile.objects.get(user=request.user)
  userprofile.active_team = team
  userprofile.save()
  return redirect('team_detail', pk=pk)
  # return render(request, 'team/detail.html')

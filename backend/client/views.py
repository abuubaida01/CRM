from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import AddClientForm
from django.contrib import messages


@login_required
def client_list(request):
  clients = Client.objects.filter(created_by=request.user)
  return render(request, 'client/client_list.html', {"clients": clients})


@login_required
def client_detail(request, pk):
  client = get_object_or_404(Client, created_by=request.user, pk=pk)
  return render(request, 'client/client_detail.html', {
    'client': client,
  })


from team.models import Team


@login_required
def add_client(request):
  team = Team.objects.filter(created_by=request.user)[0]


  if request.method == 'POST':
    form = AddClientForm(request.POST)
    if form.is_valid():
      team = Team.objects.filter(created_by=request.user)[0]
      client = form.save(commit=False)
      client.created_by = request.user 
      client.team = team
      client.save()
      messages.success(request, 'Client created')
      return redirect('client_list')
  else:
    form = AddClientForm()

  return render(request, 'client/add_client.html', {'form': form, 'team': team})
  


@login_required
def client_edit(request, pk): 
  client = get_object_or_404(Client, created_by=request.user, pk=pk)
  if request.method == 'POST':
    form = AddClientForm(request.POST, instance=client)
    if form.is_valid():
      form.save()
      messages.success(request, 'Client was Edited')
      return redirect('client_list')

  else:
    form = AddClientForm(instance=client)
  return render(request, 'client/edit_client.html', {'form': form})




@login_required
def client_delete(request, pk):
  print("in the delete view", pk)
  client = get_object_or_404(Client, created_by=request.user, pk=pk)
  client.delete()
  messages.success(request, 'client was deleted')
  return redirect("client_list")


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Client, ClientFile
from .forms import AddClientForm, CommentForm, ClientFileForm
from django.contrib import messages
import csv
from django.http import HttpResponse

@login_required
def client_export(request):
  clients = Client.objects.filter(created_by=request.user)

  # Create the HttpResponse object with the appropriate CSV header.
  response = HttpResponse(
      content_type="text/csv",
      headers={"Content-Disposition": 'attachment; filename="clients.csv"'},
  )

  writer = csv.writer(response)
  writer.writerow(["Client", "Description", "Created_at", "Created_by"])

  for client in clients:
    writer.writerow([client.name, client.description, client.created_at, client.created_by])
    
  return response



@login_required
def client_list(request):
  clients = Client.objects.filter(created_by=request.user)
  return render(request, 'client/client_list.html', {"clients": clients})

@login_required
def clients_add_file(request, pk):
  client = get_object_or_404(Client, created_by=request.user, pk=pk)
  team = Team.objects.filter(created_by=request.user)[0]

  if request.method=='POST':
    form = ClientFileForm(request.POST, request.FILES)
    if form.is_valid():
      file  = form.save(commit=False)
      file.team = team 
      file.created_by = request.user 
      file.client_id = pk 
      file.save()
      messages.success(request, 'added file')
    return redirect('client_detail', pk=pk)

  else:
    return redirect("client_detail", pk=pk)



@login_required
def client_detail(request, pk):
  client = get_object_or_404(Client, created_by=request.user, pk=pk)
  team = Team.objects.filter(created_by=request.user)[0]
  fileform = ClientFileForm(request.POST)

  if request.method=='POST':
    form = CommentForm(request.POST)

    if form.is_valid():
      comment = form.save(commit=False)
      comment.team = team 
      comment.created_by = request.user 
      comment.client = client
      comment.save()

      return redirect('client_detail', pk=pk)    
  else:
    form = CommentForm()

  return render(request, 'client/client_detail.html', {
    'client': client,
    'form': form,
    'fileform': fileform,
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



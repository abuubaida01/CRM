from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AddLeadForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lead
from django.contrib import messages
from .forms import AddCommentForm, LeadFileForm
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from userprofile.models import Userprofile

@login_required
def leads_list(request):
  leads = Lead.objects.filter(created_by=request.user, converted_to_client=False)
  return render(request, 'lead/leads_list.html', {
    "leads": leads,
  })

class lead_detail(ListView):
  model = Lead 
  context_object_name = 'lead'
  template_name = 'lead/lead_detail.html'
  success_url = reverse_lazy('lead/lead_detail.html')
  
  def get_queryset(self):
      q =  super().get_queryset()
      return q.filter(created_by=self.request.user).get(pk=self.kwargs['pk'])
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["form"] = AddCommentForm() 
      context['fileform'] = LeadFileForm()
      return context
  


class AddCommentView(View):
  def post(self, request, *args, **kwargs):
    content = request.POST.get('content')
    pk = self.kwargs.get('pk')

    form = AddCommentForm(request.POST)
    if form.is_valid():
      at = Userprofile.objects.get(user=request.user).active_team
      
      comment = form.save(commit=False)
      comment.team = at
      comment.created_by = self.request.user 
      comment.lead_id = pk 
      comment.save()
      messages.success(request, 'added comment')

    return redirect('lead_detail', pk=pk)

class AddFileView(View):
  def post(self, request,*args, **kwargs):
    pk = kwargs.get('pk')
    form = LeadFileForm(request.POST, request.FILES)
    if form.is_valid():
      at = Userprofile.objects.get(user=request.user).active_team
      file  = form.save(commit=False)
      file.team = at
      file.created_by = self.request.user 
      file.lead_id = pk 
      file.save()
      messages.success(request, 'added file')
    return redirect('lead_detail', pk=pk)



# @login_required
# def lead_detail(request, pk):
#   lead = Lead.objects.filter(created_by=request.user).get(pk=pk)
#   return render(request, 'lead/lead_detail.html', { 'lead': lead})

from team.models import Team

@login_required
def add_lead(request):
  at = Userprofile.objects.get(user=request.user).active_team

  
  if request.method == 'POST':
    form = AddLeadForm(request.POST)
    if form.is_valid():
      lead = form.save(commit=False)
      lead.created_by = request.user 
      lead.team = at
      lead.save()

      messages.success(request, 'Lead created')
      return redirect('leads_list')
  else:
    form = AddLeadForm()

  return render(request, 'lead/add_lead.html', {'form': form, 'team':team})
  

@login_required
def leads_edit(request, pk): 
  lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
  print('in the edit')
  if request.method == 'POST':
    form = AddLeadForm(request.POST, instance=lead)
    if form.is_valid():
      form.save()
      messages.success(request, 'Lead was Edited')
      return redirect('leads_list')

  else:
    form = AddLeadForm(instance=lead)
  return render(request, 'lead/edit_lead.html', {'form': form})




@login_required
def leads_delete(request, pk):
  print("in the delete view", pk)
  lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
  lead.delete()
  messages.success(request, 'Lead was deleted')
  return redirect("leads_list")


from client.models import Client, Comment as Client_Comment

@login_required
def convert_to_client(request, pk):
  lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
  at = Userprofile.objects.get(user=request.user).active_team



  client = Client.objects.create(name=lead.name, email=lead.email, description=lead.description, created_by=request.user, team=at)

  lead.converted_to_client = True 
  messages.success(request, 'Lead was converted to client')

  lead.save()

  # convert lead comment into client comment
  comments = lead.comments.all()
  for comment in comments:
    Client_Comment.objects.create(
      content= comment.content, 
      client = client,
      created_by=comment.created_by,
      team = team
    )
  return redirect('leads_list')




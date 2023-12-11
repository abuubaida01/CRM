from django.db import models
from django.contrib.auth.models import User
from team.models import Team


CHOICES_PRIORITY = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
  )

CHOICES_STATUS = (
    ('new', 'New'),
    ('contacted', 'Contacted'),
    ('won', 'Won'),
    ('lost', 'Lost'),
  )


class Lead(models.Model):
  created_by = models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  priority = models.CharField(max_length=10, choices=CHOICES_PRIORITY, default='medium')
  status = models.CharField(max_length=10, choices=CHOICES_STATUS, default='new')
  name = models.CharField(max_length=255)
  email = models.EmailField()
  description = models.TextField(blank=True, null=True)
  converted_to_client = models.BooleanField(default=False)
  team = models.ForeignKey(Team, related_name='leads', on_delete=models.CASCADE)

  class Meta:
    ordering = ('name',)
    
  def __str__(self):
    return self.name



class LeadFile(models.Model):
  team = models.ForeignKey(Team, related_name='lead_file', on_delete=models.CASCADE)
  lead = models.ForeignKey(Lead, related_name='files', on_delete=models.CASCADE)
  created_by = models.ForeignKey(User, related_name='user_lead_file', on_delete=models.CASCADE)
  file = models.FileField(upload_to='leadFiles/')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-created_at',)
    
  def __str__(self):
    return self.created_by.username


class Comment(models.Model):
  team = models.ForeignKey(Team, related_name='lead_comments', on_delete=models.CASCADE)
  lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE)
  created_by = models.ForeignKey(User, related_name='user_lead_comment', on_delete=models.CASCADE)
  content = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-created_at',)
    
  def __str__(self):
    return self.created_by.username

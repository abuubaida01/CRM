from django.db import models
from team.models import Team
from profiles.models import Profile


class Client(models.Model):
  team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
  created_by = models.ForeignKey(Profile, related_name='client', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)
  name = models.CharField(max_length=255)
  email = models.EmailField()
  description = models.TextField(blank=True, null=True)


  class Meta:
    ordering = ('name',)
    
  def __str__(self):
    return self.name



class ClientFile(models.Model):
  team = models.ForeignKey(Team, related_name='client_file', on_delete=models.CASCADE)
  client = models.ForeignKey(Client, related_name='files', on_delete=models.CASCADE)
  created_by = models.ForeignKey(Profile, related_name='user_client_file', on_delete=models.CASCADE)
  file = models.FileField(upload_to='clientFiles/')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-created_at',)
    
  def __str__(self):
    return self.created_by.username


class Comment(models.Model):
  team = models.ForeignKey(Team, related_name='client_comments', on_delete=models.CASCADE)
  client = models.ForeignKey(Client, related_name='comments', on_delete=models.CASCADE)
  created_by = models.ForeignKey(Profile, related_name='user_client_comment', on_delete=models.CASCADE)
  content = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('-created_at',)
    
  def __str__(self):
    return self.created_by.username

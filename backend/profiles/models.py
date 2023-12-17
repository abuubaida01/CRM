from django.db import models
from django.contrib.auth import get_user_model
from user.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.core.mail import send_mail
from notifications.signals import notify
# from team.models import Team

from decouple import config
# PRODUCTION = config('PRODUCTION', cast=bool)
# TESTING = config('TESTING', cast=bool)
INFO_EMAIL = config('INFO_EMAIL', cast=str, default='famior01@gmail.com')

class Profile(models.Model):
  user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  picture             = models.ImageField(default='media/picture.jpg', upload_to='media/picture/')
  intro               = models.TextField(max_length=500, blank=True)
  slogan              = models.CharField(max_length=100, blank=True)
  profession          = models.CharField(max_length=200, blank=True)
  cur_add             = models.CharField(max_length=500, blank=True) 
  phone_number        = PhoneNumberField(null=True, unique=False, blank=True)
  bank_details        = models.CharField(max_length=500, blank=True)

  fam_post_no         = models.IntegerField(default=0)
  org_post_no         = models.IntegerField(default=0)
  kind                = models.CharField(max_length=100, blank=True) # creator, supporter, org
  following           = models.ManyToManyField(User, related_name='following', blank=True)
  
  # active_team         = models.ForeignKey(Team, related_name='profileTream', on_delete=models.SET_NULL, null=True, blank=True)
  reported            = models.BooleanField(default=False, blank=True) 
  restricted          = models.BooleanField(default=False, blank=True) 
  updated             = models.DateTimeField(auto_now=True)
  created             = models.DateTimeField(auto_now_add=True)
  promote             = models.BooleanField(default=False, blank=True)

  restriction_hits    = models.IntegerField(default=0)
  restricted          = models.BooleanField(default=False, blank=True) 

  admin_message       = models.TextField(blank=True)
  email_notif         = models.BooleanField(default=False, blank=True)
  cat                 = models.CharField(blank=True, max_length=200, default='General')

  def __str__(self):
    # String representation of the model
    return str(self.user)

  def profile_pvc(self):
    return self.pvc_set.all() 

  def reported_pvc(self):
    return self.pvc_reporter.all()

  def reported_zakat(self): 
    return self.zakat_reporter.all()

  def reported_org(self): 
    return self.org_reporter.all() 

  def reported_user(self): 
    return self.reporter_profile.all()

  def get_following(self):
    return self.following.all()

  def get_following_ids(self):
    return self.following.values_list('id', flat=True)

  # Get all profiles that are not being followed by the user
  def get_unfollowing(self):
    user = self.following.all()
    return Profile.objects.exclude(user__in=user).exclude(user=self.user)

  def get_following_no(self):
    user = self.following.all()
    return Profile.objects.filter(user__in=user).exclude(user=self.user).count()

  def get_follower_no(self):
    total_profiles = Profile.objects.filter(following=self.user).exclude(user=self.user).count()
    return total_profiles

  def get_followers(self):
    all_users = Profile.objects.filter(following=self.user).all()
    return all_users

  # to get the absolute url of the profile
  def get_absolute_url(self):
    return reverse("profiles:profile-detail-view", kwargs={"user": self.user}) 

  def get_post_no(self):
    return self.pvc.all().count() 

  def get_all_authors_posts(self):
    return self.pvc.all()  

  def get_fam(self):
    return self.fam.all()

  def get_fam_no(self): 
    total_verified_posts = self.fam.filter(verified__gte=50).count()
    return total_verified_posts

  def get_all_org_posts(self):
    return self.Org.all()
  
  def get_org_count(self):
    return self.Org.all().count()


  def get_all_ads_posts(self):
    return self.savads.all()
  
  def get_ads_count(self):
    return self.savads.all().count()


  def total_pvc_likes_by_curruser(self):
    return self.pvc_likes.all().count()

  def total_pvc_dislikes_by_curruser(self):
    return self.pvc_dislike.all().count()

  def total_pvcIncome(self):
    return self.profile_income.aggregate(models.Sum('amount'))['amount__sum'] or 0.00


  def is_pvc_profile_verified(self):
    verify_pvc = self.verified_pvc.first()
    if verify_pvc:
        return verify_pvc.PVCVerified
    return False
  
  def type_of_verified_org(self):
    verify_org = self.Verify_profile_org.first()
    if verify_org:
        return verify_org.org_type
    return ''

  def save(self, *args, **kwargs):
    first_state = 0
    if self.restriction_hits >= 3 and not self.restricted:
      self.restricted = True
      self.reported = True
      self.restriction_hits = 0
      send_mail(
        f"Your Account got 3 Restriction and is now Restricted",
        f"Dear {self.user.full_name},\n\nYour account has been restricted due to a violation of Sefarz. As a result, your activities are no longer being displayed to the public. If you believe this decision was made in error, please contact us at contact.sellbata@gmail.com.\n\nRegards,\nSefarz Team",
        f"{INFO_EMAIL}",
        [f"{self.user.email}"],
        fail_silently=False,
      )
      notify.send(self.user, recipient=self.user, verb='Your account has been restricted due to violation of Sefarz Community Guidelines. Please check your email.')
      first_state = self.restriction_hits

    elif self.restriction_hits >= first_state and not self.restricted and self.restriction_hits>0 :
      send_mail(
        f"Your Account Got {self.restriction_hits} Restriction ",
        f"Dear {self.user.full_name},\n\nYour Account Got {self.restriction_hits} Restriction out of 3, Please ensure that you adhere to our policies to avoid further restrictions.\n\n{self.admin_message}\n\nRegards,\nSefarz Team",
        f"{INFO_EMAIL}",
        [f"{self.user.email}"],
        fail_silently=False,
      )
      notify.send(self.user, recipient=self.user, verb=f'Your account got {self.restriction_hits} Restriction out of 3. Please check your email.')
      first_state = self.restriction_hits

    else:
      if len(self.admin_message) > 0:
        send_mail(
          f"Violation of Sefarz Community Guidelines",
          f"Dear {self.user.first_name},\n\n{self.admin_message}\n\nRegards,\nSefarz Team",
          f"{INFO_EMAIL}",
          [f"{self.user.email}"],
          fail_silently=False,
        )
        self.admin_message = ''
        notify.send(self.user, recipient=self.user, verb='We have sent you an email regarding the voilation of Sefarz Community Guidelines. Please check your email.')

    super().save(*args, **kwargs)

  # def get_likes_given_no(self):
  #   """
  #   like has a relationship with the profile model
  #   """
  #   likes = self.like_set.all() # type: ignore
  #   total_liked = 0
  #   for item in likes:
  #     if item.value == 'Like':
  #         total_liked += 1
  #   return total_liked

  # def get_likes_recieved_no(self):
  #   posts = self.pvc.all() # type: ignore
  #   total_posts = 0
  #   for item in posts:
  #     total_posts+= item.likes.all().count()
  #   return total_posts
  
  class Meta:
    ordering = ['-created']

  # __initial_first_name = None
  # __initial_last_name = None

  
  # def __init__(self, *args, **kwargs):
  #   super().__init__(*args, **kwargs)
  #   self.__initial_first_name = self.first_name
  #   self.__initial_last_name = self.last_name

  # # to set the slug
  # def save(self, *args, **kwargs):
  #       ex = False
  #       to_slug = self.slug
  #       if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
  #           if self.first_name and self.last_name:
  #               to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
  #               ex = Profile.objects.filter(slug=to_slug).exists()
  #               while ex:
  #                   to_slug = slugify(to_slug + " " + str(get_random_code()))
  #                   ex = Profile.objects.filter(slug=to_slug).exists()
  #           else:
  #               to_slug = str(self.user)
  #       self.slug = to_slug
  #       super().save(*args, **kwargs)





class VerifyUser(models.Model):
  Vuser = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='VerifyUser')
  idcard = models.ImageField(upload_to='idcard', blank=True, null=True)
  UserVerified = models.BooleanField(default=False)

  def __str__(self):
    return self.Vuser.user.username

class vpvc_creator(models.Model):
  Vpvc = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='VerifyPVC')
  pvc_verified = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.Vpvc.user.username






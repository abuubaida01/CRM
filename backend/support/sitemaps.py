from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['terms_and_conditions', 'privacy_policy']

    def location(self, item):
    # Update the URL name to match the actual name in your urls.py
      return reverse('support:' + item)

    # def lastmod(self, item):
    #     if item == 'terms_and_conditions':
    #         return timezone.now()

    # def get_latest_lastmod(self, obj):
    #     return self.lastmod('terms_and_conditions')



# from pvc.models import pvc

# class PVCSitemap(Sitemap):
#     changefreq = 'weekly' # can be weekly daily always monthly yearly or never
#     priority = 1.0   # on a scale of 0.0 to 1.0
#     protocol = 'http'  # use https when you deploy your website and are using a secure connection

#     # define the posts you want in your sitemap here
#     def items(self):
#         return pvc.objects.all()

#     # will return the last time an article was updated
#     def lastmod(self, obj):
#         return obj.created
    
#     # will return the location of each post
#     def location(self, obj):
#       return f'/pvc/{obj.pk}'



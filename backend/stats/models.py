from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Statistic(models.Model):
  name = models.CharField(max_length=200)
  slug = models.SlugField(blank=True)

  @property
  def data(self):
    return self.dataitem_set.all()

  def get_absolute_url(self):
    return reverse("stats:dashboard", kwargs={"slug": self.slug})

  def __str__(self):
    return  str(self.name)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)

    super().save(*args, **kwargs)


class DataItems(models.Model):
  statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE, related_name='dataitem_set')
  value = models.PositiveSmallIntegerField()
  owner = models.CharField(max_length=200)

  def __str__(self):
    return f"{self.owner}, and {self.value}"
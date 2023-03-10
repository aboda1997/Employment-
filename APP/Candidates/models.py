from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
User = get_user_model()
from django.utils import timezone
from django_countries.fields import CountryField
from job.models import Job
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
    ('Remote', 'Remote'),
)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    location = models.CharField(max_length=255, null=True, blank=True)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    grad_year = models.IntegerField(blank=True ,default=2000)
    looking_for = models.CharField(
        max_length=30, choices=CHOICES, default='Full Time', null=True)
    slug = AutoSlugField(populate_from='user', unique=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')


    def __str__(self):
        return self.slug 


class Skill(models.Model):
    skill = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, related_name='skills', on_delete=models.CASCADE)


class SavedJobs(models.Model):
    job = models.ForeignKey(
        Job, related_name='saved_job', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='saved', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job.title


class AppliedJobs(models.Model):
    job = models.ForeignKey(
        Job, related_name='applied_job', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='applied_user', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job.title

from django.conf import settings
from django.db import models
from djangoldp_conversation.models import Conversation

from djangoldp.models import Model
from djangoldp_skill.models import Skill

job_fields = ["@id", "author", "title", "description", "creationDate", "skills", "closingDate", "conversation"]
if 'djangoldp_community' in settings.DJANGOLDP_PACKAGES:
    job_fields += ['community']


class JobOffer(Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='jobOffers', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    closingDate = models.DateField(null=True)
    conversation = models.ManyToManyField(Conversation, blank=True)

    class Meta:
        auto_author = 'author'
        owner_field = 'author'
        nested_fields = ["skills", "conversation"]
        anonymous_perms = ["view"]
        authenticated_perms = ["inherit", "add"]
        owner_perms = ["inherit", "change", "delete"]
        container_path = 'job-offers/'
        serializer_fields = job_fields
        rdf_type = 'hd:joboffer'

    def __str__(self):
        return '{} ({})'.format(self.title, self.author.get_full_name())

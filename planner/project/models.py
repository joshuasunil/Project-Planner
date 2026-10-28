from django.db import models


import uuid

from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.

class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    class Meta:

        abstract = True

class Project(BaseClass):

    name = models.CharField(max_length=250)

    description = CKEditor5Field()

    document = models.FileField(upload_to='project-documents')


    class Meta :

        verbose_name = 'Project'

        verbose_name_plural = 'Projects'


    def __str__(self):

        return self.name


class AssignedProjects(BaseClass):

    project = models.ForeignKey('Project',on_delete=models.PROTECT,related_name='project')

    coordinator = models.ForeignKey('authentication.Profile',on_delete=models.PROTECT,related_name='coordinator')

    developers = models.ManyToManyField('authentication.Profile')

    project_duration = models.IntegerField()

    project_start_date = models.DateField()

    project_tentative_end_date = models.DateField()

    completed = models.BooleanField(default=False)

    completed_date = models.DateField(null=True , blank=True)


    class Meta :

        verbose_name = 'Assigned Project'

        verbose_name_plural = 'Assigned Projects'


    def __str__(self):

        return f'{self.project.name}-{self.project_start_date}'
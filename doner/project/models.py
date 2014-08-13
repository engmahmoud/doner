from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


STATUS_CODES = (
    (1, _('Open')),
    (2, _('Working')),
    (3, _('Closed')),
)

PRIORITY_CODES = (
    (1, _('High')),
    (2, _('Medium')),
    (3, _('Low')),
)

TICKET_TYPES = (
    (1, _('Task')),
    (2, _('Bug')),
    (3, _('Improvement')),
    (4, _('Research')),
)


class Project(models.Model):

    name = models.CharField(verbose_name=_('Name'), max_length=50)
    description = models.CharField(verbose_name=_('Description'), max_length=250, blank=True)
    is_private = models.BooleanField(verbose_name=_('Private'), default=False)
    created_date = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)
    last_active = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='project_members')
    members_number = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __unicode__(self):
        return u'%s' % self.name


class Attachment(models.Model):

    attachment = models.FileField(upload_to='attachments/', help_text='(optional)')
    created_date = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

    def __str__(self):
        return self.attachment.name.replace('attachments/', '')


class Ticket(models.Model):

    project = models.ForeignKey(Project, verbose_name=_('Project'))
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    submitted_date = models.DateTimeField(verbose_name=_('Submited date'), auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name=_('Modified date'), auto_now=True)

    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Submitter'), related_name='submitter')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Assigned to'), null=True, blank=True)

    status = models.IntegerField(verbose_name=_('Status'), default=1, choices=STATUS_CODES)
    priority = models.IntegerField(verbose_name=_('Priority'), default=2, choices=PRIORITY_CODES)
    ttype = models.IntegerField(verbose_name=_('Ticket type'), default=1, choices=TICKET_TYPES)

    attachments = models.ManyToManyField(Attachment, null=True, blank=True)

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    def __unicode__(self):
        return u'%s' % self.title
